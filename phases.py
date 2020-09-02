import BoardState
import random
import math

class Build:
    def __init__(self, game): # game.turn_state, etc.
        pass

    def build_unit(self, territory, unit_index): #called by the AI
        pass


class Combat_Move:
    pass

    def battle_calculator(self):
    #MAKE A COPY OF STUFF BEFORE YOU USE THIS BC THE BATTLE STUFF ACTUALLY MAKES CHANGES
    #account for land units on transpots in ipc swing
    # tool for the AI to determine how a battle WOULD turn out without actually changing the GameState
        pass

class Battles:
    def __init__(self, game):
        self.territory_states = game.state_dict
        self.player = game.turn_state.player
        self.team = game.rules.teams[player]
        self.game = game

        self.enemy_team = game.rules.teams[player]
        while (self.enemy_team == game.rules.teams[player]):
            for country in self.game.rules.teams:
                if country != "Neutral":
                    self.enemy_team = game.rules.teams[country]
                else:
                    pass
        # sets enemy team to opposite team.

        for territory_key in territory_states:
            territory_states[territory_key] = territory_state
            territory_state.unit_state_list = unit_state_list

            #TODO Account for submarine submerge option

            if embattled (unit_state_list):
                #if two different team's units are in a territory at the end of combat move
                unit_state_list = battler(unit_state_list)  #resets unit_state_list to be equal to the remaining units
            else:
                pass

    def battler(self, unit_state_list):
    # inputs units (unit_states) originally in embattled territory and returns remaining units

        while embattled(unit_state_list):

            total_friendly_power = 0
            total_enemy_power = 0

            #TODO Account for AA gun shots

            for unit_state in unit_state_list:
                    if self.game.rules.teams[unit_state.owner] == self.team:
                        #assume offense for current player
                        total_friendly_power += self.game.rules.units[unit_state.type_index].attack  #I think this path works...
                    else:
                        total_enemy_power += self.game.rules.units[unit_state.type_index].defense

            friendly_units_killed = hit_roller(total_friendly_power % 6) + math.floor(total_friendly_power / 6)
            enemy_units_killed = hit_roller(total_enemy_power % 6) + math.floor(total_enemy_power / 6)

            casualty_selector(self.team, unit_state_list, attack, friendly_units_killed)
            casualty_selector(self.enemy_team, unit_state_list, defense, enemy_units_killed)
            #these modify unit_state_list

        return unit_state_list

    def embattled(self, unit_state_list):
        for unit_state in unit_state_list:
            if self.game.rules.teams[unit_state.owner] != self.team:
                return True
        else:
            return False

    def hit_roller(self, power):
        roll = random.randint(1, 6)
        if roll <= power:
            return 1
        else:
            return 0

    def casualty_selector(self, unit_state_list, attack_or_defense, casualty_count, \
    one_land_unit_remaining = False, prioritize_unit_index = -1):
        friendly_units = []

        for unit_state in unit_state_list:
            if self.game.rules.teams[unit_state.owner] == self.team:
                friendly_units.append(unit_state)

        #check if can simply wipe the list
        if casualty_count >= len(friendly_units):
            for unit_state in friendly_units:
                unit_state_list.remove(unit_state)

        #saving list keeps caviats if set to True
        saving_list = []
        if one_land_unit_remaining:
            highest_cost = 0
            for unit_state in friendly_units:
                 if self.game.rules.units[unit_state.type_index].cost >= highest_cost \
                 and self.game.rules.units[unit_state.type_index].unit_type == "land":
                    highest_cost = self.game.rules.units[unit_state.type_index].cost
            for unit_state in friendly_units:
                 if self.game.rules.units[unit_state.type_index].cost == highest_cost \
                 and self.game.rules.units[unit_state.type_index].unit_type == "land":
                    saving_list.append(unit_state)
                    friendly_units.remove(unit_state)

        #will likely be either planes for defensive retreat, subs for submerge ability, or bombers on defense
        if prioritize_unit_index != -1:
            for unit_state in friendly_units:
                if unit_state.type_index == prioritize_unit_index:
                    saving_list.append(unit_state)
                    friendly_units.remove(unit_state)

        #TODO CHECK IF THIS GOES INFINITE
        while casualty_count > 0:

            #choose based on power
            lowest_power = 6
            for unit_state in friendly_units:
                if self.game.rules.units[unit_state.type_index].attack_or_defense <= lowest_power:
                    lowest_power = self.game.rules.units[unit_state.type_index].attack_or_defense
            lowest_power_list = []
            for unit_state in friendly_units:
                if self.game.rules.units[unit_state.type_index].attack_or_defense == lowest_power:
                    lowest_power_list.append(unit_state)

            #two while loops allows us to remove redundant use of lowest_power
            while lowest_power_list != []:

                #then choose based on cost
                lowest_cost = 1000
                for unit_state in lowest_power_list:
                    if self.game.rules.units[unit_state.type_index].cost <= lowest_cost:
                        lowest_cost = self.game.rules.units[unit_state.type_index].cost

                #delete units
                for unit_state in lowest_power_list:
                    if self.game.rules.units[unit_state.type_index].cost == lowest_cost:
                        unit_state_list.remove(unit_state)    # to change the master list
                        friendly_units.remove(unit_state)     # for the while loop
                        lowest_power_list.remove(unit_state)  # for the while loop
                        casualty_count = casualty_count - 1

            if friendly_units == []:
                break








class Non_Combat:
    pass

class Place:
    pass

class Cleanup:
    pass
