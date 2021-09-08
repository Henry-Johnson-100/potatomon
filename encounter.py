import potato
import combatant

TURN_OPTIONS = ["fight", "run"]


class Encounter:
    def __init__(self, combatant_a: potato.Potato, combatant_b: potato.Potato):
        self.combatant_a = self.__construct_combatant(combatant_a, combatant_b)
        self.combatant_b = self.__construct_combatant(combatant_b, combatant_a)
        self.__battle()

    def __battle(self) -> None:
        while self.__is_ongoing_encounter():
            self.__turn()

    def __turn(self) -> None:
        priority, subordinate = self.__get_turn_order()
        priority.turn()
        subordinate.turn()

    def __is_ongoing_encounter(self) -> bool:
        """:
            Return True if the encounter can continue for the next turn.
            Defines cases where the encounter can't continue.

            Returns:
                bool: True if the encounter can continue for the next turn.
            """
        if any([self.combatant_a.is_fainted(), self.combatant_b.is_fainted()]):
            return False
        if any([self.combatant_a.is_fleeing, self.combatant_b.is_fleeing]):
            return False
        return True

    def __get_turn_order(self) -> tuple[combatant.Combatant, combatant.Combatant]:
        if self.combatant_a.actor.stats["spd"] >= self.combatant_a.target.stats["spd"]:
            return (self.combatant_a, self.combatant_b)
        return (self.combatant_b, self.combatant_a)

    def __construct_combatant(self, potato_a: potato.Potato, potato_b: potato.Potato) -> combatant.Combatant:
        if potato_a.is_npc:
            return combatant.NPCCombatant(potato_a, potato_b)
        return combatant.Combatant(potato_a, potato_b)


if __name__ == "__main__":
    chi = potato.Chito()
    yuu = potato.Yuuri()
    chi.set_npc(True)
    enc = Encounter(yuu, chi)
