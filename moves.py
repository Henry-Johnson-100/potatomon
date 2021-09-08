import elemtype as elem


class MoveEffect:
    def __init__(self, magnitude: int = None, stat: str = None, apply_status: str = None, on_self: bool = False):
        self.magnitude = magnitude
        self.stat = stat
        self.apply_status = apply_status
        self.on_self = on_self

    def is_status_applied(self):
        return self.apply_status is not None

    def is_stat_affected(self):
        if self.stat is not None and self.magnitude is not None:
            return self.magnitude != 0
        else:
            return False

    def effects_self(self):
        return self.on_self

    def do_effect(self, target) -> str: ...  # Abstract method


class MoveEffectFlat(MoveEffect):
    def __init__(self, **kwargs):
        MoveEffect.__init__(self, **kwargs)

    def do_effect(self, target):
        target.encounter_stats[self.stat] += self.magnitude
        return f"{target.name}'s {self.stat} changed by {str(self.magnitude)}."


class MoveEffectPercent(MoveEffect):
    def __init__(self, **kwargs):
        MoveEffect.__init__(self, **kwargs)

    def do_effect(self, target):
        percent = float(self.magnitude) / 100.0
        amount = round((percent * target.encounter_stats[self.stat]))
        target.encounter_stats[self.stat] += amount
        return f"{target.name}'s {self.stat} changed by {amount}."


class MoveEffectHealPercent(MoveEffect):
    def __init__(self, **kwargs):
        MoveEffect.__init__(self, **kwargs)

    def do_effect(self, target):
        percent = float(self.magnitude) / 100.0
        amount_to_heal = abs(round(percent * target.stats["max hp"]))
        target.gain_health(amount_to_heal)
        return f"{target.name} heals for {amount_to_heal}."


class Move:
    def __init__(self, name: str, pp: int, power: int, elem_type: elem.ElemType, is_special: bool = False, move_effect: MoveEffect = None):
        self.name = name
        self.max_pp = pp
        self.pp = pp
        self.power = power
        self.elem = elem_type
        self.is_special = is_special
        self.move_effect = move_effect

    def get_style(self) -> str:
        if self.is_special:
            return "sp. "
        return ""

    def has_effect(self) -> bool:
        if self.move_effect is not None:
            return True
        return False

    def has_healing_effect(self) -> bool:
        return isinstance(self.move_effect, MoveEffectHealPercent)

    def has_stat_effect(self) -> bool:
        return isinstance(self.move_effect, MoveEffectFlat) or isinstance(self.move_effect, MoveEffectPercent)

    def is_damage_move(self) -> bool:
        return self.power > 0

    def decr_pp(self) -> None:
        self.pp = self.pp - 1
        if self.pp <= 0:
            self.pp = 0

    def is_usable(self) -> bool:
        if self.pp <= 0:
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, obj) -> bool:
        if not all([hasattr(obj, attr) for attr in dir(self)]):
            return False
        return self.name == obj.name

    def __str__(self) -> str:
        return_str = f"{self.name}    Power: {self.power}    Element: {self.elem}    PP: {self.pp}"
        return return_str


#######################################################################################
#######################################################################################
######################################MAKER############################################


class Zetsubou(Move):
    """Lowers speed of target and inflicts sp. damage"""

    def __init__(self):
        Move.__init__(self, "Zetsubou", 10, 30, elem.MAKER, is_special=True,
                      move_effect=MoveEffectPercent(stat="spd", magnitude=-20))


class Dig(Move):
    """Inflicts damage"""

    def __init__(self):
        Move.__init__(self, "Dig", 15, 40, elem.MAKER,
                      is_special=False, move_effect=None)


class DrawMap(Move):
    """Greatly raises speed of self"""

    def __init__(self):
        Move.__init__(self, "Draw Map", 10, 0, elem.MAKER, is_special=False,
                      move_effect=MoveEffectPercent(stat="spd", magnitude=50, on_self=True))


class Demolition(Move):
    """Inflicts sp. damage"""

    def __init__(self):
        Move.__init__(self, "Demolition", 5, 75,
                      elem.MAKER, is_special=True, move_effect=None)

######################################DOER##############################################


class FaceSqueeze(Move):
    """Lowers defense of target and inflicts damage"""

    def __init__(self):
        Move.__init__(self, "Face Squeeze", 15, 40, elem.DOER, is_special=False,
                      move_effect=MoveEffectPercent(stat="def", magnitude=-15))


class Koneru(Move):
    """Inflicts sp. damage"""

    def __init__(self):
        Move.__init__(self, "Koneru", 10, 30, elem.DOER,
                      is_special=True, move_effect=None)


class Snowball(Move):
    """Raises sp. def of target and inflicts damage"""

    def __init__(self):
        Move.__init__(self, "Snowball", 10, 50, elem.DOER, is_special=False,
                      move_effect=MoveEffectPercent(stat="sp. def", magnitude=10))


class Kettenkrad(Move):
    """Inflicts damage"""

    def __init__(self):
        Move.__init__(self, "Kettenkrad", 5, 75, elem.DOER,
                      is_special=False, move_effect=None)


######################################MOVER##########################################


class BookBurn(Move):
    """Inflicts sp. damage"""

    def __init__(self):
        Move.__init__(self, "Book Burn", 10, 50, elem.MOVER,
                      is_special=True, move_effect=None)


class Tackle(Move):
    """Inflicts damage"""

    def __init__(self):
        Move.__init__(self, "Tackle", 25, 20, elem.MOVER,
                      is_special=False, move_effect=None)


class EatRation(Move):
    """Heals self"""

    def __init__(self):
        Move.__init__(self, "Eat Ration", 5, 0, elem.MOVER,
                      is_special=False, move_effect=MoveEffectHealPercent(magnitude=50, on_self=True))


class Hug(Move):
    """Raises sp. def of self and inflicts damage on target"""

    def __init__(self):
        Move.__init__(self, "Hug", 10, 40, elem.MOVER, is_special=False, move_effect=MoveEffectPercent(
            stat="sp. def", magnitude=20, on_self=True))


#POTATO_MASH = Move()

#STEAL_RATION = Move()


if __name__ == "__main__":
    print(Hug())
