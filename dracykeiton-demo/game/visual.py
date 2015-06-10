from compat import *
from util import UFunction
from turnman import LockableTurnman
from action import SimpleEffectProcessor
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
