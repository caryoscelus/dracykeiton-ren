init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController
    from entity import Entity
    from controller import UserController
    from battleuimanager import BattleUIManager
    import classpatch
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    classpatch.register(Goblin, 'mod', NamedGoblin)


label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle(UserController, AIBattleController)
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
                label "{}".format(entity).replace('{', '').replace('}', '')
                action UFunction(manager.clicked, side, entity)
