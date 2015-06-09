init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController, KindEntity
    from entity import Entity, simplenode
    from controller import UserController
    from battleuimanager import BattleUIManager
    from turnman import Turnman
    from action import SimpleEffectProcessor
    import classpatch
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    classpatch.register(Goblin, 'mod', NamedGoblin)
    
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
                return self.kind + ' ' + self.visual_state
    classpatch.register(Goblin, 'mod', VisualEntity)
    
    class VisualTurnman(Turnman, SimpleEffectProcessor):
        def __init__(self, *args, **kwargs):
            super(VisualTurnman, self).__init__(*args, **kwargs)
            self.add_effect('hit', self.hit_effect)
        
        def hit_effect(self, action):
            (attacker, attacked) = action.args
            attacker.visual_state = 'attack'
            attacked.visual_state = 'attacked'

label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle(UserController, AIBattleController, VisualTurnman)
    $ battle.start()
    $ manager = BattleUIManager(battle)
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
    frame:
        has vbox
        for entity in side.members:
            button:
                vbox:
                    label entity.name
                    label "hp {}/{}".format(entity.hp, entity.maxhp)
                    label "ap {}/{}".format(entity.ap, entity.maxap)
                    add entity.image
                
                action UFunction(manager.clicked, side, entity)
