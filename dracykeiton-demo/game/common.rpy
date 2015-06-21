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
    class EntityText(Text):
        def __init__(self, proxy, text, *args, **kwargs):
            self.proxy = proxy
            self.entity_text = text
            t = self.entity_text.format(self.proxy)
            super(EntityText, self).__init__(t, *args, **kwargs)
        def render(self, width, height, st, at):
            try:
                r = self.proxy.tick(st)
            except AttributeError:
                r = False
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
            try:
                r = self.entity.tick(st)
            except AttributeError:
                r = False
            self.adjustment.change(self.value())
            if r:
                return 0
            return None