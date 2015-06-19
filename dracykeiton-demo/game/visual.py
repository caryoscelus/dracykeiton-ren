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
from util import UFunction
from dracykeiton.tb.turnman import LockableTurnman
from dracykeiton.action import SimpleEffectProcessor
import renpy

class VisualTurnman(LockableTurnman, SimpleEffectProcessor):
    def __init__(self, *args, **kwargs):
        super(VisualTurnman, self).__init__(*args, **kwargs)
        self.add_effect('hit', self.hit_effect)
    
    def hit_effect(self, action):
        (attacker, attacked) = action.args
        attacker.visual_state = 'attack'
        attacked.visual_state = 'attacked'
        self.lock()
        renpy.ui.timer(1, [UFunction(self.hit_uneffect, attacker, attacked), UFunction(self.unlock)])
    
    def hit_uneffect(self, attacker, attacked):
        attacker.visual_state = 'default'
        attacked.visual_state = 'default'
