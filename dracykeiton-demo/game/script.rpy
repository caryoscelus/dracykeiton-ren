init python:
    from test_battle import prepare_battle

label start:
    "Dracykeiton demo."
    $ renpy.retain_after_load()
    $ battle = prepare_battle()
    call screen battle(battle)
    return

screen battle(turnman):
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

screen battle_side(side):
    frame:
        has vbox
        for unit in side.entities:
            label "{}".format(unit).replace('{', '').replace('}', '')
            button:
                label "kill"
                action UFunction(unit.hurt, 5)
