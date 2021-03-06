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
from dracykeiton.entity import Entity, simplenode, mod_dep
from dracykeiton.action import action, category
from dracykeiton.ui.battleuimanager import BattleUIHints
from dracykeiton.common.sandbox.goblin import Goblin, GoblinLeader
from dracykeiton.common import Caller, Heal
from visual import VisualDyingEntity
from renpy import exports as renpy

@mod_dep(BattleUIHints)
class CustomizableCharacterUI(Entity):
    @category('always')
    @action
    def char(self):
        renpy.show_screen('customize_character', self)
    
    @unbound
    def can_char(self):
        return True
Goblin.global_mod(CustomizableCharacterUI)

class NamedGoblin(Entity):
    @unbound
    def _init(self):
        self.dynamic_property('name')
        if not self.name:
            self.name = 'Goblin'
Goblin.global_mod(NamedGoblin)

Goblin.global_mod(VisualDyingEntity)
