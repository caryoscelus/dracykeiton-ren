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
    from dracykeiton.tb.controller import UserController
    from dracykeiton.ui.battleuimanager import BattleUIManager
    from dracykeiton.tb.turnman import LockableTurnman
    from dracykeiton.action import SimpleEffectProcessor
    from dracykeiton.entity.proxyentity import ProxyEntity, CachedEntity
    from dracykeiton.entity.interpolate import InterpolatingCache
    from dracykeiton.common.battlefield import TwoSideField
    from dracykeiton.common.sandbox.goblin import Goblin, GoblinLeader, GoblinHealer
    from dracykeiton.ai.sandbox.battleai import AIBattleController
    from dracykeiton.tb.battlegen import BattleGen
    from dracykeiton.util import curry
    from visual import VisualTurnman, ProxyGoblin
    import custom_ui
    
    def check_if_dead(e, side):
        return e.living == 'dead'
    
    def check_if_empty(side):
        return side.empty_side()
    
    def next_encounter(pc):
        """Prepare next random encounter with pc"""
        encounter = BattleGen(VisualTurnman, TwoSideField, keep_dead=True)
        encounter.add_side('left', UserController, 3, predefined=[pc], possible=[Goblin, GoblinHealer])
        encounter.add_side('right', AIBattleController, 3, possible=[Goblin, GoblinHealer])
        turnman = encounter.generate()
        turnman.world.add_lose_condition('left', curry.curry(check_if_dead)(pc))
        turnman.world.add_lose_condition('right', curry.curry(check_if_empty)())
        return turnman

label main_menu:
    return

label start:
    "Dracykeiton demo."
    $ pc = GoblinLeader()
    $ pc.xp = 280
label random_encounter_loop:
    $ renpy.block_rollback()
    $ battle = next_encounter(pc)
    $ manager = BattleUIManager(battle)
    $ manager.start()
    $ renpy.save('test')
    call screen battle(manager)
    $ renpy.save('test')
    "Battle is over.."
    jump random_encounter_loop
    return
