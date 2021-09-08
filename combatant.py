import potato
import menuinterface
import random
import math
import npc


class Combatant:
    def __init__(self, combatant_potato: potato.Potato, target_potato: potato.Potato, no_menu: bool = False):
        self.actor = combatant_potato
        self.is_temp_disabled = False
        self.is_fleeing = False
        self.target = target_potato
        self.actor.init_at_encounter()
        if not no_menu:
            self.encounter_menu = EncounterMenu(
                combatant_potato, target_potato)
        self.__action_options = ["FIGHT", "RUN"]

    def turn(self):
        self.encounter_menu.clear_text()
        self.encounter_menu.update_menu()
        if not self.is_disabled():
            self.encounter_menu.write_line(f"It is {self.actor.name}'s turn.")
            self.encounter_menu.write_line("")
            self.__choose_action()
        else:
            self.encounter_menu.write_line(
                f"{self.actor.name} cannot act this turn!")
            self.encounter_menu.update_menu()
        self.encounter_menu.prompt_for_continue()

    def __choose_action(self):
        action = self.encounter_menu.choose_from_list(self.__action_options)
        if action == "FIGHT":
            self.__fight()
        elif action == "RUN":
            self.__run()

    def __fight(self):
        self.encounter_menu.clear_text()
        self.encounter_menu.write_line("")
        move_to_perform = self.encounter_menu.choose_from_list(
            self.get_move_list())
        move_effects_list = self.do_move(move_to_perform)
        self.encounter_menu.write_lines(move_effects_list)

    def __run(self):
        self.encounter_menu.clear_text()
        self.__set_is_fleeing()
        self.encounter_menu.write_line(f"{self.actor.name} is fleeing!")

    def is_fainted(self) -> bool:
        return self.actor.is_fainted()

    def is_disabled(self) -> bool:
        """:
            Return True if the actor cannot perform an action for some given turn.
            Define cases where an actor may be unable to move.
            Returns:
                bool: True if the actor cannot perform an action for some given turn.
            """
        if self.is_fainted():
            return True
        if self.is_temp_disabled:
            self.is_temp_disabled = False
            return True
        return False

    def get_move_list(self):
        return self.actor.moves.__iter__()

    # Probably return a flavor text string
    def do_move(self, move: potato.moves.Move) -> list[str]:
        atk_damage = self.__get_attack_damage(move)
        additional_effects = self.__do_additional_move_effects(move)
        move_use_str = f"{self.actor.name} uses {move.name}."
        atk_damage_str = f"It hits for {atk_damage} damage."
        is_super_effective = str()
        if self.target.elem.is_weak_to(move.elem):
            is_super_effective = "It's super effective!"
        self.target.lose_health(atk_damage)
        move.decr_pp()
        return ["", move_use_str, atk_damage_str, is_super_effective, additional_effects, ""]

    def __get_attack_damage(self, move: potato.moves.Move) -> int:
        style = (f"{move.get_style()}atk", f"{move.get_style()}def")
        actor_atk = self.actor.stats[style[0]]
        target_def = self.target.stats[style[1]]
        dmg = math.ceil(move.power * (actor_atk / 100))
        if self.target.elem.is_weak_to(move.elem):
            dmg = math.ceil(dmg * 1.5)
        dmg = math.ceil(dmg - (target_def / 100))
        if dmg < 1 and move.is_damage_move():
            dmg = 1
        if not move.is_damage_move():
            dmg = 0
        return dmg

    def __do_additional_move_effects(self, move: potato.moves.Move) -> str:
        effects_string = str()
        if move.has_effect():
            if move.move_effect.effects_self():
                effects_string = move.move_effect.do_effect(self.actor)
            else:
                effects_string = move.move_effect.do_effect(self.target)
        return effects_string

    def __set_is_fleeing(self) -> None:
        self.is_fleeing = True


class NPCCombatant(Combatant):
    def __init__(self, combatant_potato: potato.Potato, target_potato: potato.Potato):
        Combatant.__init__(self, combatant_potato, target_potato, no_menu=True)
        self.encounter_menu = EncounterMenu(
            protagonist_potato=target_potato, target_potato=combatant_potato)

    def turn(self):
        self.encounter_menu.clear_text()
        self.encounter_menu.update_menu()
        if not self.is_disabled():
            self.encounter_menu.write_line(f"It is {self.actor.name}'s turn.")
            self.encounter_menu.write_line("")
            self.__choose_action()
        else:
            self.encounter_menu.write_line(
                f"{self.actor.name} cannot act this turn!")
            self.encounter_menu.update_menu()
        self.encounter_menu.prompt_for_continue()

    def __choose_action(self):
        if self.__will_flee():
            self.__run()
        else:
            self.__fight()

    def __fight(self):
        self.encounter_menu.clear_text()
        self.encounter_menu.write_line("")
        move_to_perform = self.actor.moves[npc.choose_from_probabilities(
            self.__calculate_move_probabilities())]
        move_effects_list = self.do_move(move_to_perform)
        self.encounter_menu.write_lines(move_effects_list)

    def __run(self):
        self.encounter_menu.clear_text()
        self.__set_is_fleeing()
        self.encounter_menu.write_line(f"{self.actor.name} is fleeing!")

    def __will_flee(self) -> bool:
        return random.random() < self.__calculate_fleeing_probability()

    def __calculate_fleeing_probability(self) -> float:
        """:
            Calculate fleeing probability based on some factors like target level.

            Returns:
                float: probability where 1 and above is 100% and 0 and below is 0%
            """
        prob = (self.target.stats["level"] - self.actor.stats["level"]) / 10
        return prob

    def __calculate_move_probabilities(self) -> list[float]:
        return [self.__calculate_single_move_probabilities(move) for move in self.actor.moves.__iter__()]

    def __calculate_single_move_probabilities(self, move: potato.moves.Move) -> float:
        """:
            Return probability of a single move being chosen.

            Args:
                move (potato.moves.Move): A Move object

            Returns:
                float: 0 means will not be chosen, 1 means will be chosen
            """
        prob = float()
        prob += self.__calculate_damage_move_probability(move)
        prob += self.__calculate_additional_effect_probability(move)
        return prob

    def __calculate_damage_move_probability(self, move: potato.moves.Move) -> float:
        if not move.is_damage_move():
            return 0.0
        prob = float(move.power / 200)
        if move.pp < (move.max_pp * 0.25):
            prob = prob / 2
        if self.target.elem.is_weak_to(move.elem):
            prob *= 3
        if self.actor.encounter_stats["atk"] >= self.actor.encounter_stats["sp. atk"] and not move.is_special:
            prob *= 2
        elif self.actor.encounter_stats["sp. atk"] >= self.actor.encounter_stats["atk"] and move.is_special:
            prob *= 2
        return prob

    def __calculate_additional_effect_probability(self, move: potato.moves.Move) -> float:
        if not move.has_effect():
            return 0.0
        prob = float()
        if move.has_healing_effect():
            prob += self.__calculate_healing_effect_probability(move)
        if move.move_effect.is_status_applied():
            prob += self.__calculate_applied_status_probability(move)
        if move.has_stat_effect():
            prob += self.__calculate_stat_effect_probability(move)
        return prob

    def __calculate_stat_effect_probability(self, move: potato.moves.Move) -> float:
        prob = float()
        stat_change_fraction = float()
        stat_change_target: potato.Potato = self.__get_move_effect_target(move)
        if isinstance(move.move_effect, potato.moves.MoveEffectPercent):
            stat_change_fraction = move.move_effect.magnitude / 100
        else:
            stat_change_fraction = move.move_effect.magnitude / \
                stat_change_target.encounter_stats[move.move_effect.stat]
        prob = stat_change_fraction / \
            ((stat_change_target.encounter_stats[move.move_effect.stat] /
             stat_change_target.stats[move.move_effect.stat]) * 0.5)
        prob *= -1  # So negative stat changes are advantageous to use
        if move.move_effect.effects_self():
            prob *= -1  # So negative stat changes on self are not advantageous
        return prob

    def __calculate_applied_status_probability(self, move: potato.moves.Move) -> float:
        prob = float()
        status_target: potato.Potato = self.__get_move_effect_target(move)
        if not status_target.has_status_effect():
            prob += 0.333
        if move.move_effect.effects_self():
            prob *= -1
        return prob

    def __calculate_healing_effect_probability(self, move: potato.moves.Move) -> float:
        if not move.has_healing_effect():
            return 0.0
        prob = float()
        hp_fraction = self.actor.hp / self.actor.encounter_stats["max hp"]
        if hp_fraction < 0.5:
            prob = 1 - hp_fraction
        fraction_total_health_healed = float()
        if isinstance(move.move_effect, potato.moves.MoveEffectHealPercent):
            fraction_total_health_healed = move.move_effect.magnitude / 100.0
        # No idea how this tuning would work out
        prob *= fraction_total_health_healed
        if not move.move_effect.effects_self():
            # Reverses the probability if the move is intended to heal the enemy for some reason, probably will have to change this at some point, in the event double battles get added
            prob *= -1
        return prob

    # TODO Not tuned right, gives too small floats
    def __health_percent_exponential_fraction(self, heal_fraction) -> float:
        a = 5.8
        def exponential(x): return math.pow(x, a)
        return exponential(heal_fraction) / exponential(1.0)

    def __get_move_effect_target(self, move: potato.moves.Move) -> potato.Potato:
        if move.move_effect.effects_self():
            return self.actor
        return self.target


class EncounterMenu(menuinterface.Menu):
    def __init__(self, protagonist_potato: potato.Potato, target_potato: potato.Potato):
        menuinterface.Menu.__init__(self)
        self.write_line(target_potato, length_to_pad_front=50)
        self.write_line("")
        self.write_line("")
        self.write_line("")
        self.write_line(protagonist_potato)
        self.write_line("")
        self.staticise()
