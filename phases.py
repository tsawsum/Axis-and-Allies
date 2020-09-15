import BoardState
import random
from statistics import stdev


class UnitStack:
    # Used to make transports in Attackable and Vulnerable much easier to handle
    def __init__(self, game, unit_state, territory, transported_units=None, transported_unit_territories=None):
        if transported_units:
            self.transport_state = unit_state
            self.transport_territory = territory
            self.land_unit_territories = transported_unit_territories
            self.land_unit_states = transported_units
            self.land_units = [game.rules.get_unit(land_unit_state.type_index) for land_unit_state in self.land_unit_states]
            if len(self.land_units) == 2 and self.land_units[1].name == 'infantry':
                self.land_units = self.land_units[::-1]
                self.land_unit_states = self.land_unit_states[::-1]
                self.land_unit_territories = self.land_unit_territories[::-1]
            self.unit_state = None
            self.unit = None
            self.is_transport = True
            self.territory = None
        else:
            self.unit_state = unit_state
            self.unit = game.rules.get_unit(unit_state.type_index)
            self.territory = territory
            self.transport_state = None
            self.land_unit_states = None
            self.land_units = None
            self.is_transport = False
            self.transport_territory = None
            self.land_unit_territories = None
        self.possible_goals = list()

    def remove_units(self, unit_state_list):
        if self.is_transport:
            for unit_state in unit_state_list:
                if unit_state in self.land_unit_states:
                    i = self.land_unit_states.index(unit_state)
                    self.land_units.pop(i)
                    self.land_unit_states.pop(i)
                    self.land_unit_territories.pop(i)

    def get_unit_states(self):
        if self.is_transport:
            return self.land_unit_states
        else:
            return [self.unit_state]

    def get_attack_power(self):
        if not self.is_transport:
            return self.unit.attack
        else:
            if len(self.land_units) == 2 and self.land_units[1].name == 'artillery':
                return self.land_units[0].attack + 1 + self.land_units[1].attack
            else:
                return sum([land_unit.attack for land_unit in self.land_units])


class Attackable:
    # James Hawkes' tactical battle strategy: First attack capitals. Otherwise calculate the "IPC value" of
    #   the territory which is the total unit value of the enemy units plus twice the territory value.
    #   then calculate "defense score" which is the total defensive power + (average_power_of_both_sides) * the total number of units
    #           + (standard deviation * (0.5 + number_of_units)/4.5)
    #  approx both sides averaeg by (opponent average * 1/2) + 1
    #   then determine the ratio: and pick like the top 5 to battle calculate
    #  Make sure to both prioritize taking factory territories and to not include them in the above calculation
    def __init__(self, game, player, ai_importance, risk_tolerances, vuln=None):
        self.game = game
        self.player = player
        if vuln:
            self.vuln = vuln
        else:
            self.vuln = Vulnerability(game)
        self.importance = ai_importance
        self.risk_tolerances = risk_tolerances

    def get_is_frontline(self, territory_name):
        enemy_team = self.game.rules.enemy_team(player=self.game.state_dict[territory_name].owner)
        for neighbor in self.game.rules.board[territory_name].neighbors:
            if self.game.rules.teams[self.game.state_dict[neighbor].owner] == enemy_team:
                return True
        return False

    def is_worth_attacking_battle_sim(self, territory_name, battle_sim):
        # TODO (Future) Make this better
        return battle_sim.net_ipc_swing > 0

    def is_worth_attacking(self, territory_name):
        # TODO (Future): Make this better
        owner = self.game.state_dict[territory_name].owner
        enemy_team = self.game.rules.enemy_team(player=self.player)

        has_friendly_units, has_enemy_units, has_factory = False, False, False
        for unit_state in self.game.state_dict[territory_name].unit_state_list:
            if self.game.rules.teams[unit_state.owner] == enemy_team:
                has_enemy_units = True
            else:
                has_friendly_units = True

        vulnerability = self.vuln.get_vulnerability(territory_name, attacker=self.player)

        return (owner == 'Sea Zone' or self.game.rules.teams[owner] != self.game.rules.teams[self.player]) \
               and (has_enemy_units or not has_friendly_units) \
               and vulnerability >= self.risk_tolerances[territory_name]

    def get_best_attacks(self, just_get_territories=False):
        # TODO (Future): Planes sometimes try to attack sea zones with only subs, which does nothing since the sub just submerges
        # TODO (Future): Fighters will often try to attack with the intention of returning to a certain carrier. But, multiple fighters will try to
        #                do this, and the carrier can only save one or two of them
        possible_territories = sorted([territory_name for territory_name in self.game.state_dict.keys()
                                       if self.is_worth_attacking(territory_name)],
                                      key=lambda x: self.importance[x], reverse=True)

        # Get list of territories that each unit can attack
        attackable_by_unit = dict()
        for territory_name in possible_territories:
            for unit_stack in self.vuln.territories[territory_name][self.player]:
                if unit_stack.is_transport or unit_stack.unit_state.type_index != 9:  # Ignore carriers in combat move
                    if unit_stack not in attackable_by_unit.keys():
                        attackable_by_unit[unit_stack] = list()
                    attackable_by_unit[unit_stack].append(territory_name)

        attackable_by_unit_copy = {k: v[:] for k, v in attackable_by_unit.items()}

        # Temporarily remove units from battle if they can attack multiple places
        can_attack_one, can_attack_many = list(), list()
        for unit_stack, territories in attackable_by_unit.items():
            if len(territories) > 1:
                can_attack_many.append(unit_stack)
                for territory_name in territories:
                    self.vuln.territories[territory_name][self.player].remove(unit_stack)
            else:
                can_attack_one.append(unit_stack)

        while True:
            while True:
                # See which territories are still good to attack even without these units
                still_attackable = dict()
                for territory_name in possible_territories:
                    if self.is_worth_attacking(territory_name):
                        still_attackable[territory_name] = self.vuln.get_vulnerability(territory_name)

                # Remove these territories from units that can attack multiple
                changed_units = list()
                for unit_stack in can_attack_many:
                    removed = list()
                    for territory_name in still_attackable.keys():
                        if territory_name in attackable_by_unit[unit_stack]:
                            attackable_by_unit[unit_stack].remove(territory_name)
                            removed.append(territory_name)
                    if len(attackable_by_unit[unit_stack]) == 0:
                        most_needed_at = min(removed, key=lambda x: still_attackable[x])
                        attackable_by_unit[unit_stack].append(most_needed_at)
                    if len(attackable_by_unit[unit_stack]) == 1:
                        changed_units.append(unit_stack)
                        self.vuln.territories[attackable_by_unit[unit_stack][0]][self.player].append(unit_stack)
                for unit_stack in changed_units:
                    can_attack_many.remove(unit_stack)
                    can_attack_one.append(unit_stack)
                if not changed_units:
                    break

            # See which territories still need help
            not_still_attackable = list()
            for territory_name in possible_territories:
                if not self.is_worth_attacking(territory_name):
                    not_still_attackable.append(territory_name)

            if not can_attack_many or not not_still_attackable:
                break

            # Send units to attack the most important territory still remaining
            # Choose units to send based on how much they boost vulnerability
            attacking_territory = not_still_attackable.pop(0)
            while not self.is_worth_attacking(attacking_territory):
                biggest_boost, attacking_unit = 0, None
                for unit_stack in can_attack_many:
                    if attacking_territory in attackable_by_unit[unit_stack]:
                        prev_vuln = self.vuln.get_vulnerability(attacking_territory, attacker=self.player)
                        self.vuln.territories[attacking_territory][self.player].append(unit_stack)
                        vuln_boost = self.vuln.get_vulnerability(attacking_territory, attacker=self.player) - prev_vuln
                        self.vuln.territories[attacking_territory][self.player].remove(unit_stack)
                        if vuln_boost > biggest_boost:
                            attacking_unit, biggest_boost = unit_stack, vuln_boost
                if attacking_unit:
                    self.vuln.territories[attacking_territory][self.player].append(attacking_unit)
                    attackable_by_unit[attacking_unit] = [attacking_territory]
                    can_attack_many.remove(attacking_unit)
                    can_attack_one.append(attacking_unit)
                elif not_still_attackable:
                    attacking_territory = not_still_attackable.pop(0)
                else:
                    break

        # Any unused units that can attack should help where possible
        for unit_stack in can_attack_many:
            biggest_boost, attacking_territory = 0, None
            for territory_name in attackable_by_unit[unit_stack]:
                if territory_name in still_attackable:
                    prev_vuln = self.vuln.get_vulnerability(territory_name, attacker=self.player)
                    self.vuln.territories[territory_name][self.player].append(unit_stack)
                    vuln_boost = (prev_vuln - self.vuln.get_vulnerability(territory_name, attacker=self.player)) * \
                                 self.importance[territory_name]
                    self.vuln.territories[territory_name][self.player].remove(unit_stack)
                    if vuln_boost > biggest_boost:
                        attacking_territory, biggest_boost = territory_name, vuln_boost
            if attacking_territory:
                self.vuln.territories[attacking_territory][self.player].append(unit_stack)
                attackable_by_unit[unit_stack] = [attacking_territory]

        # Create theoretical attack
        theoretical_attack = dict()
        for unit_stack in attackable_by_unit.keys():
            if attackable_by_unit[unit_stack][0] in still_attackable:
                theoretical_attack[unit_stack] = attackable_by_unit[unit_stack][0]

        battles = dict()
        for unit_stack, territory_name in theoretical_attack.items():
            if territory_name not in battles:
                battles[territory_name] = [UnitStack(self.game, unit_state, territory_name)
                                           for unit_state in self.game.state_dict[territory_name].unit_state_list[:]]
            battles[territory_name].append(unit_stack)

        # Run battle simulator on these battles to make sure none of them are bad
        # If they are, take the worst battle, remove the units and reassign them somewhere better
        while True:
            # Find worst battle
            not_worth = list()
            for territory_name in battles.keys():
                unit_state_list = list()
                for unit_stack in battles[territory_name]:
                    for unit_state in unit_stack.get_unit_states():
                        unit_state_list.append(unit_state)
                battle_sim = BattleCalculator(self.game, self.player, unit_state_list, self.importance, territory_name)
                if not self.is_worth_attacking_battle_sim(territory_name, battle_sim):
                    not_worth.append(territory_name)
            if not not_worth:
                break
            not_worth.sort(key=lambda x: self.importance[x], reverse=True)
            worst_battle = not_worth.pop()
            # Reassign these units
            for unit_stack in battles[worst_battle]:
                if unit_stack in attackable_by_unit_copy.keys():
                    theoretical_attack[unit_stack] = ''
                    for i in range(len(not_worth)):
                        if not_worth[i] in attackable_by_unit_copy[unit_stack]:
                            theoretical_attack[unit_stack] = not_worth[i]
                            break
                    if theoretical_attack[unit_stack]:
                        unit_state_list = list()
                        for other_unit_stack in battles[theoretical_attack[unit_stack]]:
                            for unit_state in other_unit_stack.get_unit_states():
                                unit_state_list.append(unit_state)
                        battle_sim = BattleCalculator(self.game, self.player, unit_state_list, self.importance, theoretical_attack[unit_stack])
                        if self.is_worth_attacking_battle_sim(theoretical_attack[unit_stack], battle_sim):
                            not_worth.remove(theoretical_attack[unit_stack])
            del battles[worst_battle]
            if not not_worth:
                break

        # When looking at what the enemy wants to attack, save time by only returning the territories that they want to attack
        if just_get_territories:
            self.vuln.invalid = True
            return list(battles.keys())

        # Find the best location for all unassigned units
        for unit_stack in theoretical_attack.keys():
            if not theoretical_attack[unit_stack]:
                biggest_boost, attacking_territory = 0, None
                for territory_name in attackable_by_unit_copy[unit_stack]:
                    if territory_name in still_attackable:
                        prev_vuln = self.vuln.get_vulnerability(territory_name, attacker=self.player)
                        self.vuln.territories[territory_name][self.player].append(unit_stack)
                        vuln_boost = (prev_vuln - self.vuln.get_vulnerability(territory_name, attacker=self.player)) * \
                                     self.importance[territory_name]
                        self.vuln.territories[territory_name][self.player].remove(unit_stack)
                        if vuln_boost > biggest_boost:
                            attacking_territory, biggest_boost = territory_name, vuln_boost
                if attacking_territory:
                    theoretical_attack[unit_stack] = attacking_territory

        # For every battle, remove attacking units until it reaches a certain threshold. Leave behind ones from the most vulnerable territory
        battles_2 = dict()
        threshold = 3
        for unit_stack, territory_name in theoretical_attack.items():
            if territory_name:
                if territory_name not in battles_2:
                    battles_2[territory_name] = list()
                battles_2[territory_name].append(unit_stack)
                for unit_state in unit_stack.get_unit_states():
                    self.game.state_dict[territory_name].unit_state_list.append(unit_state)
                if unit_stack.is_transport:
                    for i in range(len(unit_stack.land_unit_states)):
                        self.game.state_dict[unit_stack.land_unit_territories[i]].unit_state_list.remove(unit_stack.land_unit_states[i])
                else:
                    self.game.state_dict[unit_stack.territory].unit_state_list.remove(unit_stack.unit_state)
        dont_move = list()
        for territory_name, unit_stack_list in battles_2.items():
            attack_unit_states = list()
            for unit_stack in unit_stack_list:
                attack_unit_states += unit_stack.get_unit_states()
            while True:
                res = self.vuln.battle_formula(attack_units=[self.game.rules.get_unit(us.type_index) for us in attack_unit_states],
                                               defense_units=[self.game.rules.get_unit(us.type_index) for us in self.vuln.territories[territory_name][self.game.rules.enemy_team(player=self.player)]])
                if res < threshold:
                    break

                can_remove = list()
                for unit_stack in unit_stack_list:
                    for unit_state in unit_stack.get_unit_states():
                        attack_unit_states.remove(unit_state)
                    res = self.vuln.battle_formula(attack_units=[self.game.rules.get_unit(us.type_index) for us in attack_unit_states],
                                                   defense_units=[self.game.rules.get_unit(us.type_index) for us in self.vuln.territories[territory_name][self.game.rules.enemy_team(player=self.player)]])
                    if res >= threshold:
                        can_remove.append(unit_stack)
                    for unit_state in unit_stack.get_unit_states():
                        attack_unit_states.append(unit_state)

                min_defense, to_leave_behind = 99999, None
                for unit_stack in can_remove:
                    if not unit_stack.is_transport:
                        if self.vuln.get_estimated_defensibility(unit_stack.territory, defender=self.player) < min_defense:
                            min_defense = self.vuln.get_estimated_defensibility(unit_stack.territory, defender=self.player)
                            to_leave_behind = unit_stack
                if not to_leave_behind:
                    break

                for unit_state in to_leave_behind.get_unit_states():
                    attack_unit_states.remove(unit_state)
                unit_stack_list.remove(to_leave_behind)
                dont_move.append(to_leave_behind)

        for unit_stack, territory_name in theoretical_attack.items():
            if territory_name:
                for unit_state in unit_stack.get_unit_states():
                    self.game.state_dict[territory_name].unit_state_list.remove(unit_state)
                if unit_stack.is_transport:
                    for i in range(len(unit_stack.land_unit_states)):
                        self.game.state_dict[unit_stack.land_unit_territories[i]].unit_state_list.append(unit_stack.land_unit_states[i])
                else:
                    self.game.state_dict[unit_stack.territory].unit_state_list.append(unit_stack.unit_state)

        for unit_stack in dont_move:
            theoretical_attack[unit_stack] = ''

        self.vuln.invalid = True

        # Return a list of the moves to do
        moves_to_do = list()
        used_units = list()
        # Do non-amphibious units first
        for unit_stack, target in theoretical_attack.items():
            if target:
                if not unit_stack.is_transport:
                    moves_to_do.append([unit_stack.unit_state, unit_stack.territory, target])
                    used_units.append(unit_stack.unit_state)
        # Then do amphibious units
        for unit_stack, target in theoretical_attack.items():
            if target:
                if unit_stack.is_transport:
                    # TODO (Brett): Any unit that can attack both amphibiously and by land will default to doing the land movement, which is not optimal
                    # Remove any units that have already been used
                    unit_stack.remove_units(used_units)
                    # Get a valid path for the transport
                    if len(unit_stack.land_units) == 0:
                        continue
                    elif len(unit_stack.land_units) == 1:
                        valid_paths = self.game.check_unit_transport(unit_stack.land_unit_states[0], unit_stack.land_unit_territories[0],
                                                                    unit_stack.transport_state, unit_stack.transport_territory, target, 3, True)
                    else:
                        valid_paths = self.game.check_two_unit_transport(unit_stack.land_unit_states[0], unit_stack.land_unit_territories[0],
                                                                         unit_stack.land_unit_states[1], unit_stack.land_unit_territories[1],
                                                                         unit_stack.transport_state, unit_stack.transport_territory, target, 3, True)
                    shortest_path = min(valid_paths, key=len)
                    unit_1_picked_up = unit_stack.land_unit_states[0].attached_to is not None
                    unit_2_picked_up = len(unit_stack.land_unit_states) < 2 or unit_stack.land_unit_states[1].attached_to is not None
                    idx = 0
                    water_target = self.game.rules.board[target].is_water
                    while True:
                        if not unit_1_picked_up and unit_stack.land_unit_territories[0] in self.game.rules.board[shortest_path[idx]].neighbors:
                            moves_to_do.append([unit_stack.land_unit_states[0], unit_stack.land_unit_territories[0], shortest_path[idx], unit_stack.transport_state])
                            unit_1_picked_up = True
                        elif not unit_2_picked_up and unit_stack.land_unit_territories[1] in self.game.rules.board[shortest_path[idx]].neighbors:
                            moves_to_do.append([unit_stack.land_unit_states[1], unit_stack.land_unit_territories[1], shortest_path[idx], unit_stack.transport_state])
                            unit_2_picked_up = True
                        elif unit_1_picked_up and unit_2_picked_up \
                                and ((water_target and target == shortest_path[idx])
                                     or (not water_target and target in self.game.rules.board[shortest_path[idx]].neighbors)):
                            if not water_target:
                                for i in range(len(unit_stack.land_unit_states)):
                                    moves_to_do.append([unit_stack.land_unit_states[i], shortest_path[idx], target])
                            break
                        else:
                            moves_to_do.append([unit_stack.transport_state, shortest_path[idx], shortest_path[idx + 1]])
                            idx += 1

        return moves_to_do


class Vulnerability:
    def __init__(self, game, init_territories=True):
        self.game = game
        self.territories = dict()
        self.transport_data = list()
        self.invalid = True
        if init_territories:
            self.update()

    def get_attackable_territories(self, unit_state, territory_name):
        unit = self.game.rules.get_unit(unit_state.type_index)

        # AA guns can't attack, and ignore transported units for now
        if unit.name == 'aa' or unit_state.attached_to:
            return list()

        # Get amount of available movement (planes get one less because they need to land)
        available_movement = unit.movement - unit_state.moves_used - (unit.unit_type == 'air')

        # BFS to get all territories within range
        within_range = [territory_name]
        idx, dist, next_dist_idx = 0, 0, 1
        while dist < available_movement:
            for neighbor in self.game.rules.board[within_range[idx]].neighbors:
                if neighbor not in within_range:
                    within_range.append(neighbor)
            idx += 1
            if idx == next_dist_idx:
                dist += 1
                next_dist_idx = len(within_range)

        # Use calc_movement to see which of these territories can be attacked
        attackable = [territory for territory in within_range if
                      self.game.calc_movement(unit_state, territory_name, territory, phase=3)[0] >= 0]

        # Done with non-transports
        if unit_state.type_index != 5:
            return attackable

        # See what territories can be unloaded at
        reachable_land = set()
        for territory in attackable:
            for neighbor in self.game.rules.board[territory].neighbors:
                reachable_land.add(neighbor)

        # See what types of units can be picked up
        pick_up_infantry, pick_up_other = True, True
        if len(unit_state.attached_units) == 2:
            pick_up_infantry, pick_up_other = False, False
        elif len(unit_state.attached_units) == 1:
            pick_up_other = unit_state.attached_units[0].type_index == 0
            pick_up_infantry = True

        # Find all units that can be picked up, and see which territories they can attack
        possible_units = dict()
        # Start with already attached units
        for land_unit_state in unit_state.attached_units:
            for territory in reachable_land:
                if land_unit_state not in possible_units:
                    possible_units[land_unit_state] = [territory_name, list()]
                possible_units[land_unit_state][1].append(territory)
        # Then check all other units
        if pick_up_infantry or pick_up_other:
            for territory in reachable_land:
                for land_unit_state in self.game.state_dict[territory].unit_state_list:
                    if land_unit_state.owner == unit_state.owner and land_unit_state.type_index < 3:
                        if (land_unit_state.type_index == 0 and pick_up_infantry) or pick_up_other:
                            for goal_territory in reachable_land:
                                if self.game.check_unit_transport(land_unit_state, territory, unit_state, territory_name, goal_territory, 3):
                                    if land_unit_state not in possible_units:
                                        possible_units[land_unit_state] = [territory, list()]
                                    possible_units[land_unit_state][1].append(goal_territory)
        # Get all possible pairs of units
        all_unit_states = list(possible_units.keys())
        self.transport_data.append(list())
        for i in range(len(all_unit_states)):
            for j in range(i+1, len(all_unit_states)):
                unit_state_1, unit_state_2 = all_unit_states[i], all_unit_states[j]
                territory_1, territory_2 = possible_units[unit_state_1][0], possible_units[unit_state_2][0]
                goal_territories_1, goal_territories_2 = possible_units[unit_state_1][1], possible_units[unit_state_2][1]
                goals = set(goal_territories_1).intersection(goal_territories_2)
                unit_stack = UnitStack(self.game, unit_state, territory_name, [unit_state_1, unit_state_2], [territory_1, territory_2])
                for goal_territory in goals:
                    if self.game.check_two_unit_transport(unit_state_1, territory_1, unit_state_2, territory_2,
                                                          unit_state, territory_name, goal_territory, phase=3):
                        unit_stack.possible_goals.append(goal_territory)
                self.transport_data[-1].append(unit_stack)
            unit_stack = UnitStack(self.game, unit_state, territory_name, [all_unit_states[i]], [possible_units[all_unit_states[i]][0]])
            unit_stack.possible_goals = possible_units[all_unit_states[i]][1]

    def place_unit(self, unit_state, territory_name):
        # This unit isn't actually placed here - it only counts towards defense. Make sure update() is called in between phases
        self.territories[territory_name][self.game.rules.teams[unit_state.owner]].append(
            self.game.rules.get_unit(unit_state.type_index))

    def update(self):
        # updates the territory dict to accurately represent the boardstate.

        keys = ['America', 'Britain', 'Russia', 'Germany', 'Japan', 'Axis', 'Allies']
        self.territories = {territory_name: {player: list() for player in keys} for territory_name in
                            self.game.state_dict.keys()}
        for territory_name in self.territories.keys():
            for unit_state in self.game.state_dict[territory_name].unit_state_list:
                player = unit_state.owner
                if unit_state.type_index == 5:  # Transports (and their attached units) are different
                    self.get_attackable_territories(unit_state, territory_name)
                elif unit_state.type_index != 4:  # Ignores factories
                    if unit_state.type_index != 3:  # AA guns can only defend
                        unit_stack = UnitStack(self.game, unit_state, territory_name)
                        for ter in self.get_attackable_territories(unit_state, territory_name):
                            if unit_stack not in self.territories[ter][player]:
                                self.territories[ter][player].append(unit_stack)
                    if not unit_state.attached_to:
                        self.territories[territory_name][self.game.rules.teams[player]].append(unit_state)
        # Deal with transports
        # TODO (Future): The way this deals with transports in not optimal. Currently just takes strongest unit pairs and doesn't consider anything else
        while self.transport_data:
            self.transport_data.sort(key=len)
            unit_stack_list = self.transport_data.pop(0)
            if unit_stack_list:
                best_stack = max(unit_stack_list, key=lambda x: x.get_attack_power())
                for i in range(len(self.transport_data)):
                    for j in range(len(self.transport_data[i]) - 1, -1, -1):
                        for unit_state in best_stack.land_unit_states:
                            if unit_state in self.transport_data[i][j].land_unit_states:
                                self.transport_data[i].pop(j)
                                break
                for goal in best_stack.possible_goals:
                    self.territories[goal][best_stack.transport_state.owner].append(best_stack)
        self.invalid = False

    def battle_formula(self, attack_units=None, defense_units=None):
        # Implements a formula representing the rough approximation of a battle without taking the time to calculate 500 simulations

        if self.invalid:
            self.update()
        # James' Formula:
        #  For each side:
        #   total_power_of_this_side + (average_power_of_both_sides) * number_of_units
        #   + (standard_deviation * (0.5 + number_of_units)/4.5)
        num_attackers, num_defenders = len(attack_units), len(defense_units)
        if num_defenders == 0:
            if num_attackers:
                return 2
            else:
                return 0
        defense_powers = [unit.defense for unit in defense_units]
        # Account for extra attack power of artillery paired with infantry
        attack_powers = list()
        artillery_infantry_pairs = min(len([unit for unit in attack_units if unit.name == 'artillery']),
                                       len([unit for unit in attack_units if unit.name == 'infantry']))
        for unit in attack_units:
            if unit.name == 'infantry' and artillery_infantry_pairs > 0:
                attack_powers.append(unit.attack + 1)
                artillery_infantry_pairs -= 1
            else:
                attack_powers.append(unit.attack)

        total_attack_power, total_defense_power = sum(attack_powers), sum(defense_powers)
        avg_power = (total_attack_power + total_defense_power) / (num_attackers + num_defenders)
        attack_stdev = 0 if num_attackers < 2 else stdev(attack_powers)
        defense_stdev = 0 if num_defenders < 2 else stdev(defense_powers)

        attack_value = total_attack_power + (num_attackers * avg_power) + (attack_stdev * (0.5 + num_attackers) / 4.5)
        defense_value = total_defense_power + (num_defenders * avg_power) + (defense_stdev * (0.5 + num_defenders) / 4.5)

        return attack_value - defense_value

    def get_estimated_defensibility(self, territory_name, defender=''):
        if defender in self.game.rules.teams.keys():
            defender = self.game.rules.teams[defender]
        defense_values = list()
        for unit_state in self.game.state_dict[territory_name].unit_state_list:
            if self.game.rules.teams[unit_state.owner] == defender and not unit_state.attached_to \
                    and (unit_state.type_index < 3 or unit_state.type_index > 5):
                defense_values.append(self.game.rules.get_unit(unit_state.type_index).defense)
        defense_stdev = 0 if len(defense_values) < 2 else stdev(defense_values)
        # Use same formula as normal, but use defense_power/num_defenders + 1/2 instead of average power
        return 2 * sum(defense_values) + len(defense_values)/2 + (defense_stdev * (0.5 + len(defense_values)) / 4.5)

    def get_vulnerability(self, territory_name, theoretical_append=None, attacker='', defender=''):
        if not theoretical_append:
            theoretical_append = list()
        if self.invalid:
            self.update()
        if defender in self.game.rules.teams.keys():
            defender = self.game.rules.teams[defender]
        elif not defender:
            if not attacker:
                defender = self.game.rules.teams[self.game.turn_state.player]
            else:
                defender = self.game.rules.enemy_team(player=attacker)

        if attacker:
            attackers = [attacker]
        else:
            attacker_team = self.game.rules.enemy_team(team=defender)
            attackers = [player for player, team in self.game.rules.teams.items() if team == attacker_team]

        # Get attacking and defending units
        attacking_units = list()
        used_units = list()
        for attacking_player in attackers:
            # Get all units that can attack this territory
            attacking_units.append([])
            for unit_stack in self.territories[territory_name][attacking_player]:
                if not unit_stack.is_transport:
                    if unit_stack.unit_state not in used_units:
                        attacking_units[-1].append(unit_stack.unit)
                        used_units.append(unit_stack.unit_state)
                else:
                    for i in range(len(unit_stack.land_units)):
                        if unit_stack.land_unit_states[i] not in used_units:
                            attacking_units[-1].append(unit_stack.land_units[i])
                            used_units.append(unit_stack.land_unit_states[i])

        defending_units = [self.game.rules.get_unit(unit_state.type_index)
                           for unit_state in (self.territories[territory_name][defender] + theoretical_append)]

        values = [self.battle_formula(attack_units, defending_units) for attack_units in attacking_units]
        worst_case = max(values)
        return worst_case

    def is_vulnerable(self, territory_name, risk_tolerances, theoretical_append=None, attacker='', defender=''):
        vulnerability = self.get_vulnerability(territory_name, theoretical_append, attacker, defender)
        return vulnerability >= risk_tolerances[territory_name]


class Build:
    """
    AI decides upon priority values. Purchases are determined by the ratio of each priority value to the sum times the total ipc.
    """

    def __init__(self, game):  # game.turn_state, etc.
        self.game = game
        self.player = self.game.turn_state.player
        self.ipc = self.game.players[self.player].ipc

        # TODO (Future): Implement AI building factories
        self.prioritization_list = []
        self.prioritization_list.append(['tech_token', 0])  # never use this one
        self.prioritization_list.append(['battleship', 0])  # 1
        self.prioritization_list.append(['factory', 0])  # 2
        self.prioritization_list.append(['carrier', 0])  # 3
        self.prioritization_list.append(['cruiser', 0])  # 4
        self.prioritization_list.append(['bomber', 0])  # 5
        self.prioritization_list.append(['carrier_fighter', 0])  # same here
        self.prioritization_list.append(['fighter', 0])  # 7
        self.prioritization_list.append(['destroyer', 0])  # 8
        self.prioritization_list.append(['transport', 0])  # 9
        self.prioritization_list.append(['transportable_units', 0])  # only positive if no adjacent units
        self.prioritization_list.append(['sub', 0])  # 11
        self.prioritization_list.append(['tank', 0])  # 12
        self.prioritization_list.append(['aa', 0])  # 13
        self.prioritization_list.append(['artillery', 0])  # 14
        self.prioritization_list.append(['infantry', 0])  # 15

    def build_units(self):
        # sea
        self.sea_defense_sum = self.prioritization_list[1][1] + self.prioritization_list[3][1] \
                               + self.prioritization_list[4][1] + self.prioritization_list[6][1] + \
                               self.prioritization_list[8][1]
        self.sea_sum = self.sea_defense_sum + self.prioritization_list[9][1] + self.prioritization_list[10][1] \
                       + self.prioritization_list[11][1]

        # land. These may prove vistigial
        self.land_defense_sum = self.prioritization_list[12][1] + self.prioritization_list[13][1] \
                                + self.prioritization_list[14][1] + self.prioritization_list[15][1] + \
                                self.prioritization_list[7][1]
        self.land_sum = self.land_defense_sum + self.prioritization_list[2][1] + self.prioritization_list[5][
            1]  # Note that factories are part of land sum

        self.priority_sum = self.land_sum + self.sea_sum

        self.purchased_unit_state_list = []
        # purchasing
        for unit_priority in self.prioritization_list:
            priority_ratio = unit_priority[1] / self.priority_sum
            allotted_ipc = priority_ratio * self.ipc

            if unit_priority[0] == 'carrier_fighter':
                cost = 10
                num_purchased = round(allotted_ipc / cost)
                if num_purchased >= 1:
                    for i in range(num_purchased):
                        if (self.ipc - cost) >= 0:
                            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 11))
                            self.ipc -= cost

            elif unit_priority[0] == 'transportable_units':
                cost = 7  # transportable units in this context are always infantry and artillery
                num_purchased = round(allotted_ipc / cost)
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
                        num_purchased = round(allotted_ipc / cost)
                        if num_purchased >= 1:
                            for i in range(num_purchased):
                                if (self.ipc - cost) >= 0:
                                    self.purchased_unit_state_list.append(
                                        BoardState.UnitState(self.player, self.game.rules.units.index(unit)))
                                    self.ipc = self.ipc - cost
        while self.ipc >= 3:  # Hopefully the AI does not give bad priorities else we run out of placement space
            self.purchased_unit_state_list.append(BoardState.UnitState(self.player, 0))  # infantry
            self.ipc -= 3

        self.game.purchased_units[self.player] += self.purchased_unit_state_list[:]

    def prioritizer(self, prioritization, strength):
        # Something the AI can call if it wants to change the build priority of a unit
        for arr in self.prioritization_list:
            if arr[0] == prioritization:
                arr[1] = strength


class BattleCalculator:
    """
    tool for the AI to determine how a battle WOULD turn out without actually changing the GameState
    """

    # account for land units on transpots in ipc swing

    def __init__(self, game, attacking_player, unit_state_list, ai_importance, territory_name,
                 attacker_one_land_unit_remaining=False, attacker_prioritize_unit_index=-1, defender_prioritize_unit_index=-1):
        self.unit_state_list = unit_state_list
        self.territory_name = territory_name
        self.ipc_swing = 0
        self.game = game
        self.embattled_territory_value = game.rules.board[territory_name].ipc
        self.victory_chance = 0  # consider both amalgamation and victory chance alone
        self.tie_chance = 0
        self.one_land = attacker_one_land_unit_remaining
        self.attack_priority = attacker_prioritize_unit_index
        self.defend_priority = defender_prioritize_unit_index
        self.attacking_player = attacking_player
        self.battler = Battles(self.game, ai_importance)
        self.battle_sim(500)
        # TODO (Future): The net ipc swing formula probably isn't optimal
        self.net_ipc_swing = self.ipc_swing + ((self.embattled_territory_value + 1) * (ai_importance[territory_name] + 1) * self.victory_chance)

    def battle_sim(self, run_count):
        damages = [unit_state.damaged for unit_state in self.unit_state_list]
        attack_casualty_order, defense_casualty_order = self.battler.get_casualty_orders(self.unit_state_list)
        attack_ipcs, defense_ipcs = self.battler.get_total_ipcs(attack_casualty_order), self.battler.get_total_ipcs(defense_casualty_order)
        attack_ipcs_left, defense_ipcs_left = 0, 0

        if not attack_casualty_order:
            self.victory_chance = 0
            self.tie_chance = (not defense_casualty_order)
            self.ipc_swing = 0
        elif not defense_casualty_order:
            self.victory_chance = 1
            self.tie_chance = 0
            self.ipc_swing = 0
        else:
            # Run simulations
            for _ in range(run_count):
                # TODO (Later): Considering retreats exceeds the maximum recursion depth. Oops.
                result = self.battler.battler(self.unit_state_list[:], self.territory_name, ignore_retreats_and_movement=True)
                for i in range(len(damages)):
                    self.unit_state_list[i].damaged = damages[i]
                if result > 0:
                    self.victory_chance += 1
                    attack_ipcs_left += result
                elif result < 0:
                    defense_ipcs_left -= result
                else:
                    self.tie_chance += 1

            # Get needed values
            self.victory_chance /= run_count
            self.tie_chance /= run_count
            avg_attack_ipcs_lost = attack_ipcs - (attack_ipcs_left / run_count)
            avg_defense_ipcs_lost = defense_ipcs - (defense_ipcs_left / run_count)
            self.ipc_swing = avg_defense_ipcs_lost - avg_attack_ipcs_lost


class CombatMove:
    def __init__(self, game, ai_importances):
        self.game = game
        self.importances = ai_importances

    def can_move(self, unit_state, current_territory, goal_territory):
        return self.game.calc_movement(unit_state, current_territory, goal_territory)[0] >= 0

    def move_unit(self, unit_state, current_territory, goal_territory, transport=None, bombing=False, bombarding=False):
        dist, path = self.game.calc_movement(unit_state, current_territory, goal_territory)
        if dist == -1:
            return False

        current_territory_state, goal_territory_state = self.game.state_dict[current_territory], \
                                                        self.game.state_dict[goal_territory]
        current_territory_state.unit_state_list.remove(unit_state)
        for other_unit_state in unit_state.attached_units:
            current_territory_state.unit_state_list.remove(other_unit_state)
        unit = self.game.rules.get_unit(unit_state.type_index)
        print('  - Moved', unit.name, 'from', current_territory, 'to', goal_territory)
        if unit.name == 'transport':
            print('    - Unit is carrying', [self.game.rules.get_unit(land_unit.type_index).name for land_unit in unit_state.attached_units])

        # AA guns
        if self.game.rules.aa_flyover and unit.unit_type == 'air':
            # Check for aa guns in each territory
            for ter_name in path:
                territory_state = self.game.state_dict[ter_name]
                for other_unit_state in territory_state.unit_state_list:
                    if other_unit_state.type_index == 3 and self.game.rules.teams[other_unit_state.owner] != \
                            self.game.rules.teams[unit_state.owner]:
                        # Can only shoot 3 times
                        if other_unit_state.shots_taken < 3:
                            other_unit_state.shots_taken += 1
                            if random.randint(1, 6) == 1:
                                print('    - Unit shot down by AA gun in', ter_name)
                                return True

        # Bombing factories
        if bombing and unit.name == 'bomber':
            unit_state.retreated = True
            for other_unit_state in goal_territory_state.unit_state_list:
                if other_unit_state.type_index == 4 and other_unit_state.shots_taken < 3 and \
                        self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
                    dmg = random.randint(1, 6)
                    print('    - Unit shot factory for', dmg, 'damage')
                    self.game.players[unit_state.owner].ipc -= dmg
                    other_unit_state.shots_taken += 1
                    if random.randint(1, 6) == 1:
                        print('    - Unit shot down by factory')
                        current_territory_state.unit_state_list.remove(unit_state)
                        return True

        # Update unit
        captured_territories = list()
        # Check for tank blitzes
        if unit.name == 'tank' and dist == 2:
            if self.game.rules.teams[self.game.state_dict[path[1]].owner] != self.game.rules.teams[unit_state.owner]:
                print('    - Blitzed with tank')
                captured_territories.append(path[1])
        # And check if territory it went to is empty
        if unit.unit_type == 'land' and not self.game.rules.board[goal_territory].is_water\
                and self.game.rules.teams[goal_territory_state.owner] != self.game.rules.teams[unit_state.owner]:
            enemy_units = False
            for other_unit_state in goal_territory_state.unit_state_list:
                if other_unit_state.type_index != 4 and self.game.rules.teams[other_unit_state.owner] != self.game.rules.teams[unit_state.owner]:
                    enemy_units = True
                    break
            if enemy_units:
                captured_territories.append(goal_territory)
        # Then capture these territories
        for ter in captured_territories:
            ter_state = self.game.state_dict[ter]
            ter_state.just_captured = True
            # Check if original owner has capital and is ally, if so give it back to them
            original_owner = self.game.rules.board[ter].original_owner
            capital = self.game.players[original_owner].capital
            if self.game.rules.teams[unit_state.owner] == self.game.rules.teams[original_owner] \
                    and (self.game.state_dict[capital].owner == original_owner or ter == capital):
                ter_state.owner = original_owner
            else:
                ter_state.owner = unit_state.owner
                if self.game.rules.board[ter].is_capital:  # if the territory is someone's capital
                    original_owner = self.game.rules.board[ter].original_owner
                    self.game.players[unit_state.owner].ipc += self.game.players[original_owner].ipc
                    self.game.players[original_owner].ipc = 0

        goal_territory_state.unit_state_list.append(unit_state)
        for other_unit_state in unit_state.attached_units:
            goal_territory_state.unit_state_list.append(other_unit_state)
        unit_state.moves_used += dist
        if not unit_state.moved_from:
            unit_state.moved_from = path
        else:
            unit_state.moved_from += path[1:]
        if unit_state.attached_to:
            print('    - Unit was on transport carrying', [self.game.rules.get_unit(land_unit.type_index).name for land_unit in unit_state.attached_to.attached_units])
            unit_state.attached_to.attached_units.remove(unit_state)
            unit_state.attached_to.moves_used = 2
            unit_state.attached_to = None
            # Bombarding
            if bombarding:
                # Check if there are enemy units to bombard
                enemy_units = False
                for other_unit_state in goal_territory_state.unit_state_list:
                    if other_unit_state.type_index != 4 and self.game.rules.teams[other_unit_state.owner] != \
                            self.game.rules.teams[unit_state.owner]:
                        enemy_units = True
                        break
                if enemy_units:
                    # Check for battleships to bombard with
                    for other_unit_state in current_territory_state.unit_state_list:
                        if other_unit_state.type_index == 10 and \
                                self.game.rules.teams[other_unit_state.owner] == self.game.rules.teams[unit_state.owner]:
                            if not other_unit_state.shots_taken:
                                other_unit_state.shots_taken += 1
                                unit_state.moves_used = unit.movement
                                other_unit_state.retreated = True
                                if random.randint(1, 6) <= 4:
                                    _, defense_order = Battles(self.game, self.importances).get_casualty_orders(goal_territory_state.unit_state_list)
                                    goal_territory_state.unit_state_list.remove(defense_order[0])
                                    print('    - Battleship successfully bombarded enemy', self.game.rules.get_unit(defense_order[0].type_index))
                                else:
                                    print('    - Battleship unsuccessfully bombarded')

        if self.game.rules.board[goal_territory].is_water and unit.unit_type == 'land':
            if transport and transport.type_index == 5 and (len(transport.attached_units) == 0 or (len(transport.attached_units) == 1 and (transport.attached_units[0].type_index == 0 or unit.name == 'infantry'))):
                # If given which transport it attaches to
                unit_state.attached_to = transport
                transport.attached_units.append(unit_state)
            else:
                # Attach to transport
                if unit.name == 'infantry':
                    # Look for open infantry spots
                    for other_unit_state in goal_territory_state.unit_state_list:
                        if other_unit_state.type_index == 5:
                            if len(other_unit_state.attached_units) == 0 or \
                                    (len(other_unit_state.attached_units) == 1 and other_unit_state.attached_units[0].type_index != 0):
                                unit_state.attached_to = other_unit_state
                                other_unit_state.attached_units.append(unit_state)
                                break
                # Look for any available spot
                if not unit_state.attached_to:
                    for other_unit_state in goal_territory_state.unit_state_list:
                        if other_unit_state.type_index == 5:
                            if len(other_unit_state.attached_units) == 0:
                                unit_state.attached_to = other_unit_state
                                other_unit_state.attached_units.append(unit_state)
                                break
                            elif len(other_unit_state.attached_units) == 1:
                                if unit.name == 'infantry' or other_unit_state.attached_units[0].type_index == 0:
                                    unit_state.attached_to = other_unit_state
                                    other_unit_state.attached_units.append(unit_state)
                                    break
            if len(unit_state.attached_to.attached_units) == 1:
                print('    - Attached unit to empty transport')
            else:
                name = self.game.rules.get_unit(unit_state.attached_to.attached_units[0].type_index).name
                print('    - Attached unit to transport carrying', name)
        return True

    def do_combat_move(self, risk_tolerances):
        # TODO (Future): Currently can't bomb factories
        attackable = Attackable(self.game, self.game.turn_state.player, self.importances, risk_tolerances)
        moves_to_do = attackable.get_best_attacks()
        # Move battleships first
        for arr in moves_to_do:
            if arr[0].type_index == 10:
                if not self.move_unit(arr[0], arr[1], arr[2], bombarding=False):
                    print("Tried to make an invalid move:", arr[0].type_index, 'from', arr[1], 'to', arr[2])
        # Now any battleships that didn't need to move can bombard
        for arr in moves_to_do:
            if arr[0].type_index != 10:
                transport = None if len(arr) < 4 else arr[3]
                if not self.move_unit(arr[0], arr[1], arr[2], transport=transport, bombarding=True):
                    print("Tried to make an invalid move:", arr[0].type_index, 'from', arr[1], 'to', arr[2])


class Battles:
    def __init__(self, game, ai_importance):
        self.game = game

        self.territory_states = game.state_dict
        self.player = game.turn_state.player
        self.team = game.rules.teams[self.player]

        self.importances = ai_importance
        self.retreating = False
        self.kamikaze = False
        self.battle_calculator = None
        # TODO (Future): Have the AI decide on retreating and kamikaze values

        self.enemy_team = self.game.rules.enemy_team(player=self.player)

    def resolve_all_battles(self):
        for territory_key, territory_state in self.territory_states.items():
            result = self.battler(territory_state.unit_state_list, territory_key, output=True)
            if result is None:
                continue
            elif result > 0:
                print('    - Won battle\n')
                territory_state.just_captured = True
                # Set new owner of the territory
                original_owner = self.game.rules.board[territory_key].original_owner
                if original_owner in self.game.players.keys():
                    capital = self.game.players[original_owner].capital
                    # Return the territory to original owner, if ally
                    if self.game.rules.teams[self.player] == self.game.rules.teams[original_owner] \
                            and (self.game.state_dict[capital].owner == original_owner or territory_key == capital):
                        territory_state.owner = original_owner
                    # Otherwise goes to player
                    else:
                        territory_state.owner = self.player
                        if self.game.rules.board[territory_key].is_capital:  # if the territory is someone's capital
                            self.game.players[self.player].ipc += self.game.players[original_owner].ipc
                            self.game.players[original_owner].ipc = 0
            elif result < 0:
                print('    - Lost battle\n')
            else:
                print('    - Tied battle\n')

    def choose_retreat_spot(self, unit_state, retreat_options, current_territory):
        if len(retreat_options) == 0:
            return None  # Should never reach here, but just in case
        elif len(retreat_options) == 1:
            return list(retreat_options)[0]
        vuln = Vulnerability(self.game, init_territories=False)
        return min(retreat_options, key=lambda x: vuln.get_estimated_defensibility(x, unit_state.owner) / self.importances[x])

    def sub_submerger(self, friendly_units, enemy_units, attacking):
        # Can't submerge if you don't have unsubmerged subs
        if 6 not in [unit_state.type_index for unit_state in friendly_units if not unit_state.retreated]:
            return

        # Can't submerge if there are destroyers
        if 7 in [unit_state.type_index for unit_state in enemy_units]:
            return

        # Values of -5 and 1 here are arbitrary thresholds
        if attacking:
            submerge = (Vulnerability(self.game, False).battle_formula([self.game.rules.get_unit(us.type_index) for us in friendly_units],
                                                                       [self.game.rules.get_unit(us.type_index) for us in enemy_units])) <= -5
        else:
            submerge = (Vulnerability(self.game, False).battle_formula([self.game.rules.get_unit(us.type_index) for us in enemy_units],
                                                                       [self.game.rules.get_unit(us.type_index) for us in friendly_units])) >= 1

        if submerge:
            for i in range(len(friendly_units)-1, -1, -1):
                if friendly_units[i].type_index == 6:
                    friendly_units[i].retreated = True
                    print('    - Retreated', friendly_units.pop(i).owner, 'submarine')

    def battler(self, unit_state_list, territory_name, ignore_retreats_and_movement=False, output=False):
        attacker_order, defender_order = self.get_casualty_orders(unit_state_list, self.game.rules.board[territory_name].ipc > 0)
        if not attacker_order or not defender_order:
            return None
        if output:
            print('  - Resolving battle in', territory_name)

        land_retreat_options, water_retreat_options = set(), set()
        if not ignore_retreats_and_movement:
            # Submerge subs before battle if necessary
            self.sub_submerger(attacker_order, defender_order, True)
            self.sub_submerger(defender_order, attacker_order, False)

            # Get all territories that can be retreated to
            for unit_state in attacker_order:
                if unit_state.type_index <= 10:
                    # Non-retreated land and sea units use up all movement
                    if not unit_state.retreated and not ignore_retreats_and_movement:
                        unit_state.moves_used = self.game.rules.get_unit(unit_state.type_index).movement
                    # Also get possible retreat locations for the attack
                    if len(unit_state.moved_from) >= 2:
                        if unit_state.type_index <= 4:
                            land_retreat_options.add(unit_state.moved_from[-2])
                        else:
                            water_retreat_options.add(unit_state.moved_from[-2])

        # Run battle one round at time
        round_num = 1
        already_retreated = ignore_retreats_and_movement
        while attacker_order and defender_order:
            if output:
                print('    - Running round', round_num)
            round_num += 1

            attack_destroyer = (7 in [unit_state.type_index for unit_state in attacker_order])
            defense_destroyer = (7 in [unit_state.type_index for unit_state in defender_order])

            # Check to see if subs should submerge
            if not defense_destroyer and not ignore_retreats_and_movement:
                self.sub_submerger(attacker_order, defender_order, True)
            if not attack_destroyer and not ignore_retreats_and_movement:
                self.sub_submerger(defender_order, attacker_order, False)

            attack_power, attack_sub_power = self.get_total_power(attacker_order, False)
            defense_power, defense_sub_power = self.get_total_power(defender_order, True)

            if not attack_power and not attack_sub_power and not defense_power and not defense_power:
                break

            # Subs attack first, and the killed units can't shoot back
            if not defense_destroyer and attack_sub_power:
                self.kill_multiple_units(unit_state_list, defender_order, self.num_casualties(attack_sub_power), output, True)
            if not attack_destroyer and defense_sub_power:
                self.kill_multiple_units(unit_state_list, attacker_order, self.num_casualties(defense_sub_power), output, True)
                defense_power, defense_sub_power = self.get_total_power(defender_order, True)
                defense_sub_power = 0
            if not defense_destroyer and attack_sub_power:
                attack_power, attack_sub_power = self.get_total_power(attacker_order, False)
                attack_sub_power = 0

            # Then the rest of the units attack, including subs if a destroyer is present
            self.kill_multiple_units(unit_state_list, defender_order, self.num_casualties(attack_sub_power), output, True)
            self.kill_multiple_units(unit_state_list, defender_order, self.num_casualties(attack_power), output)
            self.kill_multiple_units(unit_state_list, attacker_order, self.num_casualties(defense_sub_power), output, True)
            self.kill_multiple_units(unit_state_list, attacker_order, self.num_casualties(defense_power), output)

            # Check if need to retreat
            if not already_retreated and defender_order and attacker_order:
                self.battle_calculator = BattleCalculator(self.game, self.player, unit_state_list, self.importances, territory_name)
                if (self.battle_calculator.net_ipc_swing < 0) and not self.kamikaze:
                    self.retreating = True

            # Retreat units
            if attacker_order and defender_order and self.retreating and not already_retreated and (land_retreat_options or water_retreat_options):
                if output:
                    print('    - Retreated units')
                already_retreated = True
                self.retreating = False
                for i in range(len(attacker_order)-1, -1, -1):
                    # Amphibious units can't retreat
                    if not unit_state.retreated and (self.game.rules.board[territory_name].is_water or not self.game.rules.board[attacker_order[i].moved_from[-2]].is_water):
                        unit_state = attacker_order.pop(i)
                        unit_state.retreated = True
                        retreat_choice = None
                        if unit_state.type_index < 5:
                            retreat_choice = self.choose_retreat_spot(unit_state, land_retreat_options, territory_name)
                        elif unit_state.type_index <= 10:
                            retreat_choice = self.choose_retreat_spot(unit_state, water_retreat_options, territory_name)
                        if retreat_choice:
                            self.game.state_dict[retreat_choice].unit_state_list.append(unit_state)
                            self.game.state_dict[territory_name].unit_state_list.remove(unit_state)
                            if output:
                                print('    - Retreated ' + self.game.rules.get_unit(unit_state.type_index).name + ' to ' + retreat_choice)

        return self.get_total_ipcs(attacker_order) - self.get_total_ipcs(defender_order)

    def kill_multiple_units(self, unit_state_list, casualty_order, num_casualties, output, sub_kills=False):
        while num_casualties > 0:
            attackable_units = [unit_state for unit_state in casualty_order if not sub_kills or unit_state.type_index <= 10]
            if attackable_units:
                self.kill_one_unit(attackable_units[0], unit_state_list, output)
                casualty_order.remove(attackable_units[0])
            else:
                break
            num_casualties -= 1

    def kill_one_unit(self, unit_state, unit_state_list, output):
        if unit_state.type_index == 10 and unit_state.damaged == 0:
            if output:
                print('      - ' + unit_state.owner + ' battleship took one hit')
            unit_state.damaged = 1
        else:
            if output:
                print('      -', unit_state.owner, self.game.rules.get_unit(unit_state.type_index).name, 'died')
            unit_state_list.remove(unit_state)
            for land_unit in unit_state.attached_units:
                if output:
                    print('      - Attached ', land_unit.owner, self.game.rules.get_unit(land_unit.type_index).name, 'died')
                unit_state_list.remove(land_unit)

    def num_casualties(self, power):
        return power // 6 + (random.randint(1, 6) <= power % 6)

    def get_total_power(self, unit_state_list, attacking):
        power, sub_power = 0, 0
        num_infantry, num_artillery = 0, 0
        for i in range(len(unit_state_list)):
            if unit_state_list[i] not in unit_state_list[:i]:  # Don't count battleships twice
                index = unit_state_list[i].type_index
                if attacking:
                    num_infantry += (index == 0)
                    num_artillery += (index == 1)
                    if index == 6:
                        sub_power += self.game.rules.get_unit(index).attack
                    else:
                        power += self.game.rules.get_unit(index).attack
                else:
                    if index == 6:
                        sub_power += self.game.rules.get_unit(index).defense
                    else:
                        power += self.game.rules.get_unit(index).defense
        power += min(num_infantry, num_artillery)
        return power, sub_power

    def get_casualty_orders(self, unit_state_list, one_land_unit_remaining=False, attacker_priority_unit=-1, defender_priority_unit=-1):
        enemy_team = self.game.rules.enemy_team(player=self.player)
        defending_players = [player for player, team in self.game.rules.teams.items() if team == enemy_team]
        attacker_first, attacker_middle, attacker_last = list(), list(), list()
        defender_first, defender_middle, defender_last = list(), list(), list()

        # Get best land unit to keep for capturing territories
        land_unit = None
        if one_land_unit_remaining:
            for unit_state in unit_state_list:
                if unit_state.owner == self.player and unit_state.type_index < 3 and not unit_state.attached_to:
                    if not land_unit or unit_state.type_index > land_unit.type_index:
                        land_unit = unit_state
        if land_unit:
            attacker_last.append(land_unit)

        # Go through the remaining units and add them to the lists
        for unit_state in unit_state_list:
            # Ignore transported units and factories
            if unit_state.attached_to or unit_state == land_unit or unit_state.type_index == 4:
                continue
            # If owned by the attacking player
            if unit_state.owner == self.player:
                if unit_state.type_index == 5:
                    # Transports die last
                    attacker_last.append(unit_state)
                elif unit_state.type_index == attacker_priority_unit:
                    # Priority units are before land unit
                    attacker_last.insert(0, unit_state)
                elif unit_state.type_index == 10 and unit_state.damaged == 0:
                    # Battleships have two lives
                    attacker_first.append(unit_state)
                    attacker_middle.append(unit_state)
                else:
                    attacker_middle.append(unit_state)
            # If owned by the defending team
            elif unit_state.owner in defending_players:
                if unit_state.type_index == 5:
                    # Transports die last
                    defender_last.append(unit_state)
                elif unit_state.type_index == defender_priority_unit:
                    # Priority units are before land unit
                    defender_last.insert(0, unit_state)
                elif unit_state.type_index == 10 and unit_state.damaged == 0:
                    # Battleships have two lives
                    defender_first.append(unit_state)
                    defender_middle.append(unit_state)
                else:
                    defender_middle.append(unit_state)

        attacker_order = attacker_first + sorted(attacker_middle, key=lambda x: self.game.rules.get_unit(x.type_index).attack + self.game.rules.get_unit(x.type_index).cost/25) + attacker_last
        defender_order = defender_first + sorted(defender_middle, key=lambda x: self.game.rules.get_unit(x.type_index).defense + self.game.rules.get_unit(x.type_index).cost/25) + defender_last
        return attacker_order, defender_order

    def get_total_ipcs(self, unit_state_list):
        ipcs = 0
        for i in range(len(unit_state_list)):
            if unit_state_list[i] not in unit_state_list[:i]:
                ipcs += self.game.rules.get_unit(unit_state_list[i].type_index).cost
        return ipcs


class NonCombatMove:
    def __init__(self, game, ai_importance, risk_tolerances):
        self.game = game
        self.importances = ai_importance
        self.risk_tolerances = risk_tolerances

    def can_move(self, unit_state, current_territory, goal_territory):
        return self.game.calc_movement(unit_state, current_territory, goal_territory)[0] >= 0

    def extra_aa_needed_where(self):
        # Hey look at this! Cool! Use it if you want for moving aas.
        # Make sure, when implemented, that you actually use a path finder to see if an AA could get their easily
        # simple function that determines which 'important' of your allied territories do not have AA guns

        territory_name_list = []

        for territory_key in self.importances:
            for territory_name in self.game.state_dict:
                if territory_key == territory_name and \
                        self.game.rule.teams[self.game.state_dict[territory_name].owner] == self.game.rule.teams[self.game.turn_state.player]:
                    territory_name_list.append(territory_name)

    def move_unit(self, unit_state, current_territory, goal_territory):
        if current_territory == goal_territory:
            return True
        dist, path = self.game.calc_movement(unit_state, current_territory, goal_territory)
        if dist == -1:
            return False
        current_territory_state, goal_territory_state = self.game.state_dict[current_territory], self.game.state_dict[goal_territory]
        current_territory_state.unit_state_list.remove(unit_state)
        for other_unit_state in unit_state.attached_units:
            current_territory_state.unit_state_list.remove(other_unit_state)
        unit = self.game.rules.get_unit(unit_state.type_index)
        print('  - Moved', unit.name, 'from', current_territory, 'to', goal_territory)
        if unit.name == 'transport':
            print('    - Unit is carrying', [self.game.rules.get_unit(land_unit.type_index).name for land_unit in unit_state.attached_units])

        # AA guns
        if self.game.rules.aa_flyover and unit.unit_type == 'air':
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
                                    print('    - Unit shot down by AA gun in', ter_name)
                                    return True

        # Update unit
        goal_territory_state.unit_state_list.append(unit_state)
        for other_unit_state in unit_state.attached_units:
            goal_territory_state.unit_state_list.append(other_unit_state)
        unit_state.moves_used += dist
        if not unit_state.moved_from:
            unit_state.moved_from = path
        else:
            unit_state.moved_from += path[1:]
        if unit_state.attached_to:
            print('    - Unit was on transport carrying', [self.game.rules.get_unit(land_unit.type_index).name for land_unit in unit_state.attached_to.attached_units])
            unit_state.attached_to.attached_units.remove(unit_state)
            unit_state.attached_to = None
        if self.game.rules.board[goal_territory].is_water and unit.unit_type == 'land':
            # Attach to transport
            if unit.name == 'infantry':
                # Look for open infantry spots
                for other_unit_state in goal_territory_state.unit_state_list:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0 or \
                                (len(other_unit_state.attached_units) == 1 and other_unit_state.attached_units[
                                    0].type_index != 0):
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
            # Look for any available spot
            if not unit_state.attached_to:
                for other_unit_state in goal_territory_state.unit_state_list:
                    if other_unit_state.type_index == 5:
                        if len(other_unit_state.attached_units) == 0:
                            unit_state.attached_to = other_unit_state
                            other_unit_state.attached_units.append(unit_state)
                            break
                        elif len(other_unit_state.attached_units) == 1:
                            if unit.name == 'infantry' or other_unit_state.attached_units[0].type_index == 0:
                                unit_state.attached_to = other_unit_state
                                other_unit_state.attached_units.append(unit_state)
                                break
            if len(unit_state.attached_to.attached_units) == 1:
                print('    - Attached unit to empty transport')
            else:
                name = self.game.rules.get_unit(unit_state.attached_to.attached_units[0].type_index).name
                print('    - Attached unit to transport carrying', name)
        return True

    def do_non_combat_move(self):
        # Get which units even have moves left
        total_moves = [self.game.rules.get_unit(i).movement for i in range(len(self.game.rules.units))]
        planes = list()
        for territory_name in self.game.state_dict.keys():
            for unit_state in self.game.state_dict[territory_name].unit_state_list:
                if unit_state.owner == self.game.turn_state.player and unit_state.type_index > 10:
                    planes.append((unit_state, territory_name))

        vulnerability = Vulnerability(self.game)

        for plane_state, territory_name in planes:
            vulnerability.territories[territory_name][self.game.rules.teams[plane_state.owner]].remove(plane_state)

        # Get which territories are likely to be attacked
        territories_under_threat = set()
        enemy_team = self.game.rules.enemy_team(player=self.game.turn_state.player)
        for player in self.game.rules.teams.keys():
            if self.game.rules.teams[player] == enemy_team:
                # We can avoid initializing the vulnerability class multiple times by making it once and then making a copy
                vuln_copy = Vulnerability(self.game, init_territories=False)
                vuln_copy.territories = vulnerability.territories.copy()
                vuln_copy.invalid = False
                # Simulate opponent trying to attack
                attackable = Attackable(self.game, player, self.importances, self.risk_tolerances, vuln_copy)
                territories_under_threat.update(attackable.get_best_attacks(just_get_territories=True))

        # Start by looking for non-carrier landing spots for planes
        non_carrier_planes = dict()
        carrier_planes = dict()
        needed_carrier_spots = set()
        for plane_state, territory_name in planes:
            plane_unit = self.game.rules.get_unit(plane_state.type_index)
            moves_left = plane_unit.movement - plane_state.moves_used
            within_range, queue, dist = {territory_name}, [territory_name], 0
            while dist < moves_left:
                next_queue = list()
                for ter in queue:
                    for neighbor in self.game.rules.board[ter].neighbors:
                        if neighbor not in within_range:
                            within_range.add(neighbor)
                            next_queue.append(neighbor)
                queue = next_queue
                dist += 1
            carrier_spots, landing_spots = list(), list()
            for ter in within_range:
                if self.game.rules.board[ter].is_water:
                    carrier_spots.append(ter)
                elif self.game.calc_movement(plane_state, territory_name, ter, phase=5)[0] >= 0:
                    landing_spots.append(ter)
            if landing_spots:
                non_carrier_planes[plane_state] = [territory_name, landing_spots[:]]
                self.game.state_dict[territory_name].unit_state_list.remove(plane_state)
            elif carrier_spots and plane_unit.name == 'fighter':
                carrier_planes[plane_state] = [territory_name, set(carrier_spots)]
                needed_carrier_spots.update(carrier_spots)
            else:
                print('  - ' + plane_unit.name + ' in ' + territory_name + " couldn't land and died")
                self.game.state_dict[territory_name].unit_state_list.remove(plane_state)
        # Find where carriers can go
        carriers = dict()
        carrier_spots = set()
        for territory_name, territory_state in self.game.state_dict.items():
            allied_fighters, allied_carriers, player_carriers, allied_fighter = 0, 0, list(), None
            for unit_state in territory_state.unit_state_list:
                if self.game.rules.teams[unit_state.owner] == self.game.rules.teams[self.game.turn_state.player]:
                    if unit_state.type_index == 9:
                        if unit_state.owner == self.game.turn_state.player:
                            player_carriers.append(unit_state)
                        else:
                            allied_carriers += 1
                    elif unit_state.type_index == 11 and unit_state.owner != self.game.turn_state.player:
                        allied_fighters += 1
                        allied_fighter = unit_state
            player_carriers.sort(key=lambda x: x.moves_used)
            allied_carrier_spots = 2 * allied_carriers - allied_fighters
            while allied_carrier_spots < -1 and player_carriers:
                player_carriers.pop()
                allied_carrier_spots += 2
            if allied_carrier_spots == -1 and player_carriers:
                player_carriers[-1].attached_units = [allied_fighter]
            for carrier_state in player_carriers:
                moves_left = 2 - carrier_state.moves_used
                within_range, queue, dist = {territory_name}, [territory_name], 0
                while dist < moves_left:
                    next_queue = list()
                    for ter in queue:
                        for neighbor in self.game.rules.board[ter].neighbors:
                            if neighbor not in within_range:
                                within_range.add(neighbor)
                                next_queue.append(neighbor)
                    queue = next_queue
                    dist += 1
                within_range.intersection_update(needed_carrier_spots)
                spots = list()
                for ter in within_range:
                    if self.game.calc_movement(carrier_state, territory_name, ter)[0] >= 0:
                        spots.append(ter)
                        carrier_spots.add(ter)
                carriers[carrier_state] = [territory_name, set(spots)]
        # Try to match them up
        while carrier_planes and carriers:
            needed_carrier_spots = set()
            for plane_state, arr in carrier_planes.items():
                needed_carrier_spots.update(arr[1])
            carrier_spots = set()
            for carrier_state, arr in carriers.items():
                carrier_spots.update(arr[1])
            common_spots = needed_carrier_spots.intersection(carrier_spots)
            # Remove fighters that can't be picked up
            to_delete = list()
            for plane_state in carrier_planes.keys():
                carrier_planes[plane_state][1].intersection_update(common_spots)
                if not carrier_planes[plane_state][1]:
                    print('  - fighter in ' + carrier_planes[plane_state][0] + " couldn't land and died")
                    self.game.state_dict[carrier_planes[plane_state][0]].unit_state_list.remove(plane_state)
                    to_delete.append(plane_state)
            for plane_state in to_delete:
                del carrier_planes[plane_state]
            # Remove carriers that aren't in range of any fighters
            to_delete = list()
            for carrier_state in carriers.keys():
                carriers[carrier_state][1].intersection_update(common_spots)
                if not carriers[carrier_state][1]:
                    to_delete.append(carrier_state)
                    if carrier_state.attached_units:
                        carrier_state.attached_units = list()
            for carrier_state in to_delete:
                del carriers[carrier_state]
            if carrier_planes and carriers:
                # Check the most restricted carrier first
                carrier_state = min(carriers.keys(), key=lambda x: len(carriers[x][1]))
                possible_fighters = [carriers[carrier_state][0], 999999]
                for target in carriers[carrier_state][1]:
                    possibilities = sorted([fighter_state for fighter_state, arr in carrier_planes.items() if target in arr[1]], key=lambda x: len(carrier_planes[x][1]))
                    needed = 1 if carrier_state.attached_units else 2
                    if len(possibilities) > needed:
                        possibilities = possibilities[:needed]
                    num_poss = len(carrier_planes[possibilities[0]][1])
                    if len(possibilities) > 1:
                        num_poss -= 1 / len(carrier_planes[possibilities[1]][1])
                    if num_poss < possible_fighters[-1]:
                        possible_fighters = possibilities[:] + [target, num_poss]
                # Actually move the units
                self.move_unit(carrier_state, carriers[carrier_state][0], possible_fighters[-2])
                vulnerability.territories[carriers[carrier_state][0]][self.game.rules.teams[carrier_state.owner]].remove(carrier_state)
                vulnerability.territories[possible_fighters[-2]][self.game.rules.teams[carrier_state.owner]].append(carrier_state)
                if carrier_state.attached_units:
                    self.move_unit(carrier_state.attached_units[0], carriers[carrier_state][0], possible_fighters[-2])
                    vulnerability.territories[carriers[carrier_state][0]][self.game.rules.teams[carrier_state.owner]].remove(carrier_state)
                    vulnerability.territories[possible_fighters[-2]][self.game.rules.teams[carrier_state.owner]].append(carrier_state.attached_units[0])
                    print('    - Attached ' + carrier_state.attached_units[0].owner + ' fighter moved with above carrier')
                    carrier_state.attached_units[0].moved_used = 0
                    carrier_state.attached_units = list()
                del carriers[carrier_state]
                for fighter_state in possible_fighters[:-2]:
                    self.move_unit(fighter_state, carrier_planes[fighter_state][0], possible_fighters[-2])
                    vulnerability.territories[possible_fighters[-2]][self.game.rules.teams[fighter_state.owner]].append(fighter_state)
                    del carrier_planes[fighter_state]
        # Delete anything that didn't make it
        available_units = list()
        if carrier_planes:
            for plane_state, arr in carrier_planes.items():
                print('  - fighter in ' + arr[0] + " couldn't land and died")
                self.game.state_dict[arr[0]].unit_state_list.remove(plane_state)
        if carriers:
            for carrier_state, arr in carriers.items():
                available_units.append((carrier_state, arr[0]))
        # Get the rest of the units
        aa_guns = dict()
        for territory_name in self.game.state_dict.keys():
            for unit_state in self.game.state_dict[territory_name].unit_state_list:
                if unit_state.owner == self.game.turn_state.player and unit_state.moves_used < total_moves[unit_state.type_index]:
                    if unit_state.type_index != 4 and unit_state.type_index != 9 and unit_state.type_index <= 10 and not unit_state.attached_to:
                        if unit_state.type_index == 3:
                            if territory_name not in aa_guns:
                                aa_guns[territory_name] = list()
                            aa_guns[territory_name].append(unit_state)
                        else:
                            available_units.append((unit_state, territory_name))

        # Any AA gun that isn't alone should try to move
        aa_guns_to_move = list()
        duplicate_aa_guns = list()
        already_has_aa_gun = set(aa_guns.keys())
        for territory_name in aa_guns.keys():
            if len(aa_guns[territory_name]) > 1:
                neighbors = [ter for ter in self.game.rules.board[territory_name].neighbors if ter not in already_has_aa_gun]
                for unit_state in aa_guns[territory_name][1:]:
                    aa_guns_to_move.append([unit_state, territory_name, [ter for ter in neighbors if self.can_move(unit_state, territory_name, ter)]])
        while aa_guns_to_move:
            arr = min(aa_guns_to_move, key=lambda x: len(x[2]))
            if len(arr[2]) == 0:
                duplicate_aa_guns.append((arr[0], arr[1]))
            else:
                target = max(arr[2], key=lambda x: self.importances[x])
                self.move_unit(arr[0], arr[1], target)
                vulnerability.territories[arr[1]][self.game.rules.teams[arr[0].owner]].remove(arr[0])
                vulnerability.territories[target][self.game.rules.teams[arr[0].owner]].append(arr[0])
                already_has_aa_gun.add(target)
                for arr in aa_guns_to_move:
                    if target in arr[2]:
                        arr[2].remove(target)
            aa_guns_to_move.remove(arr)
        for unit_state, territory_name in duplicate_aa_guns:
            can_move_to = [ter for ter in [territory_name] + self.game.rules.board[territory_name].neighbors if self.can_move(unit_state, territory_name, ter)]
            target = max(can_move_to, key=lambda x: self.importances[x])
            self.move_unit(unit_state, territory_name, target)
            vulnerability.territories[territory_name][self.game.rules.teams[unit_state.owner]].remove(unit_state)
            vulnerability.territories[target][self.game.rules.teams[unit_state.owner]].append(unit_state)

        # For each unit, check which of these territories it is able to help, and find the most important one.
        # It shouldn't move if doing so would make it's own territory vulnerable though, unless said territory was more important
        available_units.sort(key=lambda x: x[0].type_index)
        for unit_state, territory_name in available_units:
            moves_left = self.game.rules.get_unit(unit_state.type_index).movement - unit_state.moves_used
            within_range, queue, dist = {territory_name}, [territory_name], 0
            while dist < moves_left:
                next_queue = list()
                for ter in queue:
                    for neighbor in self.game.rules.board[ter].neighbors:
                        if neighbor not in within_range:
                            within_range.add(neighbor)
                            next_queue.append(neighbor)
                queue = next_queue
                dist += 1
            can_move_to = [ter for ter in within_range if self.game.calc_movement(unit_state, territory_name, ter)[0] >= 0]
            arr = vulnerability.territories[territory_name][self.game.rules.teams[self.game.turn_state.player]]
            if unit_state in arr:
                arr.remove(unit_state)
            self.game.state_dict[territory_name].unit_state_list.remove(unit_state)
            target = self.get_most_needed_territory(unit_state, territories_under_threat, territory_name, can_move_to, vulnerability)
            self.game.state_dict[territory_name].unit_state_list.append(unit_state)
            self.move_unit(unit_state, territory_name, target)
            if unit_state.type_index != 5:
                vulnerability.territories[target][self.game.rules.teams[self.game.turn_state.player]].append(unit_state)

        # Get open carrier spots
        carrier_spots = dict()
        for territory_name, territory_state in self.game.state_dict.items():
            allied_fighters, allied_carriers = 0, 0
            for unit_state in territory_state.unit_state_list:
                if self.game.rules.teams[unit_state.owner] == self.game.rules.teams[self.game.turn_state.player]:
                    allied_fighters += (unit_state.type_index == 11)
                    allied_carriers += (unit_state.type_index == 9)
            if allied_fighters < allied_carriers * 2:
                carrier_spots[territory_name] = allied_carriers * 2 - allied_fighters

        # For any planes that moved to land, find what carriers they could move to instead
        for plane_state in non_carrier_planes.keys():
            non_carrier_planes[plane_state].append(list())
            if plane_state.type_index == 11:  # Bombers can't land on carriers
                territory_name = non_carrier_planes[plane_state][0]
                moves_left = 4 - plane_state.moves_used
                within_range, queue, dist = {territory_name}, [territory_name], 0
                while dist < moves_left:
                    next_queue = list()
                    for ter in queue:
                        for neighbor in self.game.rules.board[ter].neighbors:
                            if neighbor not in within_range:
                                within_range.add(neighbor)
                                next_queue.append(neighbor)
                    queue = next_queue
                    dist += 1
                self.game.state_dict[territory_name].unit_state_list.append(plane_state)
                for goal in within_range:
                    if goal in carrier_spots and self.game.calc_movement(plane_state, territory_name, goal, phase=5)[0] >= 0:
                        for _ in range(carrier_spots[goal]):
                            non_carrier_planes[plane_state][2].append(goal)
            else:
                self.game.state_dict[non_carrier_planes[plane_state][0]].unit_state_list.append(plane_state)

        # Starting with the most restricted plane first, find the best place to move it
        while non_carrier_planes:
            plane_state = min(non_carrier_planes.keys(), key=lambda x: len(non_carrier_planes[x][1]) + len(set(non_carrier_planes[x][2])))
            arr = non_carrier_planes[plane_state]
            if not arr[1] and not arr[2]:
                # Hopefully shouldn't reach this lol
                print('    - ' + self.game.rules.get_unit(plane_state.type_index).name + ' in ' + arr[0] + " couldn't land and died")
            else:
                target = self.get_most_needed_territory(plane_state, territories_under_threat, arr[0], list(set(arr[1] + arr[2])), vulnerability)
                self.move_unit(plane_state, arr[0], target)
                vulnerability.territories[target][self.game.rules.teams[plane_state.owner]].append(plane_state)
            del non_carrier_planes[plane_state]

        # Any amphibious units that can move off of their transport should, because it is free to move back on
        for territory_name in self.game.state_dict.keys():
            for unit_state in self.game.state_dict[territory_name].unit_state_list:
                if unit_state.attached_units:
                    neighbors = [ter for ter in self.game.rules.board[territory_name].neighbors if not self.game.rules.board[ter].is_water]
                    unloadable = [ter for ter in neighbors if self.game.calc_movement(unit_state.attached_units[0], territory_name, ter, phase=5)[0] >= 0]
                    if unloadable:
                        target = self.get_most_needed_territory(unit_state.attached_units[0], territories_under_threat, territory_name, unloadable, vulnerability)
                        while unit_state.attached_units:
                            if unit_state.attached_units[0].owner == self.game.turn_state.player:
                                self.move_unit(unit_state.attached_units[0], territory_name, target)

    def get_most_needed_territory(self, unit_state, territories_under_threat, current, within_range, vuln):
        team = self.game.rules.teams[unit_state.owner]
        # If there are any capturable land territories, there needs to be a unit there
        capturable = list()
        for ter in within_range:
            can_capture = False
            territory = self.game.rules.board[ter]
            if not territory.is_water:
                has_ally = False
                for us in self.game.state_dict[ter].unit_state_list:
                    if (us.type_index < 3 or us.type_index > 4) and self.game.rules.teams[us.owner] == team:
                        has_ally = True
                        break
                if not has_ally:
                    for neighbor in territory.neighbors:
                        if self.game.rules.board[neighbor].is_water:
                            possible_enemy_ters, queue, dist = {neighbor}, [neighbor], 0
                            while dist <= 2 and not can_capture:
                                next_queue = list()
                                for water_ter in queue:
                                    has_ally = False
                                    for us in self.game.state_dict[water_ter].unit_state_list:
                                        if self.game.rules.teams[us.owner] == team:
                                            if 7 <= us.type_index <= 10:
                                                has_ally = True
                                        elif us.type_index == 5:
                                            can_capture = True
                                            break
                                    if can_capture:
                                        break
                                    if not has_ally:
                                        for neighbor_2 in self.game.rules.board[neighbor].neighbors:
                                            if neighbor_2 not in possible_enemy_ters:
                                                possible_enemy_ters.add(neighbor_2)
                                                if self.game.rules.board[neighbor].is_water:
                                                    next_queue.append(neighbor_2)
                                queue = next_queue
                                dist += 1
                        else:
                            has_friendlies = False
                            for us in self.game.state_dict[neighbor].unit_state_list:
                                if us.type_index < 3 and self.game.rules.teams[us.owner] != team:
                                    can_capture = True
                                    break
                                elif (us.type_index < 3 or us.type_index > 4) and self.game.rules.teams[us.owner] == team:
                                    has_friendlies = True
                            if can_capture:
                                break
                            if not has_friendlies:
                                for neighbor_2 in self.game.rules.board[neighbor].neighbors:
                                    for us in self.game.state_dict[neighbor_2].unit_state_list:
                                        if us.type_index == 2 and self.game.rules.teams[us.owner] != team:
                                            can_capture = True
                                            break
                                    if can_capture:
                                        break
                        if can_capture:
                            break
            if can_capture:
                capturable.append(ter)
        if capturable:
            return max(capturable, key=lambda x: self.importances[x])
        # If any of the territories under threat are vulnerable, go there
        under_threat = [ter for ter in within_range if ter in territories_under_threat and vuln.is_vulnerable(ter, self.risk_tolerances, defender=team)]
        if under_threat:
            target = max(under_threat, key=lambda x: self.importances[x])
        else:
            # Otherwise, go to the most important/vulnerable territory within range if it is worth ipcs
            worth_ipcs = [ter for ter in within_range if self.game.rules.board[ter].ipc > 0]
            if worth_ipcs:
                target = min(worth_ipcs, key=lambda x: vuln.get_estimated_defensibility(x, defender=team) - self.importances[x])
            else:
                target = min(within_range, key=lambda x: vuln.get_estimated_defensibility(x, defender=team) - self.importances[x])
        return target


class Place:
    """
    this class is primarily a long list of If's. Actual machine learning would be wasted here, as placing units
    is a pretty linear, albeit complicated, process.
    """

    def __init__(self, game, purchased_unit_state_list, build_importance, risk_tolerances):
        self.placements = {}
        self.build_importance = build_importance
        self.game = game
        self.purchased_unit_state_list = purchased_unit_state_list
        self.immediate_defensive_requirements = list()
        self.latent_defensive_requirements = list()
        self.vulnerability = Vulnerability(game)
        self.endangered_name_list = self.get_territories_under_threat(build_importance, risk_tolerances)
        self.risk_tolerances = risk_tolerances

        self.factories = []
        for territory_name, territory_state in self.game.state_dict.items():
            if territory_state.owner == self.game.turn_state.player \
            and not territory_state.just_captured:
                for unit_state in self.game.state_dict[territory_name].unit_state_list:
                    if unit_state.type_index == 4:
                        self.factories.append(territory_name)
        # self.factories now has a list of names having factories

    def get_territories_under_threat(self, risk_tolerance, factory_risk=None, capital_risk=None):
        # Below code is copy-pasted from do_non_combat_move(). Should probably just make single function for it but nah
        vulnerability = Vulnerability(self.game)
        # Get which territories are likely to be attacked
        territories_under_threat = set()
        enemy_team = self.game.rules.enemy_team(player=self.game.turn_state.player)
        for player in self.game.rules.teams.keys():
            if self.game.rules.teams[player] == enemy_team:
                # We can avoid initializing the vulnerability class multiple times by making it once and then making a copy
                vuln_copy = Vulnerability(self.game, init_territories=False)
                vuln_copy.territories = vulnerability.territories.copy()
                vuln_copy.invalid = False
                # Simulate opponent trying to attack
                attackable = Attackable(self.game, player, self.build_importance, risk_tolerance, vuln=vuln_copy)
                territories_under_threat.update(attackable.get_best_attacks(just_get_territories=True))
        # (End of copy-pasted code)

        return sorted(territories_under_threat, key=lambda x: self.build_importance[x], reverse=True)

    # This will need to be called within build_strategy after adding the theoritical units to see if still under threat.
    def factory_builder(self, unit_state, territory_name):
        if territory_name not in self.placements.keys():
            self.placements[territory_name] = list()

        self.purchased_unit_state_list.remove(unit_state)
        self.placements[territory_name].append(unit_state)

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

    def build_importance_getter(self, territory_name):
        return self.build_importance[territory_name]

    def can_be_saved(self, theoretical_append, territory_name):
        # returns "can be saved True" if the territory is not a capital and can be saved. If is a capital and cant be
        # saved, automatically places (puts into placement dict) max in the capital.
        build_slots = self.build_slots(territory_name)

        can_be_saved = True
        # check if can be saved
        if self.game.state_dict[territory_name].owner != "Sea Zone":
            for unit_state in self.purchased_unit_state_list:
                if len(theoretical_append) < build_slots:
                    if unit_state.type_index == 11:  # fighter
                        theoretical_append.append(unit_state)
                    if unit_state.type_index == 2:  # tank
                        theoretical_append.append(unit_state)
                    if unit_state.type_index == 1 or unit_state.type_index == 0:  # inf or art
                        theoretical_append.append(unit_state)
                    if unit_state.type_index == 3:  # aa
                        theoretical_append.append(unit_state)
            if self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append):
                if self.game.rules.board[territory_name].is_capital:  # protect capital at all costs
                    self.theoretical_to_placements(theoretical_append, territory_name)
                else:  # abandon if cant possibly hold.
                    theoretical_append.clear()
                    can_be_saved = False

        else:
            for unit_state in self.purchased_unit_state_list:
                for fac_territory_name in self.adjacent_factory_finder(territory_name):
                    if len(theoretical_append) < self.build_slots(fac_territory_name):
                        theoretical_append.append(unit_state)
            if self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append):
                theoretical_append.clear()
                can_be_saved = False

        theoretical_append.clear()
        return can_be_saved

    def front_line_builder(self, theoretical_append, territory_name, vulnerability_reader_active=True):
        # prioritizes an even spread of infantry and artillery in frontline factories

        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append)

        build_slots = self.build_slots(territory_name)
        for unit_state in self.purchased_unit_state_list:
            if vulnerability_reader:
                if (unit_state.type_index == 1) \
                        and (len(theoretical_append) < build_slots // 2):  # artillery
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
                    if vulnerability_reader_active \
                            or len(theoretical_append) < self.build_importance[territory_name]:
                        theoretical_append.append(unit_state)

    def reserve_line_builder(self, theoretical_append, territory_name, vulnerability_reader_active=True):
        # puts, in theoretical_append, land units in non-frontline factories

        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append)

        build_slots = self.build_slots(territory_name)
        for unit_state in self.purchased_unit_state_list:
            if self.game.rules.get_unit(unit_state.type_index).unit_type != "sea" \
                    and vulnerability_reader:
                if len(theoretical_append) < build_slots:
                    if vulnerability_reader_active \
                            or len(theoretical_append) < self.build_importance[territory_name]:
                        theoretical_append.append(unit_state)

    def adjacent_factory_finder(self, territory_name):
        # returns a list of territory names that have factories
        adjacent_factory_list = []

        neighbors = self.game.rules.board[territory_name].neighbors
        for neighbor_name in neighbors:
            territory_state = self.game.state_dict[neighbor_name]
            if territory_state.owner == self.game.turn_state.player \
            and not territory_state.just_captured:
                for unit_state in territory_state.unit_state_list:
                    if unit_state.type_index == 4:  # factory
                        adjacent_factory_list.append(neighbor_name)

        adjacent_factory_list.sort(key=lambda x: self.game.rules.board[x].ipc)
        return adjacent_factory_list

    def adjacent_seazone_finder(self, territory_name):
        adjacent_seazone_list = []
        neighbors = self.game.rules.board[territory_name].neighbors
        for neighbor_name in neighbors:
            if self.game.state_dict[neighbor_name].owner == "Sea Zone":
                adjacent_seazone_list.append(neighbor_name)
        return adjacent_seazone_list

    def sea_zone_builder(self, theoretical_append, territory_name, vulnerability_reader_active=True):

        adjacent_factory_list = self.adjacent_factory_finder(territory_name)
        vulnerability_reader = True
        if vulnerability_reader_active:
            vulnerability_reader = self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append)

        carrier_slots = 0
        transport_space = 0
        for unit_state in self.purchased_unit_state_list:
            if self.game.rules.get_unit(unit_state.type_index).unit_type == "sea" \
                    and vulnerability_reader:
                # choose the bigger factory to remove build slots from first. Sub-optimal but fine.
                i = 0
                adjacent_factory_list.sort(reverse=True, key=lambda x: self.game.rules.board[x].ipc)
                for fac_territory_name in adjacent_factory_list:
                    if i == 0 and len(theoretical_append) < self.build_slots(fac_territory_name):
                        if vulnerability_reader_active \
                                or len(theoretical_append) < self.build_importance[territory_name]:
                            i = 1
                            theoretical_append.append(unit_state)
                            # TODO (Future): Have the AI organize the placements list.

            elif unit_state.type_index == 11 and \
                    vulnerability_reader:
                for ship_state in theoretical_append:
                    if ship_state.type_index == 9:
                        carrier_slots += 2
                    if ship_state.type_index == 11:
                        carrier_slots -= 1
                for ship_state in self.game.state_dict[territory_name].unit_state_list:
                    if ship_state.type_index == 9:
                        carrier_slots += 2
                    if ship_state.type_index == 11:  # aka already a fighter on board
                        carrier_slots -= 1

                i = 0
                adjacent_factory_list.sort(reverse=True, key=lambda x: self.game.rules.board[x].ipc)
                for fac_territory_name in adjacent_factory_list:
                    if i == 0 and len(theoretical_append) < self.build_slots(fac_territory_name):
                        if vulnerability_reader_active or \
                                len(theoretical_append) < self.build_importance[territory_name]:
                            i = 1
                            theoretical_append.append(unit_state)

            # places transportable units
            elif (unit_state.type_index == 0 or unit_state.type_index == 1) and not vulnerability_reader_active:
                for fac_territory_name in adjacent_factory_list:
                    if len(theoretical_append) < self.build_slots(fac_territory_name) \
                            and len(theoretical_append) < self.build_importance[territory_name]:
                        for unit_state2 in theoretical_append:
                            if unit_state2.type_index == 5:
                                transport_space += self.game.rules.get_unit(5).transport_capacity
                        for unit_state2 in self.game.state_dict[territory_name].unit_state_list:
                            if unit_state2.type_index == 5:
                                transport_space += self.game.rules.get_unit(5).transport_capacity
                                for attached_unit_state in unit_state2.attached_units:
                                    transport_space -= \
                                        self.game.rules.get_unit(attached_unit_state.type_index).transport_weight
                if transport_space >= self.game.rules.get_unit(unit_state.type_index).transport_weight:
                    if unit_state in self.purchased_unit_state_list and territory_name in self.placements:
                        self.purchased_unit_state_list.remove(unit_state)
                        self.placements[territory_name].append(unit_state)  # TODO (George): It's possible for territory_name to not be in placements, which crashes the program. pls fix
                        self.game.state_dict[fac_territory_name].built_units += 1
                        self.vulnerability.place_unit(unit_state, territory_name)           

    def update_vulnerable_builds(self, territory_name, theoretical_append):
        i = 0
        while self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append):
            i += 1
            if i == 1:
                for unit_state in theoretical_append:
                    if unit_state.type_index == 1 or unit_state.type_index == 0:  # replaces art/inf w/tanks
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

        if territory_name not in self.placements.keys():
            self.placements[territory_name] = list()

        for unit_state in theoretical_append:
            # TODO (George): Theoretical append has duplicate units in it
            if unit_state in self.purchased_unit_state_list:
                self.purchased_unit_state_list.remove(unit_state)
                self.placements[territory_name].append(unit_state)
                self.game.state_dict[factory_name].built_units += 1
                self.vulnerability.place_unit(unit_state, territory_name)

        theoretical_append.clear()

    def build_strategy(self):  # called by the AI

        for unit_state in self.purchased_unit_state_list:
            if unit_state.type_index == 4:
                # TODO (Future): Make ai factory placement work.
                # Will require a list of factory affinity weighted by how close to the turn it was build you are on
                # territory_name = ai_factory_placement_decider(maybe will need: player, strategy, weighted_list)
                territory_name = "Union of South Africa"  # TEMPORARY STAND-IN
                self.factory_builder(unit_state, territory_name)

        if self.immediate_defensive_requirements:  # this will always be land
            self.immediate_defensive_requirements.sort(reverse=True, key=lambda x: self.game.rules.board[x].ipc)
            for territory_name in self.immediate_defensive_requirements:
                build_slots = self.build_slots(territory_name)
                theoretical_append = []

                can_be_saved = self.can_be_saved(theoretical_append,
                                                 territory_name)  # this is a bool, but also modifies stuff

                is_frontline = False
                enemy_team = self.game.rules.enemy_team(player=self.game.state_dict[territory_name].owner)
                for neighbor in self.game.rules.board[territory_name].neighbors:
                    if self.game.rules.teams[self.game.state_dict[neighbor].owner] == enemy_team:
                        is_frontline = True
                        break

                if can_be_saved:
                    if is_frontline:
                        self.front_line_builder(theoretical_append, territory_name)
                        # fills frontline territories with infantry and artillery first, then with other land units.
                        if self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append):
                            self.update_vulnerable_builds(territory_name, theoretical_append)

                    else:
                        self.reserve_line_builder(theoretical_append, territory_name)
                        if self.vulnerability.is_vulnerable(territory_name, self.risk_tolerances, theoretical_append):
                            self.update_vulnerable_builds(territory_name, theoretical_append)

                # puts the theoretical units into the placements and removes them from purchased_unit_state_list
                self.theoretical_to_placements(theoretical_append, territory_name)
            # This concludes immediate_defensive_requirements

        elif self.latent_defensive_requirements:
            for territory_name in self.latent_defensive_requirements:
                build_slots = self.build_slots(territory_name)
                theoretical_append = []
                can_be_saved = self.can_be_saved(theoretical_append, territory_name)
                if self.game.state_dict[territory_name].owner == "Sea Zone":
                    if can_be_saved:
                        self.sea_zone_builder(theoretical_append, territory_name)

                else:  # builds max front-line units in factories adjacent to threatened land zones, if any
                    self.front_line_builder(theoretical_append, territory_name, False)

                self.theoretical_to_placements(theoretical_append, territory_name)

        else:  # places all the rest of the units according to the order they are in the list.
            for territory_name in self.factories:
                theoretical_append = []
                can_be_saved = self.can_be_saved(theoretical_append, territory_name)

                if can_be_saved:
                    self.reserve_line_builder(theoretical_append, territory_name, False)

                    for seazone_name in self.adjacent_seazone_finder(territory_name):
                        self.sea_zone_builder(theoretical_append, seazone_name, False)

                    self.theoretical_to_placements(theoretical_append, territory_name)
            
            # places any unplaced units if there is space
            for territory_name in self.factories:
                theoretical_append = []
                build_slots = self.build_slots(territory_name)
                for unit_state in self.purchased_unit_state_list:
                    if self.game.rules.get_unit(unit_state.type_index).unit_type != "sea":
                        if len(theoretical_append) < build_slots:
                            theoretical_append.append(unit_state)
                            self.theoretical_to_placements(theoretical_append, territory_name)
                    if self.game.rules.get_unit(unit_state.type_index).unit_type == "sea":
                        if len(theoretical_append) < build_slots:
                            seazone_list = self.adjacent_seazone_finder(territory_name)
                            for sea_zone in seazone_list:
                                theoretical_append.append(unit_state)
                                self.theoretical_to_placements(theoretical_append, sea_zone, territory_name)

    def place(self):
        for territory_key in self.placements:
            if self.game.state_dict[territory_key].owner == self.game.turn_state.player:
                for unit_state in self.placements[territory_key]:
                    self.game.state_dict[territory_key].unit_state_list.append(unit_state)
                    print('  - Placed', self.game.rules.get_unit(unit_state.type_index).name, 'in', territory_key)
                    self.game.purchased_units[self.game.turn_state.player].remove(unit_state)
            else:
                # TODO (George): It still reaches this code (i.e. it tries to place units in enemy territories)
                print("Hopefully shouldn't reach this code")
        if self.game.purchased_units[self.game.turn_state.player]:
            print('  - There are still', len(self.game.purchased_units[self.game.turn_state.player]), 'unplaced units')
        self.vulnerability.invalid = True


class Cleanup:
    def __init__(self, game):

        self.game_result = game.has_won()
        if self.game_result:
            return

        # Refund units
        for player in game.purchased_units.keys():
            for unit_state in game.purchased_units[player]:
                game.players[player].ipc += game.rules.get_unit(unit_state.type_index).cost

        for territory_key, territory_state in game.state_dict.items():
            for unit_state in game.state_dict[territory_key].unit_state_list:
                if unit_state != 4:
                    unit_state.retreated = False  # resets reatreated units
                if (unit_state.type_index == 4) and (game.state_dict[territory_key].owner != unit_state.owner):
                    unit_state.owner = game.state_dict[territory_key].owner  # reset factory ownership
            territory_state.built_units = 0  # reset built_units
            territory_state.just_captured = False
            for unit_state in territory_state.unit_state_list:
                unit_state.moves_used = 0
                if unit_state.type_index != 5:  # this is irrelevant because bombing directly affects IPCs. Allows change
                    unit_state.damaged = 0
                unit_state.moved_from.clear()

            if territory_state.owner == game.turn_state.player and \
                    game.state_dict[
                        game.players[game.turn_state.player].capital].owner == game.turn_state.player:  # has cap
                game.players[game.turn_state.player].ipc += game.rules.board[territory_key].ipc  # updates ipc

        if game.turn_state.player == "America":
            game.turn_state.round_num += 1
        game.turn_state.player = game.rules.turn_order[game.turn_state.player]  # sets player to the next player
