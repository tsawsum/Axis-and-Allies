import BoardState
import random
import math


class Vulnerability:
    def __init__(self, game):
        self.game = game

    def is_vulnerable(self, territory_name, theoretical_append=list()):
        pass


class Build:
    def __init__(self, game, endangered_name_list):  # game.turn_state, etc.
        self.game = game
        self.player = self.game.turn_state.player
        game.turn_state.phase = 2
        self.ipc = self.game.turn_state.player.ipc

        self.prioritization_list = []
        self.prioritization_list.append(['tech_token', 0])              # never use this one
        self.prioritization_list.append(['battleship', 0])              # 1
        self.prioritization_list.append(['factory', 0])                 # 2
        self.prioritization_list.append(['carrier', 0])                 # 3
        self.prioritization_list.append(['cruiser', 0])                 # 4
        self.prioritization_list.append(['bomber', 0])                  # 5
        self.prioritization_list.append(['carrier_fighter', 0])         # same here
        self.prioritization_list.append(['fighter', 0])                 # 7
        self.prioritization_list.append(['destroyer', 0])               # 8
        self.prioritization_list.append(['transport', 0])               # 9
        self.prioritization_list.append(['transportable_units', 0])     # only positive if no adjacent units
        self.prioritization_list.append(['sub', 0])                     # 11
        self.prioritization_list.append(['tank', 0])                    # 12
        self.prioritization_list.append(['aa', 0])                      # 13
        self.prioritization_list.append(['artillery', 0])               # 14
        self.prioritization_list.append(['infantry', 0])                # 15

        # sea
        self.sea_defense_sum = self.prioritization_list[1][1] + self.prioritization_list[3][1] \
            + self.prioritization_list[4][1] + self.prioritization_list[6][1] + self.prioritization_list[8][1]
        self.sea_sum = self.sea_defense_sum + self.prioritization_list[9][1] + self.prioritization_list[10][1] \
            + self.prioritization_list[11][1]

        # land. These may prove vistigial
        self.land_defense_sum = self.prioritization_list[12][1] + self.prioritization_list[13][1] \
            + self.prioritization_list[14][1] + self.prioritization_list[15][1] + self.prioritization_list[7][1]
        self.land_sum = self.land_defense_sum + self.prioritization_list[2][1] + self.prioritization_list[5][1]

        self.priority_sum = self.land_sum + self.sea_sum

        self.purchased_unit_state_list = []
        # purchasing
        for unit_priority in self.prioritization_list:
            priority_ratio = unit_priority[1]/self.priority_sum
            allotted_ipc = priority_ratio * self.ipc

            if unit_priority[0] == 'carrier_fighter':
                cost = 10
                num_purchased = round(allotted_ipc/cost)
                if num_purchased >= 1:
                    for i in range(num_purchased):
                        if (self.ipc - cost) >= 0:
                            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 11))
                            self.ipc -= cost

            elif unit_priority[0] == 'transportable_units':
                cost = 7
                num_purchased = round(allotted_ipc/cost)
                if num_purchased >= 1:
                    for i in range(num_purchased):
                        if (self.ipc - cost) >= 0:
                            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 0))
                            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 1))
                            self.ipc -= cost

            else:
                for unit in self.game.rules.units:
                    if unit.name == unit_priority[0]:
                        cost = unit.cost
                        num_purchased = round(allotted_ipc/cost)
                        if num_purchased >= 1:
                            for i in range(num_purchased):
                                if (self.ipc - cost) >= 0:
                                    self.purchased_unit_state_list.append(BoardState.UnitState(self.player, self.game.rules.units.index(unit)))
                                    self.ipc = self.ipc - cost
        while self.ipc >= 3:
            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 0))
            self.ipc -= 3

        # self.set_defensive_requirements(endangered_name_list)

    def prioritizer(self, prioritization, strength):
        for arr in self.prioritization_list:
            if arr[0] == prioritization:
                arr[1] = strength

    def build_unit(self, territory_name, unit_index):  # called by the AI
        self.game.state_dict[territory_name].append(self.game.rules.get_unit(unit_index))
        self.ipc = self.ipc - self.game.rules.get_unit(unit_index).cost


class BattleCalculator:
    # MAKE A COPY OF STUFF BEFORE YOU USE THIS BC THE BATTLE STUFF ACTUALLY MAKES CHANGES
    # account for land units on transpots in ipc swing
    # tool for the AI to determine how a battle WOULD turn out without actually changing the GameState
    def __init__(self, unit_state_list, territory_value):
        self.unit_state_list = unit_state_list
        self.ipc_swing = 0
        self.embattled_territory_value = territory_value
        self.victory_chance = 0  # consider both amalgamation and victory chance alone
        self.tie_chance = 0

        self.net_ipc_swing = self.ipc_swing + (self.embattled_territory_value * self.victory_chance)

    def battle_sim(self):
        # does the battle
        pass


# TODO: Plane retreating is different from normal retreating <- Why for combat move instead of Battle class
# one extra attack per artillery/infantry pair
# TODO: James Hawkes' tactical battle strategy: First attack capitals. Otherwise calculate the "IPC value" of
#   the territory which is the total unit value of the enemy units plus twice the territory value.
#   then calculate "defense score" which is the total defensive power + (average_power_of_both_sides) * the total number of units
#           + (standard deviation * (0.5 + number_of_units)/4.5)
#  approx both sides averaeg by (opponent average * 1/2) + 1
#   then determine the ratio: and pick like the top 5 to battle calculate
#  Make sure to both prioritize taking facotry territories and to not include them in the above calculation
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
                    self.game.players[unit_state.owner].ipc -= random.randint(1, 6)
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
                        if other_unit_state.type_index == 10 and \
                                self.game.rules.teams[other_unit_state.owner] == self.game.rules.teams[unit_state.owner]:
                            if not other_unit_state.shots_taken:
                                other_unit_state.shots_taken += 1
                                unit_state.moves_used = unit.movement
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


# TODO BRETT. Impliment territories going back to original owner if they haev capitals
class Battles:
    def __init__(self, game):
        self.territory_states = game.state_dict
        self.player = game.turn_state.player
        self.team = game.rules.teams[self.player]
        self.game = game
        game.turn_state.phase = 4

        self.retreating = False
        self.kamikaze = False
        self.battle_calculator = None
        # TODO Make this work

        self.enemy_team = game.rules.teams[self.player]
        while self.enemy_team == game.rules.teams[self.player]:
            for country in self.game.rules.teams:
                if country != "Neutral":
                    self.enemy_team = game.rules.teams[country]
                else:
                    pass
        # sets enemy team to opposite team.

        for territory_key in self.territory_states:
            territory_state = self.territory_states[territory_key]
            unit_state_list = territory_state.unit_state_list

            # TODO Account for submarine submerge option

            if self.embattled(unit_state_list):
                # if two different team's units are in a territory at the end of combat move

                # resets unit_state_list to be equal to the remaining units
                unit_state_list = self.battler(unit_state_list, territory_key)
                for unit_state in unit_state_list:
                    if unit_state.owner == self.player:  # factories are technically enemy
                        territory_state.just_captured = True
                        # Check if original owner has capital and is ally, if so give it back to them
                        original_owner = self.game.rules.board[territory_key].original_owner
                        capital = self.game.players[original_owner].capital
                        if self.game.rules.teams[self.player] == self.game.rules.teams[original_owner]\
                                and (self.game.state_dict[capital].owner == original_owner or territory_key == capital):
                            territory_state.owner = original_owner
                        else:
                            territory_state.owner = self.player
            else:
                pass

    def battler(self, unit_state_list, territory_name):
        # inputs units (unit_states) originally in embattled territory and returns remaining units
        territory_value = self.game.rules.board[territory_name].ipc
        while self.embattled(unit_state_list):

            total_friendly_power = 0
            total_enemy_power = 0

            offense_units, defense_units = list(), list()
            for unit_state in unit_state_list:
                if self.game.rules.teams[unit_state.owner] == self.team:
                    # assume offense for current player
                    offense_units.append(unit_state)
                    total_friendly_power += self.game.rules.units[unit_state.type_index].attack  # I think this path works...
                    # This only defines one of the two powers, never both
                else:
                    defense_units.append(unit_state)
                    total_enemy_power += self.game.rules.units[unit_state.type_index].defense

            friendly_units_killed = self.hit_roller(total_enemy_power % 6) + math.floor(total_enemy_power / 6)
            enemy_units_killed = self.hit_roller(total_friendly_power % 6) + math.floor(total_friendly_power / 6)

            self.casualty_selector(self.team, unit_state_list, 'attack', friendly_units_killed)
            self.casualty_selector(self.enemy_team, unit_state_list, 'defense', enemy_units_killed)
            # these modify unit_state_list

            # Get territories that cna be retreated to
            retreat_options = set()
            for unit_state in offense_units:
                if self.rules.get_unit(unit_state.type_index).unit_type != 'air' and \
                        len(unit_state.moved_from) >= 2 and not self.game.rules.board[unit_state.moved_from[-2]].is_water:
                    retreat_options.add(unit_state.moved_from[-2])

            # Unexpected retreat decision
            self.battle_calculator = BattleCalculator(unit_state_list, territory_value)
            if (self.battle_calculator.net_ipc_swing <= 0) and not self.kamikaze:  # this might not want to always be 0. Could let the AI decide?
                self.retreating = True

            # Don't try to retreat if there's nowhere to retreat to
            # TODO: Planes and subs might still want to leave battle even if other units stay?
            if self.retreating and retreat_options:
                self.retreating = False
                for unit_state in offense_units:
                    if self.rules.get_unit(unit_state.type_index).unit_type != 'air':
                        retreat_choice = retreat_options[0]  # TODO: AI needs to choose where it should retreat to
                        self.game.state_dict[retreat_choice].unit_state_list.append(unit_state)
                        self.game.state_dict[territory_name].unit_state_list.remove(unit_state)
                        if unit_state in unit_state_list:
                            unit_state_list.remove(unit_state)
                break

        # TODO fix recapturing territories swapping owners
        # How does this move units out of the territory back to another?
        # Todo remove units to the territory they came from
        # if (self.game.rules.board[territory_key].is_capital != ""):
            # if (is_offense == true):
                # self.player[offense_units[0].owner].ipc
                # self.player[offense_units[0].owner].ipc = self.player[offense_units[0].owner].ipc + self.player[defense_units[0].owner].ipc
                # self.game.rules.teams[unit_state.owner].ipc = 0
            # else:
                # self.game.rules.teams[unit_state.owner].ipc = self.game.rules.teams[unit_state.owner].ipc + self.team.ipc
                # self.team.ipc = 0
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

    def casualty_selector(self, team, unit_state_list, attack_or_defense, casualty_count,
                          one_land_unit_remaining=False, prioritize_unit_index=-1):
        friendly_units = []

        for unit_state in unit_state_list:
            if (self.game.rules.teams[unit_state.owner] == team) \
                    and (self.game.rules.units[unit_state.type_index].movement == 0):  # removes factories from consideration
                friendly_units.append(unit_state)

        # check if can simply wipe the list
        if casualty_count >= len(friendly_units):
            for unit_state in friendly_units:
                unit_state_list.remove(unit_state)

        # saving list keeps caveats if set to True
        saving_list = []

        if one_land_unit_remaining:
            highest_cost = 0
            for unit_state in friendly_units:
                if self.game.rules.units[unit_state.type_index].cost >= highest_cost \
                        and self.game.rules.units[unit_state.type_index].unit_type == "land":
                    highest_cost = self.game.rules.units[unit_state.type_index].cost
            for i in range(len(friendly_units)-1, -1, -1):
                if self.game.rules.units[friendly_units[i].type_index].cost == highest_cost \
                        and self.game.rules.units[friendly_units[i].type_index].unit_type == "land":
                    saving_list.append(friendly_units.pop(i))

        # will likely be either planes for defensive retreat, subs for submerge ability, or bombers on defense. or carriers
        if prioritize_unit_index != -1:
            for i in range(len(friendly_units) - 1, -1, -1):
                if friendly_units[i].type_index == prioritize_unit_index:
                    saving_list.append(friendly_units.pop(i))

        while casualty_count > 0:
            # TODO: Unit().attack_or_defense does not exist
            # choose based on power. This will automatically choose AA guns first
            lowest_power = 6
            for unit_state in friendly_units:
                if self.game.rules.units[unit_state.type_index].attack_or_defense <= lowest_power:
                    lowest_power = self.game.rules.units[unit_state.type_index].attack_or_defense
            lowest_power_list = []
            for unit_state in friendly_units:
                if self.game.rules.units[unit_state.type_index].attack_or_defense == lowest_power:
                    lowest_power_list.append(unit_state)

            # two while loops allows us to remove redundant use of lowest_power
            while lowest_power_list and casualty_count > 0:

                # then choose based on cost
                lowest_cost_unit = min(lowest_power_list, key=lambda x: self.game.rules.units[x.type_index].cost)
                unit_state_list.remove(lowest_cost_unit)  # to change the master list
                friendly_units.remove(lowest_cost_unit)  # for the while loop
                lowest_power_list.remove(lowest_cost_unit)  # for the while loop
                casualty_count = casualty_count - 1

            # refills friendly_units with the units we tried to save if there are too many deaths
            if not friendly_units:
                if not saving_list:
                    break
                else:
                    friendly_units = saving_list


class NonCombatMove:
    # TODO have a simple extra AA gun move prioritizer. If the builds makes one have the NC move it to a good place.
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
                        if other_unit_state.type_index == 3 and \
                                self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
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
    """
    this class is primarily a long list of If's. Actual machine learning would be wasted here, as placing units
    is a pretty linear, albeit complicated, process.
    """
    # TODO. Somehow make the transportable_units we bought earlier place correcty. AKA next to where you put transport

    # TODO: General: Make sure we dont accidentally build duplicates of purchased units, or build too many units per
    #  factory. Also make sure theoretical_append gets reset every time.
    def __init__(self, game, endangered_name_list, purchased_unit_state_list):
        game.turn_state.phase = 6
        self.placements = {}
        self.game = game
        self.endangered_name_list = endangered_name_list
        self.purchased_unit_state_list = purchased_unit_state_list
        self.immediate_defensive_requirements = list()
        self.latent_defensive_requirements = list()
        self.vulnerability = Vulnerability(game)

        self.factories = []
        for territory_name in self.game.state_dict:
            for unit_state in self.game.state_dict[territory_name].unit_state_list:
                if unit_state.type_index == 4:
                    self.factories.append(territory_name)
        # self.factories now has a list of names having factories

    # TODO Utilize combat move attack decision module to determine which factories/ key neighbors are under threat
    # This will need to be called within build_strategy after adding the theoritical units to see if still under threat.
    def set_defensive_requirements(self, endangered_name_list):
        for territory_name in endangered_name_list:
            if territory_name in self.factories:
                self.immediate_defensive_requirements.append(territory_name)

            for territory_key in self.factories:
                if territory_name in self.game.rules.board[territory_key].neighbors:
                    self.latent_defensive_requirements.append(territory_key)


    def build_slots(self, territory_name, factory_name=""):
        # returns remaining build slots of a territory
        if not factory_name:
            factory_name = territory_name
            return self.game.rules.board[territory_name].ipc - self.game.state_dict[territory_name].built_units
        else:
            build_slots = 0
            for fac_territory_name in self.adjacent_factory_finder(factory_name):
                build_slots += (self.game.rules.board[fac_territory_name].ipc
                                - self.game.state_dict[fac_territory_name].built_units)
            return build_slots

    def can_be_saved(self, theoretical_append, territory_name):
        # returns "can be saved True" if the territory is not a capital and can be saved. If is a capital and cant be
        # saved, automatically places (puts into palcement dict) max in the capital.
        build_slots = self.build_slots(territory_name)

        can_be_saved = True
        # check if can be saved
        for unit_state in self.purchased_unit_state_list:
            if len(theoretical_append) < build_slots:
                if unit_state.type_index == 11:  # fighter
                    theoretical_append.append(unit_state)
                if unit_state.type_index == 2:   # tank
                    theoretical_append.append(unit_state)
                if unit_state.type_index == 1 or unit_state.type_index == 0:  # inf or art
                    theoretical_append.append(unit_state)
                if unit_state.type_index == 3:  # aa
                    theoretical_append.append(unit_state)
        # TODO impliment capitals. Make is_capital work, and make it so that money isnt collected, and make
        #  all money taken by capturer. and make plaers with no money not be able to build.
        # TODO make the below line make sense. Dont actually append units but do the is_vunerable calculation as if you did
        if self.vulnerability.is_vulnerable(territory_name, theoretical_append):
            if self.game.rules.board[territory_name].is_capital:  # protect capital at all costs
                self.theoretical_to_placements(theoretical_append, territory_name)
            else:  # abandon if cant possibly hold.
                theoretical_append = []
                can_be_saved = False
        return can_be_saved

    def front_line_builder(self, theoretical_append, territory_name, vulnerability_reader_active=True):
        # prioritizes an even spread of infantry and artillery in frontline factories

        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, theoretical_append)

        # TODO Make the pathfinder proximity reader work. Should only count adjacent enmny land tertiries
        build_slots = self.build_slots(territory_name)
        for unit_state in self.purchased_unit_state_list:
            if vulnerability_reader:
                if (unit_state.type_index == 1) \
                        and (len(theoretical_append) < math.floor(build_slots/2)):  # artillery
                    theoretical_append.append(unit_state)
        for unit_state in self.purchased_unit_state_list:
            if vulnerability_reader:
                if (unit_state.type_index == 0) \
                        and len(theoretical_append) < build_slots:  # fills the rest of the space with infantry
                    theoretical_append.append(unit_state)
        for unit_state in self.purchased_unit_state_list:
            if self.game.rules.get_unit(unit_state.type_index).unit_type != "sea" \
                    and (unit_state.type_index != 1) and (unit_state.type_index != 0) \
                    and vulnerability_reader:
                if len(theoretical_append) < build_slots:
                    theoretical_append.append(unit_state)

    def reserve_line_builder(self, theoretical_append, territory_name, vulnerability_reader_active=True):
        # puts, in theoretical_append, land units in non-frontline factories

        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, theoretical_append)

        build_slots = self.build_slots(territory_name)
        for unit_state in self.purchased_unit_state_list:
            if self.game.rules.get_unit(unit_state.type_index).unit_type != "sea" \
                    and vulnerability_reader:
                if len(theoretical_append) < build_slots:
                    theoretical_append.append(unit_state)

    def adjacent_factory_finder(self, territory_name):
        # returns a list of territory names that have factories
        adjacent_factory_list = []

        neighbors = self.game.rules.board[territory_name].neighbors
        for neighbor_name in neighbors:
            territory_state = self.game.state_dict[neighbor_name]
            for unit_state in territory_state.attached_units:
                if unit_state.type_index == 4:  # factory
                    adjacent_factory_list.append(neighbor_name)

        return adjacent_factory_list

    def sea_zone_builder(self, theoretical_append, territory_name, adjacent_factory_list, vulnerability_reader_active=True):

        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, theoretical_append)

        for unit_state in self.purchased_unit_state_list:
            if self.game.rules.get_unit(unit_state.type_index).unit_type == "sea" \
            and vulnerability_reader:
                # choose the bigger factory to remove build slots from first. Sub-optimal but fine.
                i = 0
                adjacent_factory_list.sort(reverse=True, key=lambda x:self.game.rules.board[x].ipc)
                for fac_territory_name in adjacent_factory_list:
                    if i == 0 and len(theoretical_append) < self.build_slots(fac_territory_name):
                        i = 1
                        theoretical_append.append(unit_state)
                        # TODO: Have the AI organize the placements list.

            elif unit_state.type_index == 11 \
            and self.vulnerability.is_vulnerable(territory_name, theoretical_append):
                carrier_slots = 0
                for ship_state in theoretical_append:
                    if ship_state.type_index == 9:
                        carrier_slots += 2
                for ship_state in self.game.state_dict[territory_name].unit_state_list:
                    if ship_state.type_index == 9:
                        carrier_slots += 2
                    if ship_state.type_index == 11: #aka already a fighter on board
                        carrier_slots -= 1

    def update_vulnerable_builds(self, territory_name, theoretical_append):
        i = 0
        while self.vulnerability.is_vulnerable(territory_name, theoretical_append):
            i += 1
            if i == 1:
                for unit_state in theoretical_append:
                    if unit_state.type_index == 1 or unit_state.type_index == 0: # replaces art/inf w/tanks
                        for purchased_unit_state in self.purchased_unit_state_list:
                            if purchased_unit_state.type_index == 2:  # Tanks
                                theoretical_append.append(purchased_unit_state)
                                theoretical_append.remove(unit_state)

            phase1_fighter_count = 0
            if i == 2:
                for unit_state in theoretical_append:
                    if unit_state.type_index != 2:  # replaces everything but tanks with fighters
                        for purchased_unit_state in self.purchased_unit_state_list:
                            if purchased_unit_state.type_index == 11:  # fighters
                                phase1_fighter_count += 1
                                theoretical_append.append(purchased_unit_state)
                                theoretical_append.remove(unit_state)

            phase2_fighter_count = 0
            if i == 3:
                for unit_state in theoretical_append:
                    if unit_state.type_index != 11:  # replaces everything with fighters
                        for purchased_unit_state in self.purchased_unit_state_list:
                            if purchased_unit_state.type_index == 11:
                                phase2_fighter_count += 1
                                if phase2_fighter_count >= phase1_fighter_count:  # prevents duplicates
                                    theoretical_append.append(purchased_unit_state)
                                    theoretical_append.remove(unit_state)

            if i == 4:
                break  # just in case. If this happens something is broken

    def theoretical_to_placements(self, theoretical_append, territory_name, factory_name=""):
        if not factory_name:
            factory_name = territory_name

        for unit_state in theoretical_append:
            self.purchased_unit_state_list.remove(unit_state)
            self.placements[territory_name] = unit_state
            self.game.state_dict[factory_name].built_units += 1

        theoretical_append.clear()

    # TODO: How to build factories?
    def build_strategy(self):  # called by the AI

        if self.immediate_defensive_requirements:     # this will always be land
            self.immediate_defensive_requirements.sort(reverse=True, key=lambda x: self.game.rules.board[x].ipc)
            for territory_name in self.immediate_defensive_requirements:
                build_slots = self.build_slots(territory_name)
                theoretical_append = []

                can_be_saved = self.can_be_saved(theoretical_append, territory_name)  # this is a bool, but also modifies stuff

                if can_be_saved:
                    self.front_line_builder(theoretical_append, territory_name)
                    # fills frontline territories with infantry and artillery first, then with other land units.
                    if self.vulnerability.is_vulnerable(territory_name, theoretical_append):
                        self.update_vulnerable_builds(territory_name, theoretical_append)

                else:
                    self.reserve_line_builder(theoretical_append, territory_name)
                    if self.vulnerability.is_vulnerable(territory_name, theoretical_append):
                        self.update_vulnerable_builds(territory_name, theoretical_append)

                # puts the theoretical units into the placements and removes them from purchased_unit_state_list
                self.theoretical_to_placements(theoretical_append, territory_name)
            # This concludes immediate_defensive_requirements

        elif self.latent_defensive_requirements:
            for territory_name in self.latent_defensive_requirements:
                build_slots = self.build_slots(territory_name)
                theoretical_append = []
                adjacent_factory_list = self.adjacent_factory_finder(territory_name)

                if self.game.state_dict[territory_name].owner == "Sea Zone":
                    self.sea_zone_builder(theoretical_append, territory_name, adjacent_factory_list)

                else: #builds max (front-line) units in factories adjacent to threatened land zones, if any
                    self.front_line_builder(self, theoretical_append, territory_name, False)

                self.theoretical_to_placements(theoretical_append, territory_name)

        else: #places all the rest of the units according to the order they are in the list.
            for territory_name in factories:
                build_slots = self.build_slots(territory_name)
                theoretical_append = []

                if self.game.state_dict[territory_name].owner == "Sea Zone":
                    self.sea_zone_builder(theoretical_append, territory_name, adjacent_factory_list, False)
                else:
                    self.reserve_line_builder(theoretical_append, territory_name, False)

                self.theoretical_to_placements(theoretical_append, territory_name)

    def place(self):
        for territory_key in self.placements:
            for unit_state in self.placements[territory_key]:
                self.game.state_dict[territory_key].unit_state_list.append(unit_state)


class Cleanup:
    def __init__(self, game):

        game.turn_state.phase = 7

        for territory_key in game.state_dict:
            for unit_state in game.state_dict[territory_key].unit_state_list:
                if (unit_state.type_index == 5) and (game.state_dict[territory_key].owner != unit_state.owner):
                    unit_state.owner = game.state_dict[territory_key].owner   # reset factory ownership
            for territory_state in game.state_dict[territory_key]:
                territory_state.built_units = 0                               # reset built_units

                unit_state.moves_used = 0
                if unit_state.type_index != 5:  # this is irrelevant because bombing directly affects IPCs. Allows change
                    unit_state.damage = 0
                unit_state.moved_from = []

            if game.state_dict[territory_key].owner == game.turn_state.player:
                game.turn_state.player.ipc += game.rules.board[territory_key].ipc  # updates ipc

        if game.turn_state.player == "America":
            game.turn_state.round_num += 1
        game.turn_state.player = game.rules.turn_order[game.turn_state.player]  # sets player to the next player
