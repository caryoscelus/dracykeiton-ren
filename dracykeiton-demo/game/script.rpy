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

init python:
    from dracykeiton.compat import *
    from dracykeiton.entity import Entity, simplenode
    from dracykeiton.tb.controller import UserController
    from dracykeiton.ui.battleuimanager import BattleUIManager, SingleAllyAction, SingleEnemyAction, BattleUIHints
    from dracykeiton.tb.turnman import LockableTurnman
    from dracykeiton.action import SimpleEffectProcessor
    from dracykeiton.proxyentity import ProxyEntity, CachedEntity
    from dracykeiton.interpolate import InterpolatingCache
    from dracykeiton.common.sandbox.goblin import Goblin, GoblinLeader
    from dracykeiton.ai.sandbox.battleai import AIBattleController
    from dracykeiton.tb.encounter import Encounter
    from visual import VisualTurnman, VisualDyingEntity, ProxyGoblin
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    Goblin.global_mod(NamedGoblin)
    
    Goblin.global_mod(VisualDyingEntity)
    
    class GoblinUIHints(Entity):
        @unbound
        def _init(self):
            self.req_mod(BattleUIHints)
            self.ui_action('battle', self.hit)
    Goblin.global_mod(GoblinUIHints)
    
    class GoblinLeaderUIHints(Entity):
        @unbound
        def _init(self):
            self.req_mod(BattleUIHints)
            self.ui_action('battle', self.inspire)
    GoblinLeader.global_mod(GoblinLeaderUIHints)
    
    def prepare_battle(left_c, right_c, turnman, keep_dead=False):
        """Prepare battle with given side controllers"""
        encounter = Encounter(turnman, keep_dead=keep_dead)
        encounter.add_side('left', left_c, 2, predefined=[Goblin(), GoblinLeader()])
        encounter.add_side('right', right_c, 3, predefined=[Goblin(), Goblin(), Goblin()])
        return encounter.generate()

label main_menu:
    return

label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle(UserController, AIBattleController, VisualTurnman, True)
    $ manager = BattleUIManager(battle)
    $ manager.start()
    $ renpy.save('test')
    call screen battle(manager)
    return
