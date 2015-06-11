init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController, KindEntity
    from entity import Entity, simplenode
    from controller import UserController
    from battleuimanager import BattleUIManager
    from turnman import LockableTurnman
    from action import SimpleEffectProcessor
    from visual import VisualTurnman
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
                if not self.kind:
                    return None
                return self.kind + ' ' + self.visual_state
    classpatch.register(Goblin, 'mod', VisualEntity)

label main_menu:
    return

label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle(UserController, AIBattleController, VisualTurnman, True)
    $ battle.start()
    $ manager = BattleUIManager(battle)
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
    frame:
        has vbox
        for entity in side.members:
            button:
                vbox:
                    label entity.name
                    label "hp {}/{}".format(entity.hp, entity.maxhp)
                    label "ap {}/{}".format(entity.ap, entity.maxap)
                    if entity.image:
                        add entity.image
                
                action UFunction(manager.clicked, side, entity)
