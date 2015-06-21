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
from dracykeiton.entity import Entity, simplenode
from dracykeiton.common import LivingEntity, KindEntity
from dracykeiton.proxyentity import ProxyEntity
from dracykeiton.interpolate import InterpolatingCache
import renpy

class VisualTurnman(LockableTurnman, SimpleEffectProcessor):
    def __init__(self, *args, **kwargs):
        super(VisualTurnman, self).__init__(*args, **kwargs)
    
    def init_effects(self):
        super(VisualTurnman, self).init_effects()
        self.add_effect('hit', self.hit_effect)
    
    def hit_effect(self, action):
        args = list(action.args)
        try:
            attacker = action.keywords['self']
        except KeyError:
            attacker = args.pop(0)
        try:
            attacked = action.keywords['enemy']
        except KeyError:
            attacked = args.pop(0)
        attacker.visual_state = 'attack'
        attacked.visual_state = 'attacked'
        self.lock()
        renpy.ui.timer(1, [UFunction(self.hit_uneffect, attacker, attacked), UFunction(self.unlock)])
    
    def hit_uneffect(self, attacker, attacked):
        attacker.visual_state = 'default'
        attacked.visual_state = 'default'

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

class ProxyGoblin(Entity):
    @unbound
    def _init(self):
        self.req_mod(ProxyEntity)
        self.req_mod(InterpolatingCache, 1)
        self.cache_interpolate_float('hp', renpy.atl.warpers['linear'])
