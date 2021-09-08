import moves
import elemtype as elem
from menuinterface import MenuLine
import random
import npc


class PotatoStats:
    def __init__(self, seed: int = 0):
        self.stats = {  # TODO #default values for now, find some way to seed these or something later
            "level": 1,
            "max hp": 25,
            "req. exp": 500,
            "atk": 10,
            "sp. atk": 10,
            "def": 10,
            "sp. def": 10,
            "spd": 10
        }
        self.__rates = self.__generate_rates(seed)

    def level_up_stats(self):
        for stat_key in self.__iter__():
            if stat_key == "req. exp":
                self.stats[stat_key] *= self.__rates[stat_key]
                continue
            self.stats[stat_key] += self.__rates[stat_key]

    def encounter_copy(self) -> dict:
        return self.stats.copy()

    def __generate_rates(self, seed: int) -> dict:
        rate_dict = dict()
        for stat_key in self.__iter__():
            rate_dict[stat_key] = self.__generate_some_stat_rate(seed)
        # Setting custom values for the level and exp stats since they grow differently compared to the others
        rate_dict["level"] = 1
        # Will be used as a multiplier
        rate_dict["req. exp"] = 2 + random.random()
        return rate_dict

    def __generate_some_stat_rate(self, seed: int) -> int:
        return random.randint(1, 3)

    def __iter__(self) -> set:
        return set(self.stats.keys())

    def __getitem__(self, key) -> int:
        return self.stats[key]


class PotatoMoves:
    def __init__(self, moves: list):
        self.moves = moves[0:4]

    def has_full_move_set(self) -> bool:
        return len(self.moves) >= 4

    def has_move(self, move: moves.Move) -> bool:
        return move in self.moves

    def append_move(self, add_move: moves.Move) -> None:
        self.moves.append(add_move)

    def replace_move(self, remove_move: moves.Move, add_move: moves.Move) -> None:
        if not self.has_move(add_move) and self.has_move(remove_move):
            self.moves.insert(self.moves.index(remove_move), add_move)
            self.moves.remove(remove_move)

    def __iter__(self) -> list:
        return self.moves

    def __getitem__(self, key) -> moves.Move:
        return self.moves[key]

    def __eq__(self, obj) -> bool:
        if not hasattr(obj, "moves"):
            return False
        return self.moves == obj.moves


class Potato:
    def __init__(self, name: str, elem: elem.ElemType, moves: list, level: int = 1, stat_seed: int = 0, is_npc: bool = False):
        self.name = name
        self.elem = elem
        self.moves = PotatoMoves(moves)
        self.stats = PotatoStats(stat_seed)
        self.__appr_level(level)
        self.hp = self.stats["max hp"]
        self.exp = 0
        self.encounter_stats = dict()
        self.is_npc = is_npc
        self.status_effect = None

    def has_status_effect(self) -> bool:
        return self.status_effect is not None

    def set_npc(self, is_npc: bool) -> None:
        self.is_npc = is_npc

    def gain_health(self, amount: int) -> None:
        self.hp = self.hp + amount
        if self.hp > self.stats["max hp"]:
            self.hp = self.stats["max hp"]

    def lose_health(self, amount: int) -> None:
        self.hp = self.hp - amount
        if self.hp <= 0:
            self.hp = 0

    def gain_exp(self, amount: int) -> None:
        self.exp += amount
        if self.exp >= self.stats["req. exp"]:
            self.level_up()

    def is_fainted(self) -> bool:
        return self.hp <= 0

    def init_at_encounter(self) -> None:
        self.encounter_stats = self.stats.encounter_copy()

    def get_disp_health_bar(self) -> str:
        length_of_health_bar = 50
        filled_portion_of_health_bar = round(
            (self.hp / self.stats["max hp"]) * length_of_health_bar)
        health_bar = "".join(["#"] * filled_portion_of_health_bar)
        health_bar = str(
            MenuLine(health_bar, "-", length_to_pad_rear=length_of_health_bar))
        return health_bar

    def level_up(self) -> None:
        self.stats.level_up_stats()
        self.hp = self.stats["max hp"]
        self.exp = 0

    def __appr_level(self, level: int) -> None:
        for i in range(self.stats["level"], (level + 1)):
            self.level_up()

    def __str__(self) -> str:
        total_hp = self.stats["max hp"]
        return f"{self.name} | {self.hp}/{total_hp} {self.get_disp_health_bar()}"


#######################################################################################################

class Chito(Potato):
    def __init__(self):
        Potato.__init__(self, "Chito", elem.DOER, [
                        moves.Kettenkrad(), moves.EatRation(), moves.FaceSqueeze(), moves.Koneru()], 1)


class Yuuri(Potato):
    def __init__(self):
        Potato.__init__(self, "Yuuri", elem.MOVER, [
                        moves.Zetsubou(), moves.Snowball(), moves.BookBurn(), moves.EatRation()], 1)


class Kanazawa(Potato):
    def __init__(self):
        Potato.__init__(self, "Kanazawa", elem.MAKER, [
                        moves.DrawMap(), moves.Demolition(), moves.Zetsubou(), moves.EatRation()], 1)


if __name__ == "__main__":
    # _moves = list()
    # _moves.append(m.Koneru())
    # _moves.append(m.BookBurn())
    # _moves.append(m.Tackle())
    # _moves.append(m.Zetsubou())
    # test = Potato("Yuuri", elem.MOVER, _moves, 1)
    # print(test)
    # print(list(map(print, test.moves)))
    # print(test.is_fainted())
    # print(generate_some_stat_rate())
    # print(test.stats)
    # print(test.total_hp)
    print(Chito())
