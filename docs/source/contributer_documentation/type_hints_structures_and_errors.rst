..
   matrixctl
   Copyright (c) 2021  Michael Sasser <Michael@MichaelSasser.org>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

Type Hints, Structures and Errors
*********************************

MatrixCtl is strictly typed to avoid some bugs and help contributors in the
future to easily identify what they are dealing with. They can be used by third
party tools such as type checkers, IDEs, linters, etc.

In addition we make use of ``TypedDict`` to create typed structures (add
type hints to e.g. the configuration).

MatrixCtl specifies some additional errors. Those errors are informing the
user that, getting a traceback is a bug in this application.
They are giving the person instructions, how to hand in a bug report.

Type Hints
----------

.. automodule:: matrixctl.typehints
   :members:
   :undoc-members:
   :show-inheritance:

Structures
----------

.. automodule:: matrixctl.structures
   :members:
   :undoc-members:
   :show-inheritance:

Errors
------

.. automodule:: matrixctl.errors
   :members:
   :undoc-members:
   :show-inheritance:

..
   vim: set ft=rst :
