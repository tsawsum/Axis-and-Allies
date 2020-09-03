import BoardState
import random
import math

class Build:
    def __init__(self, game, endangered_name_list): # game.turn_state, etc.
        self.game = game
        self.player = self.game.turn_state.player
        self.endangered_name_list = endangered_name_list
        game.turn_state.phase = 2
        self.ipc = self.game.turn_state.player.ipc

        self.prioritization_list = []
        self.prioritization_list.append(['tech_token', 0])     #never use this one
        self.prioritization_list.append(['battleship', 0])     #1
        self.prioritization_list.append(['factory', 0])        #2
        self.prioritization_list.append(['carrier', 0])        #3
        self.prioritization_list.append(['cruiser', 0])        #4
        self.prioritization_list.append(['bomber', 0])         #5
        self.prioritization_list.append(['carrier_fighter', 0]) #same here
        self.prioritization_list.append(['fighter', 0])        #7
        self.prioritization_list.append(['destroyer', 0])      #8
        self.prioritization_list.append(['transport', 0])      #9
        self.prioritization_list.append(['transportable_units', 0]) #only positive if no adjacent units
        self.prioritization_list.append(['sub', 0])            #11
        self.prioritization_list.append(['tank', 0])           #12
        self.prioritization_list.append(['aa', 0])             #13
        self.prioritization_list.append(['artillery', 0])      #14
        self.prioritization_list.append(['infantry', 0])       #15

        #sea
        self.sea_defense_sum = self.prioritization_list[1][1] + self.prioritization_list[3][1] \
            + self.prioritization_list[4][1] + self.prioritization_list[6][1] + self.prioritization_list[8][1]
        self.sea_sum = self.sea_defense_sum + self.prioritization_list[9][1] + self.prioritization_list[10][1] \
            + self.prioritization_list[11][1]

        #land. These may prove vistigial
        self.land_defense_sum = self.prioritization_list[12][1] + self.prioritization_list[13][1] \
            + self.prioritization_list[14][1] + self.prioritization_list[15][1] + self.prioritization_list[7][1]
        self.land_sum = self.land_defense_sum + self.prioritization_list[2][1] + self.prioritization_list[5][1]

        self.priority_sum = self.land_sum + self.sea_sum

        self.purchased_unit_state_list = []
        # initial purchasing
        for unit_priority in self.prioritization_list:
            priority_ratio = unit_priority[1]/self.priority_sum
            allotted_ipc = priority_ratio * self.ipc

            cost = -1

            if unit_priority[0] == 'carrier_fighter':
                cost = 10
                num_purchased = round(allotted_ipc/cost)
                for i in range(num_purchased):
                    self.purchased_unit_state_list.append(UnitState(self.player, 11))
                    self.ipc -= cost

            elif unit_priority[0] == 'transportable_units':
                cost = 7
                num_purchased = round(allotted_ipc/cost)
                for i in range(num_purchased):
                    self.purchased_unit_state_list.append(UnitState(self.player, 0))
                    self.purchased_unit_state_list.append(UnitState(self.player, 1))
                    self.ipc -= cost

            else:
                for unit in self.game.rules.units:
                    if unit.name == unit_priority[0]:
                        cost = unit.cost
                        num_purchased = round(allotted_ipc/cost)
                        for i in range(num_purchased):
                            self.purchased_unit_state_list.append(UnitState(self.player, self.game.rules.units.index(unit))
                            self.ipc = self.ipc - cost
                        #TODO WHY does this give an error?

        self.factories = {}
        for territory_key in self.game.state_dict:
            for unit_state in self.game.state_dict[territory_key].unit_state_list:
                if unit_state.type_index == 5:
                    self.factories[territory_key] = self.game.rules.board[territory_key].ipc #name keys to ipc value
        # factories now has a dict of names having factories and their IPC values (max build capacity)

        set_defensive_requirements(endangered_name_list)

    def build_strategy(self):  #called by the AI


        if self.immediate_defensive_requirements != []:     #this will always be land
            self.immediate_defensive_requirements.sort(reverse=True, key=lambda x:game.rules.board[x].ipc)
            for territory_name in self.immediate_defensive_requirements:


                self.land_defense_sum = self.prioritization_list[9][1] + self.prioritization_list[11][1] \
            + self.prioritization_list[12][1] + self.prioritization_list[13][1] + self.prioritization_list[14][1]


        #TODO 1. make sure your defensive requirements are met if possible. If land prioritization is active
        #           utilize specific units if possible. Set low prioritiy if you want to build only tanks in SA
        #     2. If not possible with land prioritization, replace special units with infantry.
        #     3. If still not possible, buy the max amount of infantry and prioritize based on territory ipc value
        #     4. If sea territory must be held, repeat above process with carriers as fallback defense if planes in
        #           range, otherwise cruisers.
        #     5. Order active prioritizations from highest to lowest
        #     6. Allocate IPC according to the ratio of prioritizations. For example, prioritize_subs = 2
        #           prioritize_air = 1, try to build about twice as much value in subs as air. Generally,
        #           certain countries will have a slight value (say 1) for long term needed builds like extra infantry
        #     6.5. Check if more units than build slots. If so, dont build all of the above step.
        #     7. Check remaining IPC and buy extra units if space. If not, upgrade units as long as they were not purchased
        #           due to the transports prioritization (bc then they may not fit)

        # This whole time, these purchased units should be added to a theortical dict called "placements" (name to unit list)
        pass

    def prioritizer(self, prioritization, strength):
        for list in self.prioritization_list:
            if list[0] == prioritization:
                list[1] = strength

    #TODO Utilize combat move attack decision module to determine which factories/ key neighbors are under threat
    # This will need to be called within build_strategy after adding the theoritical units to see if still under threat.
    def set_defensive_requirements(self, endangered_name_list):
        for territory_name in endangered_name_list:
            if (territory_name in factories):
                self.immediate_defensive_requirements.append(territory_name)

            for territory_key in factories:
                if territory_name == self.game.rules.connections[territory_key]:
                    self.latent_defensive_requirements.append(territory_key)

    def build_unit(self, territory_name, unit_index): #called by the AI
        self.game.state_dict[territory_name].append(self.game.rules.get_unit(unit_index))
        self.ipc = self.ipc - self.game.rules.get_unit(unit_index).cost

class Battle_calculator:
    #MAKE A COPY OF STUFF BEFORE YOU USE THIS BC THE BATTLE STUFF ACTUALLY MAKES CHANGES
    #account for land units on transpots in ipc swing
    # tool for the AI to determine how a battle WOULD turn out without actually changing the GameState
        def __init__(self, unit_state_list, territory_value):
            self.unit_state_list = unit_state_list
            self.ipc_swing = 0
            self.embattled_territory_value = territory_value
            self.victory_chance = 0  #consider both amalgamation and victory chance alone
            self.tie_chance = 0

            self.net_ipc_swing = self.ipc_swing + (self.embattled_territory_value * self.victory_chance)

        def battle_sim(self):
            # does the battle
            pass


# TODO: Plane retreating is different from normal retreating
class CombatMove:
    def __init__(self, game, aa_flyover=True):
        self.game = game
        self.aa_flyover = aa_flyover

    def can_move(self, unit_state, current_territory, goal_territory):
        return self.game.calc_movement(unit_state, current_territory, goal_territory)[0] >= 0

    def move_unit(self, unit_state, current_territory, goal_territory, bombing=False, bombarding=False):
        dist, path = self.game.calc_movement(unit_state, current_territory, goal_territory)
        if dist == -1:
            return False
        current_territory_state, goal_territory_state = self.game.state_dict[current_territory.name], self.game.state_dict[goal_territory.name]
        current_territory_state.unit_state_list.remove(unit_state)
        unit = self.game.rules.get_unit(unit_state.type_index)

        # AA guns
        if self.aa_flyover and unit.unit_type == 'air':
            # Check for aa guns in each territory
            for ter_name in path:
                territory_state = self.game.state_dict[ter_name]
                for other_unit_state in territory_state.unit_state_list:
                    if other_unit_state.type_index == 3 and self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
                        # Can only shoot 3 times
                        if other_unit_state.shots_taken < 3:
                            other_unit_state.shots_taken += 1
                            if random.randint(1, 6) == 1:
                                return True

        # Bombing factories
        if bombing and unit.name == 'bomber':
            for other_unit_state in goal_territory_state:
                if other_unit_state.type_index == 4 and other_unit_state.shots_taken < 3:
                    self.players[unit_state.owner].ipc -= random.randint(1, 6)
                    other_unit_state.shots_taken += 1
                    if random.randint(1, 6) == 1:
                        return True

        # Update unit
        goal_territory_state.unit_state_list.append(unit_state)
        unit_state.moves_used += dist
        unit_state.moved_from = path
        if unit_state.attached_to:
            unit_state.attached_to.attached_units.remove(unit_state)
            unit_state.attached_to = None
            # Bombarding
            if bombarding:
                # Check if there are enemy units to bombard
                enemy_units = False
                for other_unit_state in goal_territory_state:
                    if other_unit_state.type_index != 4 and self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
                        enemy_units = True
                        break
                if enemy_units:
                    # Check for battleships to bombard with
                    for other_unit_state in current_territory_state:
                        if other_unit_state.type_index == 10 and self.game.rules.teams[other_unit_state.owner] == self.game.rules.teams[unit_state.owner]:
                            if not other_unit_state.shots_taken:
                                other_unit_state.shots_taken += 1
                                unit_state.moves_used = unit.movement
                                # TODO: Can battleships bombard if they have already moved?
                                if random.randint(1, 6) <= 4:
                                    pass  # TODO: Enemy needs to choose casualty in goal_territory
        if goal_territory.is_water and unit.unit_type == 'land':
            # Attach to transport
            if unit.name == 'infantry':
                # Look for open infantry spots
                for other_unit_state in goal_territory_state:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0 or \
                                (len(other_unit_state.attached_units) == 1 and other_unit_state.attached_units[0].type_index != 0):
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
            # Look for any available spot
            if not unit_state.attached_to:
                for other_unit_state in goal_territory_state:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0:
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
                        elif len(other_unit_state.attached_units) == 1:
                            if unit.name == 'infantry' or other_unit_state.type_index == 0:
                                unit_state.attached_to = other_unit_state
                                other_unit_state.attached_units.append(unit_state)
                                break
        return True

class Battles:
    def __init__(self, game):
        self.territory_states = game.state_dict
        self.player = game.turn_state.player
        self.team = game.rules.teams[player]
        self.game = game
        game.turn_state.phase = 4

        self.retreating = False
        self.kamikaze = False
        #TODO Make this work

        self.enemy_team = game.rules.teams[player]
        while (self.enemy_team == game.rules.teams[player]):
            for country in self.game.rules.teams:
                if country != "Neutral":
                    self.enemy_team = game.rules.teams[country]
                else:
                    pass
        # sets enemy team to opposite team.

        for territory_key in self.territory_states:
            territory_state = self.territory_states[territory_key]
            unit_state_list = territory_state.unit_state_list

            #TODO Account for submarine submerge option

            if embattled (unit_state_list):
                #if two different team's units are in a territory at the end of combat move

                unit_state_list = battler(unit_state_list, self.game.rules.board[territory_key].ipc)  #resets unit_state_list to be equal to the remaining units
                for unit_state in unit_state_list:
                    if (unit_state.owner == self.player):  #factories are technically enemy
                        territory_state.owner = self.player
                        territory_state.just_captured = True
            else:
                pass

    def battler(self, unit_state_list, territory_value):
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

            # Unexpected retreat decision
            self.battle_calculator = Battle_calculator(unit_state_list, territory_value)
            if (self.battle_calculator.net_ipc_swing <= 0) and not self.kamikaze:  #this might not want to always be 0. Could let the AI decide?
                retreating == True

            #TODO BRETTTT. AMPHIBIOUS REEEEEEEEEEEEEEEEEE
            if self.retreating:
                self.retreating = False
                break

        return unit_state_list

    def embattled(self, unit_state_list):
        for unit_state in unit_state_list:
        if (self.game.rules.teams[unit_state.owner] != self.team) and (unit_state.type_index != 5):
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
            if (self.game.rules.teams[unit_state.owner] == self.team) \
            and (self.game.rules.units[unit_state.type_index].movement == 0):  #removes factories from consideration
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

        #will likely be either planes for defensive retreat, subs for submerge ability, or bombers on defense. or carriers
        if prioritize_unit_index != -1:
            for unit_state in friendly_units:
                if unit_state.type_index == prioritize_unit_index:
                    saving_list.append(unit_state)
                    friendly_units.remove(unit_state)

        #TODO CHECK IF THIS GOES INFINITE
        while casualty_count > 0:

            #choose based on power. This will automatically choose AA guns first
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

            # refills friendly_units with the units we tried to save if there are too many deaths
            if friendly_units == []:
                for unit_state in friendly_units:
                    friendly_units.append(unit_state)
                    saving_list.remove(unit_state)

            if (friendly_units == []) and (saving_list == []):
                break


class NonCombatMove:
    def __init__(self, game, aa_flyover):
        self.game = game
        self.aa_flyover = aa_flyover

    def can_move(self, unit_state, current_territory, goal_territory):
        return self.game.calc_movement(unit_state, current_territory, goal_territory)[0] >= 0

    def move_unit(self, unit_state, current_territory, goal_territory):
        dist, path = self.game.calc_movement(unit_state, current_territory, goal_territory)
        if dist == -1:
            return False
        current_territory_state, goal_territory_state = self.game.state_dict[current_territory.name], self.game.state_dict[goal_territory.name]
        current_territory_state.unit_state_list.remove(unit_state)
        for other_unit_state in unit_state.attached_units:
            current_territory_state.unit_state_list.remove(other_unit_state)
        unit = self.game.rules.get_unit(unit_state.type_index)

        # AA guns
        if self.aa_flyover and unit.unit_type == 'air':
            # Check for aa guns in each territory
            for ter_name in path:
                if ter_name not in unit_state.moved_from:
                    territory_state = self.game.state_dict[ter_name]
                    for other_unit_state in territory_state.unit_state_list:
                        if other_unit_state.type_index == 3 and self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
                            # Can only shoot 3 times
                            if other_unit_state.shots_taken < 3:
                                other_unit_state.shots_taken += 1
                                if random.randint(1, 6) == 1:
                                    return True

        # Update unit
        goal_territory_state.unit_state_list.append(unit_state)
        for other_unit_state in unit_state.attached_units:
            goal_territory_state.unit_state_list.append(other_unit_state)
        unit_state.moves_used += dist
        unit_state.moved_from = path
        if unit_state.attached_to:
            unit_state.attached_to.attached_units.remove(unit_state)
            unit_state.attached_to = None
        if goal_territory.is_water and unit.unit_type == 'land':
            # Attach to transport
            if unit.name == 'infantry':
                # Look for open infantry spots
                for other_unit_state in goal_territory_state:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0 or \
                                (len(other_unit_state.attached_units) == 1 and other_unit_state.attached_units[0].type_index != 0):
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
            # Look for any available spot
            if not unit_state.attached_to:
                for other_unit_state in goal_territory_state:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0:
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
                        elif len(other_unit_state.attached_units) == 1:
                            if unit.name == 'infantry' or other_unit_state.type_index == 0:
                                unit_state.attached_to = other_unit_state
                                other_unit_state.attached_units.append(unit_state)
                                break
        return True


class Place:
    def __init__(self, game, placements):
        game.turn_state.phase = 6
        self.placements = placements
        self.game = game

    def place(self):
        for territory_key in self.placements:
            for unit_state in placements[territory_key]:
                self.game.state_dict[territory_key].unit_state_list.append(unit_state)


class Cleanup:
    def __init__(self, game):

        game.turn_state.phase = 7

        for territory_key in game.state_dict:
            for unit_state in game.state_dict[territory_key].unit_state_list:
                if (unit_state.type_index == 5) and (game.state_dict[territory_key].owner != unit_state.owner):
                    unit_state.owner = game.state_dict[territory_key].owner   # reset factory ownership

                unit_state.moves_used = 0
                if unit_state.type_index != 5: #this is irrelevant because bombing directly affects IPCs. Allows change
                    unit_state.damage = 0
                unit_state.moved_from = []

            if game.state_dict[territory_key].owner == player:
                game.turn_state.player.ipc += game.rules.board[territory_key].ipc  #updates ipc

        if player == "America":
            game.turn_state.round_num += 1
        game.turn_state.player = game.rules.turn_order[player]  #sets player to the next player
