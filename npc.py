import random
from typing import Any

# Not really a fan of this because of all the list operations
def choose_from_probabilities(prob_list: list[float]) -> int:
    choose_list = normalize_probabilities(prob_list)
    roll_list = [random.random() for x in choose_list]
    roll_list = __construct_passing_rolls(choose_list, roll_list)
    for i in range(0, len(choose_list)):
        if roll_list[i] is not None:
            if roll_list[i] == max_with_nonetypes(roll_list):
                return i
    if all([x is None for x in roll_list]):
        return 0
    else:
        return max_with_nonetypes(roll_list)

    return prob_list.index(max(prob_list))

def max_with_nonetypes(search_list: list[Any]) -> Any:
    return max(list(filter(lambda x: x is not None, search_list)))

def __construct_passing_rolls(choose_list: list[float], roll_list: list[float]) -> list[float]:
    __roll_list = roll_list.copy()
    for i in range(0, len(choose_list)):
        if choose_list[i] == 0:
            __roll_list[i] = None
        else:
            relative_roll = roll_list[i] / choose_list[i]
            if relative_roll < 1:
                __roll_list[i] = relative_roll
            else: __roll_list[i] = None
    return __roll_list


def rectify_probability(probability: float) -> float:
    """:
        Guarantees that a probability float is between 0 and 1 by truncating any values that fall outside of those bounds

        Returns: A float between 0.0 and 1.0
        """
    if probability > 1:
        return 1.0
    elif probability < 0:
        return 0.0
    return probability


def normalize_probabilities(prob_list: list[float]) -> list[float]:
    normal_list = prob_list.copy()
    minimum = min(normal_list)
    if minimum > 0:
        minimum *= -1
    normal_list = [x + minimum for x in normal_list]
    maximum = max(normal_list)
    normal_list = [x / maximum for x in normal_list]
    return normal_list


class EncounterNPC:
    def __init__(self):
        pass


class OverworldNPC:
    pass


class NPC:
    """A class defining npc behavior, should be able to interface with other classes and menus but
    But can not and should not be represented as any entity by itself.
    """

    def __init__(self, encounter_npc: EncounterNPC):
        self.encounter_npc = encounter_npc
