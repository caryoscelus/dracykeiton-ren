##
##  Copyright (C) 2015 caryoscelus
##
##  This file is part of Dracykeiton
##  https://github.com/caryoscelus/dracykeiton-ren
##  
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##  
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from dracykeiton.compat import *
import renpy
from dracykeiton.util import curry

class Function(renpy.ui.Action):
    "Like default Ren'Py Function, to use in .py files"
    def __init__(self, f, *args, **kw_args):
        super(Function, self).__init__()
        self.f = curry.curry(f)(*args, **kw_args)
    def __call__(self):
        r = self.f.__call__()
        renpy.exports.restart_interaction()
        return r
