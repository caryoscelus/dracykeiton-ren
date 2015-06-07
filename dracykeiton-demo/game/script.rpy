init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController
    from entity import Entity
    from controller import ProxyController
    import classpatch
    
    class NamedGoblin(Entity):
        @unbound
        def _init(self):
            self.dynamic_property('name')
            if not self.name:
                self.name = 'Goblin'
    classpatch.register(Goblin, 'mod', NamedGoblin)
    
    class UserController(ProxyController):
        pass
    
    class BattleUIManager(object):
        # We expect two-side battle with only one side controlled by user!
        def __init__(self, turnman):
            super(BattleUIManager, self).__init__()
            self.turnman = turnman
            self.selected = None
            self.user_controller = [s for s in self.turnman.sides if isinstance(s, UserController)][0]
        
        def clicked(self, side, entity):
            # TODO: ugh, fix this
            controller = [s for s in self.turnman.sides if tuple(s.entities)[0] == side][0]
            if isinstance(controller, UserController):
                self.select(entity)
            else:
                self.attack(entity)
        
        def select(self, entity):
            self.selected = entity
        
        def attack(self, entity):
            if not self.selected:
                return
            if self.selected.living != 'alive':
                self.selected = None
                return
            action = self.selected.hit(entity)
            if action:
                self.do_action(action)
        
        def do_action(self, action):
            self.user_controller.do_action(action)
            self.turnman.turn()
        
        def end_turn(self):
            self.user_controller.end_turn()
            self.turnman.turn()
            self.turnman.turn()

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
