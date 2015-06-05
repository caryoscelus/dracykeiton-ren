init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController
    from entity import Entity
    from controller import Controller
    import classpatch
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    classpatch.register(Goblin, 'mod', NamedGoblin)
    
    class UserController(Controller):
        def act(self):
            return False

label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle(AIBattleController, UserController)
    call screen battle(battle)
    return

screen battle(turnman):
    frame:
        has vbox
        grid 2 1:
            xfill True
            frame:
                xalign 0.0
                has vbox
                label "left"
                use battle_side(turnman.sides[0])
            frame:
                xalign 1.0
                has vbox
                label "right"
                use battle_side(turnman.sides[1])
        button:
            yalign 1.0
            label "end turn"
            action UFunction(turnman.turn)

screen battle_side(controller):
    $ world = controller.world
    $ side = tuple(controller.entities)[0]
    frame:
        has vbox
        for unit in side.members:
            label "{}".format(unit).replace('{', '').replace('}', '')
            button:
                label "kill"
                action UFunction(unit.hurt, 5)
