init python:
    from compat import *
    from test_battle import prepare_battle, Goblin, AIBattleController, KindEntity
    from entity import Entity, simplenode
    from controller import UserController
    from battleuimanager import BattleUIManager
    from turnman import LockableTurnman
    from action import SimpleEffectProcessor
    from visual import VisualTurnman
    from proxyentity import ProxyEntity, CachedEntity
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
    
    class VisualDyingEntity(Entity):
        @unbound
        def _init(self):
            self.req_mod(VisualEntity)
            self.add_get_node('visual_state', self.check_if_dead())
        
        @simplenode
        def check_if_dead(self, value):
            if self.living == 'dead':
                return 'dead'
            else:
                return value
    classpatch.register(Goblin, 'mod', VisualDyingEntity)
    
    class InterpolatingCache(Entity):
        @unbound
        def _init(self, delay=1.0):
            self.req_mod(ProxyEntity)
            self.req_mod(CachedEntity)
        
        @unbound
        def cache_interpolate_float(self, name, f):
            self.proxy_listen(name)
            self.cache_property(name, self.update)
            self.update_cache(name, 'progress', 1)
        
        @unbound
        def update(self, name, old_value, value):
            self.update_cache(name, 'progress', 0)
        
        @unbound
        def tick(self, time):
            rs = None
            for name in self._property_cache:
                r = self.update_property(name, time)
                rs = rs or r
            return rs
        
        @unbound
        def update_property(self, name, time):
            pr = self.cached(name, 'progress')
            if pr >= 1:
                return None
            pr = min(1, pr+time)
            self.update_cache(name, 'progress', pr)
            self.update_cache(name, 'current', self.cached(name, 'old')*(1-pr)+self.cached(name, 'new')*pr)
            self.notify_listeners(name)
            return True
    
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
            self.st = None
            super(EntityText, self).__init__(t, *args, **kwargs)
        def render(self, width, height, st, at):
            if self.st is None:
                self.st = st
            r = self.proxy.tick(st-self.st)
            self.st = st
            if r:
                t = self.entity_text.format(self.proxy)
                self.set_text(t)
                renpy.display.render.redraw(self, 0)
            return super(EntityText, self).render(width, height, st, at)

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

init python:
    def updateProxies(proxies, delay):
        for proxy in proxies.values():
            proxy.tick(delay)

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
                    label proxy.name
                    add EntityText(proxy, "hp {0.hp:.0f}/{0.maxhp:.0f}")
                    label "ap {}/{}".format(proxy.ap, proxy.maxap)
                    if proxy.image:
                        add proxy.image
                
                action UFunction(manager.clicked, side, entity)
