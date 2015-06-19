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
    from dracykeiton.ui.battleuimanager import BattleUIManager
    from dracykeiton.tb.turnman import LockableTurnman
    from dracykeiton.action import SimpleEffectProcessor
    from visual import VisualTurnman
    from dracykeiton.proxyentity import ProxyEntity, CachedEntity
    from dracykeiton.interpolate import InterpolatingCache
    from dracykeiton.common.sandbox.goblin import Goblin, GoblinLeader
    from dracykeiton.common import LivingEntity, KindEntity
    from dracykeiton.ai.sandbox.battleai import AIBattleController
    from dracykeiton.tb.encounter import Encounter
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    Goblin.global_mod(NamedGoblin)
    
    class VisualEntity(Entity):
        @unbound
        def _init(self):
            self.req_mod(KindEntity)
            self.dynamic_property('image')
            self.dynamic_property('visual_state', 'default')
            self.add_get_node('image', self.get_image())
        
        @simplenode
        def get_image(self, value):
            if not value:
                if not self.kind:
                    return None
                return self.kind + ' ' + self.visual_state
            return value
    
    class VisualDyingEntity(Entity):
        @unbound
        def _init(self):
            self.req_mod(VisualEntity)
            self.req_mod(LivingEntity)
            self.add_get_node('visual_state', self.check_if_dead())
        
        @simplenode
        def check_if_dead(self, value):
            if self.living == 'dead':
                return 'dead'
            else:
                return value
    Goblin.global_mod(VisualDyingEntity)
    
    class ProxyGoblin(Entity):
        @unbound
        def _init(self):
            self.req_mod(ProxyEntity)
            self.req_mod(InterpolatingCache, 1)
            self.cache_interpolate_float('hp', renpy.atl.warpers['linear'])
    
    class EntityText(Text):
        def __init__(self, proxy, text, *args, **kwargs):
            self.proxy = proxy
            self.entity_text = text
            t = self.entity_text.format(self.proxy)
            super(EntityText, self).__init__(t, *args, **kwargs)
        def render(self, width, height, st, at):
            r = self.proxy.tick(st)
            self.st = st
            if r:
                t = self.entity_text.format(self.proxy)
                self.set_text(t)
                renpy.display.render.redraw(self, 0)
            return super(EntityText, self).render(width, height, st, at)
    
    class EntityValue(BarValue):
        def __init__(self, entity, name, range):
            self.entity = entity
            self.name = name
            self.adjustment = None
            self.range = range
        
        def get_adjustment(self):
            self.adjustment = ui.adjustment(value=self.value(), range=self.range, adjustable=False)
            return self.adjustment
        
        def value(self):
            return getattr(self.entity, self.name)
        
        def periodic(self, st):
            r = self.entity.tick(st)
            self.adjustment.change(self.value())
            if r:
                return 0
            return None
    
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

screen battle(manager):
    $ turnman = manager.turnman
    frame:
        has vbox
        grid 2 1:
            xfill True
            frame:
                xalign 0.0
                has vbox
                label "left"
                use battle_side(manager, turnman.world.sides['left'])
            frame:
                xalign 1.0
                has vbox
                label "right"
                use battle_side(manager, turnman.world.sides['right'])
        button:
            yalign 1.0
            label "end turn"
            action UFunction(manager.end_turn)

screen battle_side(manager, side):
    default proxies = {}
    frame:
        has vbox
        for entity in side.members:
            if not entity in proxies:
                $ proxy = ProxyEntity(entity)
                $ proxy.req_mod(ProxyGoblin)
                $ proxies[entity] = proxy
            else:
                $ proxy = proxies[entity]
            button:
                vbox:
                    label proxy.name text_bold (proxy == manager.selected)
                    add EntityText(proxy, "hp {0.hp:.0f}/{0.maxhp:.0f}")
                    bar value EntityValue(proxy, 'hp', proxy.maxhp)
                    label "ap {}/{}".format(proxy.ap, proxy.maxap)
                    if proxy.image:
                        add proxy.image
                
                action UFunction(manager.clicked, side, proxy)
