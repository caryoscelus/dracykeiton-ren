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
            action Function(manager.end_turn)
        label "{}".format(str(manager.turnman.world.state).replace('[', '').replace(']', ''))
        if manager.can_finish():
            button:
                yalign 1.0
                label "end encounter"
                action [Function(manager.end_encounter), Return()]

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
                hbox:
                    if proxy.image:
                        add proxy.image
                    vbox:
                        label proxy.name text_bold (proxy == manager.selected)
                        hbox:
                            for act in manager.get_actions(proxy, 'battle'):
                                textbutton act.name action Function(manager.select_action, act)
                        add EntityText(proxy, "xp {0.xp:.0f} level {0.level:.0f}")
                        hbox:
                            add EntityText(proxy, "hp {0.hp:.0f}/{0.maxhp:.0f}")
                            bar value EntityValue(proxy, 'hp', proxy.maxhp)
                        label "ap {}/{}".format(proxy.ap, proxy.maxap)
                
                action Function(manager.clicked, side, proxy)
