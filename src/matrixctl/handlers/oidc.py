"""An OIDC Client for Matrix Authentication Service.

If you are reading this you might probably ask yourself:
"why yet another OIDC client?". The answer is unfortunately. It was easier to
write one from scratch (for this specific usecase) than to use any of the
existing ones I found. Either the documentation was in a devastating state
or they were unmaintained for years. It's pretty sad.

Nevertheless, this should not stop us from having nice things, too.
So here we are with yet another OIDC client.

"""

from __future__ import annotations

import base64
import hashlib
import http.server
import json
import logging
import secrets
import socketserver
import threading
import time
import typing as t
import urllib.parse
import webbrowser

from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

import httpx

from xdg_base_dirs import xdg_data_home

from matrixctl.typehints import JsonDict


__author__: str = "Michael Sasser"
__email__: str = "Michael@MichaelSasser.org"

logger = logging.getLogger(__name__)


class OidcTCPServer(socketserver.TCPServer):
    """TCP server wrapper for handling OIDC authentication callbacks.

    This server listens for incoming HTTP requests containing the OIDC
    authorization code and stores it for later retrieval.

    """

    def __init__(
        self,
        server_address: tuple[str, int],
        RequestHandlerClass: type[socketserver.BaseRequestHandler],  # noqa: N803
    ) -> None:
        """Initialize the OidcTCPServer.

        This mehod only adds the `auth_code` attribute to the server instance.

        Parameters
        ----------
        server_address : tuple[str, int]
            The address on which the server listens.
        RequestHandlerClass : type[socketserver.BaseRequestHandler])
            The request handler class.
        """
        super().__init__(server_address, RequestHandlerClass)
        self.auth_code: str | None = None


class TokenManager:
    """Manager for OIDC tokens handling.

    It supports both client credentials and authorization code flows.

    Parameters
    ----------
    token_endpoint : str
        OIDC provider's token endpoint URL
    client_id : str
        Client ID for OIDC authentication
    client_secret : str
        Client secret for OIDC authentication
    auth_endpoint : str | None, optional
        Authorization endpoint URL for user authentication flow, by default
        None
    userinfo_endpoint : str | None, optional
        Userinfo endpoint URL, by default None
    jwks_uri : str | None, optional
        JWKS endpoint URL, by default None
    cache_path : str, optional
        Path to token cache file, by default "~/.oidc_token_cache.json"
    """

    wait_for_auth_code_timeout: int = 300

    def __init__(  # noqa: PLR0913
        self,
        token_endpoint: str,
        client_id: str,
        client_secret: str,
        auth_endpoint: str | None = None,
        userinfo_endpoint: str | None = None,
        jwks_uri: str | None = None,
        cache_path: Path | None = None,
    ) -> None:
        data_home = xdg_data_home() / "matrixctl"

        self.token_endpoint: str = token_endpoint
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.auth_endpoint: str | None = auth_endpoint
        self.userinfo_endpoint: str | None = userinfo_endpoint
        self.jwks_uri: str | None = jwks_uri
        self.cache_path: Path = (
            cache_path or data_home / "oidc_token_cache.json"
        )
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self.id_token: str | None = None
        self.expires_at: float = 0.0
        logger.debug(
            "TokenManager initialized with cache path: %s", self.cache_path
        )

    def recall_cached_token(self, key: str) -> bool:
        """Load and validate cached tokens from disk.

        Returns
        -------
        bool
            True if valid token was loaded, False otherwise

        Notes
        -----
        Sets instance attributes:
        - access_token: Loaded access token or None
        - refresh_token: Loaded refresh token or None
        - expires_at: Expiration timestamp or 0
        """
        try:
            if not self.cache_path.exists():
                logger.debug(
                    "Cache file does not exist: %s",
                    self.cache_path,
                )
                return False

            with self.cache_path.open() as fp:
                data: JsonDict = json.load(fp)

            logger.debug("Cache file exists: %s", self.cache_path)
            keyed: JsonDict = t.cast(JsonDict, data.get(key.strip().lower()))

            self.access_token = keyed.get("access_token")
            self.refresh_token = keyed.get("refresh_token")
            self.id_token = keyed.get("id_token") or self.id_token
            self.expires_at = keyed.get("expires_at", 0.0)

            logger.debug(
                "Recalled refresh token contains: "
                "{access_token: %s, "
                "refresh_token: %s, "
                "id_token: %s, "
                "expires_at: %s}",
                self.access_token is not None,
                self.refresh_token is not None,
                self.id_token is not None,
                self.expires_at is not None,
            )

            if time.time() < self.expires_at:
                logger.debug("Token is not expired on recall")
                return True
        except PermissionError:
            logger.exception(
                "Insufficiant permissions to opent the file: %s",
                self.cache_path,
            )
        except IsADirectoryError:
            logger.exception(
                (
                    "The oidc token cache file %s should be a file, not "
                    "a directory"
                ),
                self.cache_path,
            )
        except OSError:
            logger.exception("Failed to open/write to oidc token cache file")
        except json.JSONDecodeError:
            logger.exception(
                (
                    "The oidc token cache file exist, but it's content is not "
                    "valid JSON: %s"
                ),
                self.cache_path,
            )
        except AttributeError:
            logger.exception(
                (
                    "The oidc token cache file exist, but it's content is not "
                    "does not contain the expected keys. Cache file: %s"
                ),
                self.cache_path,
            )

        self.access_token = None
        self.expires_at = 0.0
        logger.debug("Token is expired or invalid")
        return False

    def store_cache_token(
        self,
        access_token: str,
        refresh_token: str | None,
        id_token: str | None,
        expires_in: int,
        key: str,
    ) -> None:
        """Cache tokens to disk with expiration information.

        Parameters
        ----------
        access_token : str
            New access token to cache
        refresh_token : str | None
            Optional refresh token to cache
        expires_in : int
            Time in seconds until token expiration

        Notes
        -----
        Updates instance attributes:
        - access_token
        - refresh_token
        - expires_at
        """
        logger.debug("Started storing cached token: %s", self.cache_path)
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_at = time.time() + expires_in

        logger.debug(
            "Stored refresh token contains: "
            "{access_token: %s, "
            "refresh_token: %s, "
            "id_token: %s, "
            "expires_at: %s}",
            self.access_token is not None,
            self.refresh_token is not None,
            self.id_token is not None,
            self.expires_at is not None,
        )

        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.touch(exist_ok=True)
            self.cache_path.chmod(0o600)
            with self.cache_path.open("w") as fp:
                json.dump(
                    {
                        key.strip().lower(): {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "id_token": id_token,
                            "expires_at": self.expires_at,
                        }
                    },
                    fp,
                )
        except PermissionError:
            logger.exception(
                "Insufficiant permissions to opent the file: %s",
                self.cache_path,
            )
        except IsADirectoryError:
            logger.exception(
                (
                    "The oidc token cache file %s must be a file, "
                    "not a directory"
                ),
                self.cache_path,
            )
        except OSError:
            logger.exception("Failed to open/write to oidc token cache file")
        logger.debug("Finished storing cached token: %s", self.cache_path)

    def get_user_info(self) -> JsonDict:
        """Retrieve user information from the userinfo endpoint.

        Returns
        -------
        dict[str, Any]
            User claims dictionary

        Raises
        ------
        ValueError
            If userinfo endpoint not configured or no access token
        httpx.HTTPStatusError
            For HTTP request failures
        """
        err_msg: str
        if not self.userinfo_endpoint:
            err_msg = "Userinfo endpoint not configured"
            raise ValueError(err_msg)

        if not self.access_token:
            err_msg = "No access token available"
            raise ValueError(err_msg)

        response = httpx.get(
            self.userinfo_endpoint,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=10,
        )
        _ = response.raise_for_status()
        user_info: JsonDict = t.cast(JsonDict, response.json())
        logger.debug("User info retrieved: %s", user_info)
        return user_info

    def get_payload(self) -> JsonDict:
        """Decode payload from the ID token.

        Returns
        -------
        dict[str, Any]
            Decoded ID token payload

        Raises
        ------
        ValueError
            If no ID token available
        """
        if not self.id_token:
            err_: str = "No ID token available"
            raise ValueError(err_)

        try:
            # Split JWT into parts
            _, payload_unpadded, _ = self.id_token.split(".")
            # Add padding and decode
            payload_padded = payload_unpadded + "=" * (
                -len(payload_unpadded) % 4
            )
            payload_decoded = base64.urlsafe_b64decode(payload_padded)
            payload: JsonDict = t.cast(JsonDict, json.loads(payload_decoded))

        except json.JSONDecodeError:
            logger.exception(
                ("Unable to decode payload. Invalid JSON"),
            )
            raise

        logger.debug("Payload decoded: %s", payload)
        return payload

    def get_client_credentials_token(self) -> str:
        """Get access token using client credentials flow.

        Returns
        -------
        str
            Valid access token

        Raises
        ------
        httpx.HTTPStatusError
            For HTTP request failures
        ValueError
            If token response is invalid
        """
        logger.debug("Started client credentials token request")
        if self.recall_cached_token("user") and self.access_token:
            logger.debug(
                "Recalled cached token, which contains the  access token."
            )
            if time.time() < self.expires_at:
                logger.debug("Recalled token is not expired")
                return self.access_token
            logger.debug("Recalled token is expired, refreshing it")
            refresh_token = self.refresh_access_token()
            if refresh_token:
                return refresh_token

        try:
            response = httpx.post(
                self.token_endpoint,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=10,
            )
            _ = response.raise_for_status()
            token_data: dict[str, t.Any] = t.cast(
                dict[str, t.Any], response.json()
            )
        except httpx.HTTPStatusError as e:
            logger.exception(
                "Token request failed: %s %s",
                e.response.status_code,
                e.response.text,
            )
            raise

        except json.JSONDecodeError:
            logger.exception(
                (
                    "The returned client credentials token could not be "
                    "decoded. Invalid JSON"
                ),
            )
            raise

        access_token: str
        if not (access_token := t.cast(str, token_data.get("access_token"))):
            err_msg: str = "No access token in response"
            raise ValueError(err_msg)

        self.store_cache_token(
            access_token,
            token_data.get("refresh_token"),
            token_data.get("id_token") or self.id_token,
            t.cast(int, token_data.get("expires_in", 3600)),
            "user",
        )
        return access_token

    @staticmethod
    def _generate_pkce() -> tuple[str, str]:
        """Generate PKCE code verifier and challenge pair.

        Returns
        -------
        tuple[str, str]
            (code_verifier, code_challenge) pair
        """
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            )
            .decode()
            .replace("=", "")
        )
        return code_verifier, code_challenge

    def _start_local_server(self) -> tuple[OidcTCPServer, int]:
        """Start temporary HTTP server for OIDC callback.

        Returns
        -------
        tuple[OidcTCPServer, int]
            (server instance, port number)
        """

        class CallbackHandler(http.server.SimpleHTTPRequestHandler):
            """Handler for OIDC redirect with authorization code capture."""

            def do_GET(self) -> None:  # noqa: N802
                """Handle GET request for OIDC callback."""
                query = parse_qs(urlparse(self.path).query)
                if "code" in query:
                    self.send_response(200)
                    self.end_headers()
                    _ = self.wfile.write(
                        b"Authentication successful! "
                        b"You can close this window."
                    )
                    auth_server = t.cast(OidcTCPServer, self.server)
                    auth_server.auth_code = query["code"][0]
                else:
                    self.send_response(400)
                    self.end_headers()
                    _ = self.wfile.write(b"Missing authorization code")

        # TODO: Find out if we can do random ports in MAS instead of having
        #       a fixed one.
        server_address: tuple[str, int] = ("127.0.0.1", 8298)
        server = OidcTCPServer(server_address, CallbackHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        return server, server.server_address[1]

    def get_user_token(self, claims: t.Iterable[str]) -> str:
        """Get access token using authorization code flow with PKCE.

        Returns
        -------
        str
            Valid access token

        Raises
        ------
        TimeoutError
            If user doesn't complete authentication within 5 minutes
        httpx.HTTPStatusError
            For HTTP request failures
        ValueError
            If token response is invalid
        """
        self.recall_cached_token("user")
        logger.debug("Recalled cached token for 'user'")

        if self.access_token and time.time() < self.expires_at:
            logger.debug("Recalled acces token exists and is not expired")
            return self.access_token
        logger.debug("Recalled access token was invalid or is expired")

        if self.refresh_token:
            logger.debug("Refresh token exists")
            new_access_token = self.refresh_access_token()
            logger.debug(
                "Using recalled refresh token token to get a new access token"
            )
            if new_access_token:
                logger.debug("Refreshed access token exists")
                return new_access_token

        code_verifier, code_challenge = self._generate_pkce()
        server, port = self._start_local_server()
        logger.debug("Started local server")
        # TODO: make this configuratble
        redirect_uri = f"http://127.0.0.1:{port}/callback"

        auth_url = f"{self.auth_endpoint}?"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(claims),
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": "active",
        }
        url: str = f"{auth_url}{urllib.parse.urlencode(params)}"

        if webbrowser.open_new_tab(url):
            print("A new tab should have opened in your browser.")
            print(
                "If not, please visit this URL in your browser "
                f"manually:\n{url}\n"
            )
        else:
            print(f"Please visit this URL in your browser:\n{url}\n")

        try:
            start_time = time.time()
            while (
                time.time() - start_time
                < type(self).wait_for_auth_code_timeout
            ):  # 5 minute timeout
                if server.auth_code:
                    logger.debug("Got auth code from from browser flow")
                    break
                time.sleep(1)
            else:
                err_msg: str = "Authorization timed out"
                logger.debug("Browser flow authorization timed out")
                raise TimeoutError(err_msg)

            logger.debug("Requesting access token")
            token_response = httpx.post(
                self.token_endpoint,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": server.auth_code,
                    "redirect_uri": redirect_uri,
                    "state": "active",
                    "code_verifier": code_verifier,
                },
            )
            _ = token_response.raise_for_status()
            token_data: JsonDict = t.cast(JsonDict, token_response.json())

            access_token: str = t.cast(str, token_data.get("access_token"))
            logger.debug("Got response from requesting access token")
            if not access_token:
                logger.debug("There was no acccess token in the response")
                err_msg = "No access token in response"
                raise ValueError(err_msg)

            self.store_cache_token(
                access_token,
                token_data.get("refresh_token"),
                token_data.get("id_token") or self.id_token,
                t.cast(int, token_data.get("expires_in", 3600)),
                "user",
            )
            logger.debug("Cached token stored")
            return access_token
        finally:
            logger.debug("Shutting down web server")
            server.shutdown()

    def refresh_access_token(self) -> str | None:
        """Refresh access token using refresh token.

        Returns
        -------
        str | None
            New access token if successful, None otherwise
        """
        logger.debug("Started refresing access token")
        if not self.refresh_token:
            logger.debug(
                "Unable to refresh access token. "
                "I don not have a refresh token"
            )
            return None

        try:
            response = httpx.post(
                self.token_endpoint,
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                },
            )
            _ = response.raise_for_status()
            logger.debug("Got refresh token response")
            token_data: JsonDict = t.cast(JsonDict, response.json())

            access_token: str
            if access_token := t.cast(str, token_data.get("access_token")):
                self.store_cache_token(
                    access_token,
                    t.cast(
                        str,
                        token_data.get("refresh_token", self.refresh_token),
                    ),
                    token_data.get("id_token") or self.id_token,
                    t.cast(int, token_data.get("expires_in", 3600)),
                    "user",
                )
                logger.debug("Stored refreshed token")
                return access_token
        except httpx.HTTPStatusError as e:
            logger.exception(
                "Token refresh failed: %s %s",
                e.response.status_code,
                e.response.text,
            )
            return None
        except json.JSONDecodeError:
            logger.exception(
                (
                    "The returned refresh token could not be decoded. Invalid "
                    "JSON: %s"
                ),
                self.cache_path,
            )
            return None

        logger.error("No access token in response")
        return None

    def _exchange_code(  # TODO: Unused
        self, code_verifier: str, auth_code: str | None, redirect_uri: str
    ) -> dict[str, t.Any]:
        """Exchange authorization code for tokens."""
        if not auth_code:
            err_msg = "Missing authorization code"
            raise ValueError(err_msg)

        response = httpx.post(
            self.token_endpoint,
            data={
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": auth_code,
                "redirect_uri": redirect_uri,
                "state": "active",
                "code_verifier": code_verifier,
            },
        )
        _ = response.raise_for_status()
        return t.cast(dict[str, t.Any], response.json())


def discover_oidc_endpoints(issuer_url: str) -> JsonDict:
    """Retrieve OIDC provider configuration via discovery.

    Parameters
    ----------
    issuer_url : str
        Base URL of the OIDC issuer

    Returns
    -------
    dict[str, t.Any]
        OIDC provider configuration

    Raises
    ------
    httpx.HTTPStatusError
        For HTTP request failures
    ValueError
        If discovery document is invalid
    """
    try:
        discovery_url = issuer_url.rstrip("/")
        response = httpx.get(discovery_url, timeout=10)
        _ = response.raise_for_status()
        oidc_config: JsonDict = t.cast(JsonDict, response.json())
    except httpx.HTTPStatusError as e:
        logger.exception(
            "Discovery request failed: %s %s",
            e.response.status_code,
            e.response.text,
        )
        raise

    except json.JSONDecodeError:
        logger.exception(
            (
                "The discovery request JSON response could not be "
                "decoded. Invalid JSON: %s"
            ),
            response,
        )
        raise

    logger.debug("OIDC discovery response: %s", oidc_config)
    return oidc_config
