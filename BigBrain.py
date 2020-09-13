"""

List of things AI needs to do:
- Needs to decide if we are winning
 * use above stuff
- Needs to decide risk tolerance
 * Used in is_vulnerable and everywhere that it is used.
 * What is the minimum threshold ratio of the Hawkes formula that the AI will tolerate
 * < 1 - risk tolerance is vulnerable
 * Look at past battles and decide if they won in the end and what the 'risk tolerance' was
 * I have a higher risk tolerance if I am losing
- Needs to make an 'importance' value of each territory:
 * Informed by webcrawled games.
- Factory builder
 * each territory from other games has a average factory value (how many were there and whose).
 * if you are the player, you will build a factory there according to those values and if you can hold it
 * Make sure we impliment both purchase and placement (place the factory at the end so it doesnt think it can build in it)
- Calculate build average for each teritory
 * build importance determine max build in unthreateneed territories
- AI organize placements list
 * WHAT THE FUCK WERE WE THINKING WHYYYYYYY
- Needs to decide build priority values.
"""


import keras
import phases
import BoardState
import numpy as np
import time


class Brain:
    def __init__(self):
        self.importance = Heuristics('importance_value')
        self.risk = RiskTolerance()
        self.build = Heuristics('build_average')
        self.prioritization = Prioritization()
        self.winning = IsWinning()

    def get_risk_tolerances(self, game, player=''):
        if not player:
            player = game.turn_state.player
        vuln = phases.Vulnerability(game)
        winning = float(self.winning.get_value(game, vuln=vuln))
        risk_tolerances = dict()
        for territory in game.state_dict.keys():
            risk_tolerances[territory] = float(self.risk.get_value(game, territory, player, vuln, winning))
        return risk_tolerances

    def get_values(self, game, player='', is_winning=False, risk=False, importance=False, build=False, prioritization=False):
        print('Getting values from AI...')
        vuln = phases.Vulnerability(game)
        winning = float(self.winning.get_value(game, vuln=vuln))
        if not player:
            player = game.turn_state.player
        risk_tolerances, importance_values, build_averages = dict(), dict(), dict()
        progress = 0
        last_time = time.time()
        for territory in game.state_dict.keys():
            if risk:
                risk_tolerances[territory] = float(self.risk.get_value(game, territory, player, vuln, winning))
            if importance:
                importance_values[territory] = float(self.importance.get_value(game, territory, player, vuln, winning))
            if build:
                build_averages[territory] = float(self.build.get_value(game, territory, player, vuln, winning))
            progress += 1
            if time.time() - last_time > 5:
                print('Done ' + str(progress) + '/' + str(len(game.state_dict)) + ' territories')
                last_time = time.time()
        if game.rules.teams[player] == 'Axis':
            winning = 1 - winning
        result = list()
        if is_winning:
            result.append(winning)
        if risk:
            result.append(risk_tolerances)
        if importance:
            result.append(importance_values)
        if build:
            result.append(build_averages)
        if prioritization:
            result.append([float(k) for k in self.prioritization.get_value(game, player=player, vuln=vuln, winning=winning)])
        return result


class Heuristics:
    def __init__(self, name, load_net=True):
        self.name = name
        self.net = None
        if load_net:
            self.load_neural_net()

    def load_neural_net(self):
        model_file = 'NNData/' + self.name + '_model.h5'
        self.net = keras.models.load_model(model_file)

    def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = list()
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]
        friendly_team, enemy_team = game.rules.teams[player], game.rules.enemy_team(player=player)

        # Turn number
        heuristics.append(game.turn_state.round_num)

        # Who is winning
        heuristics.append(winning)

        # Is capital
        heuristics.append(1 if territory.is_capital else 0)

        # Is water
        heuristics.append(1 if territory.is_water else 0)

        # Defensive power of territory
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == friendly_team:
                power += game.rules.get_unit(unit_state.type_index).defense
        heuristics.append(power)

        # IPC value
        heuristics.append(territory.ipc)

        # Is key territory
        heuristics.append(1 if territory_name in game.rules.win_cons else 0)

        # Vulnerability (player = defender)
        heuristics.append(vuln.get_vulnerability(territory_name, defender=friendly_team))

        # Vulnerability (player = attacker)
        heuristics.append(vuln.get_vulnerability(territory_name, attacker=player))

        # Player's attack power within range of territory
        heuristics.append(sum(unit_stack.get_attack_power() for unit_stack in vuln.territories[territory_name][player]))

        # Enemies' attack power within range of territory
        power = 0
        for other_player, team in game.rules.teams.items():
            if team == enemy_team:
                power += sum(unit_stack.get_attack_power() for unit_stack in vuln.territories[territory_name][other_player])
        heuristics.append(power)

        # Closest distance to various places
        dists = [-1] * 6
        dist, remaining = 0, len(dists)
        current_territories, next_territories, already_seen = {territory_name}, set(), {territory_name}
        while remaining and current_territories:
            for ter in current_territories:
                enemy_unit_indices = {unit_state.type_index for unit_state in game.state_dict[ter].unit_state_list
                                      if game.rules.teams[unit_state.owner] == enemy_team}
                # Distance to capital
                if dists[0] < 0 and ter == game.players[player].capital:
                    dists[0] = dist
                    remaining -= 1
                # Distance to nearest enemy capital
                if dists[1] < 0 and game.rules.board[ter].is_capital and game.rules.teams[game.state_dict[ter].owner] == enemy_team:
                    dists[1] = dist
                    remaining -= 1
                # Distance to nearest enemy factory
                if dists[2] < 0 and 4 in enemy_unit_indices:
                    dists[2] = dist
                    remaining -= 1
                # Distance to nearest enemy territory
                if dists[3] < 0 and (game.state_dict[ter].owner in game.rules.teams and game.rules.teams[game.state_dict[ter].owner] == enemy_team):
                    dists[3] = dist
                    remaining -= 1
                # Distance to nearest enemy transport
                if dists[4] < 0 and 5 in enemy_unit_indices:
                    dists[4] = dist
                    remaining -= 1
                # Distance to nearest enemy warship
                if dists[5] < 0 and enemy_unit_indices.intersection([6, 7, 8, 9, 10]):
                    dists[5] = dist
                    remaining -= 1
                # Get neighbors for BFS
                for neighbor in game.rules.board[ter].neighbors:
                    if neighbor not in already_seen:
                        next_territories.add(neighbor)
            current_territories.clear()
            current_territories.update(next_territories)
            already_seen.update(next_territories)
            next_territories.clear()
            dist += 1
        # Default to max value
        for i in range(len(dists)):
            if dists[i] < 0:
                dists[i] = dist + 1
        heuristics += dists

        return heuristics

    def get_value(self, game, territory_name='', player='', vuln=None, winning=0.5):
        inputs = np.array([self.get_heuristics(game, player, territory_name, vuln, winning)])
        return self.net.predict(inputs)[0]


class IsWinning(Heuristics):
    """
 - Total Unit Value Ratio (Axis vs Allies) compared to the start to determine who is winning
 - Same thing but just sea power
 - Same thing but just air power
 - Same thing but just land power
 - Might be worth literally checking every unit to see if there is a correlation but this might be crazy
 - Percent of unit value in range of the front line
 - Total income compared to start
 - Number of 'combat important territories' you control / have ranged jurisdiction over
 - Number of your vs. their factories that are in danger
 - Create some sort of "Similarity distance' function to compare current board with known 'winning' boards
 - Overall 'luck' value. Do battle calculator before every battle and add up the difference between expected ipc_swing for your side and actual
 - Could do a similar luck value based on percentages, where an actual win is 1 and a loss 0.
 - Obviously number of controlled capitals.
 - Number of factories taken from enemy
 - which team controls sue
    """

    def __init__(self, load_net=True):
        super().__init__('is_winning', load_net)

    def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        heuristics = list()

        # Controls Suez
        heuristics.append(1 if game.controls_suez('Allies') else (0 if game.controls_suez('Axis') else 0.5))

        # Controls Panama
        heuristics.append(1 if game.controls_panama('Allies') else 0)

        # Capitals owned by Allies
        allies_caps = 0
        for player_obj in game.players.values():
            allies_caps += (game.rules.teams[game.state_dict[player_obj.capital].owner] == 'Allies')
        heuristics.append(allies_caps)

        # Total unit values
        axis_unit_value = 0
        axis_land_value = 0
        axis_sea_value = 0
        axis_air_value = 0
        allies_unit_value = 0
        allies_land_value = 0
        allies_sea_value = 0
        allies_air_value = 0

        # Some other things
        allies_total_ipc = 0
        allies_controlled_factories = 0
        axis_total_ipc = 0
        axis_controlled_factories = 0
        for territory_key in game.state_dict.keys():
            ipc = game.rules.board[territory_key].ipc
            owner = game.state_dict[territory_key].owner
            if owner in game.rules.teams:
                if game.rules.teams[owner] == 'Allies':
                    allies_total_ipc += ipc
                else:
                    axis_total_ipc += ipc
            for unit_state in game.state_dict[territory_key].unit_state_list:
                if game.rules.get_unit(unit_state.type_index).unit_type == 'sea':
                    if game.rules.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_sea_value += game.rules.get_unit(unit_state.type_index).cost
                    elif game.rules.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_sea_value += game.rules.get_unit(unit_state.type_index).cost
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'land':
                    if game.rules.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            axis_controlled_factories += 0
                    elif game.rules.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            allies_controlled_factories += 0
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'air':
                    if game.rules.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_air_value += game.rules.get_unit(unit_state.type_index).cost
                    elif game.rules.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_air_value += game.rules.get_unit(unit_state.type_index).cost

        # to determine the baseline for who is winning. Obv they should be 'equal' to start
        heuristics.append(axis_unit_value)
        heuristics.append(axis_land_value)
        heuristics.append(axis_sea_value)
        heuristics.append(axis_air_value)
        heuristics.append(allies_unit_value)
        heuristics.append(allies_land_value)
        heuristics.append(allies_sea_value)
        heuristics.append(allies_air_value)

        heuristics.append(allies_total_ipc)
        heuristics.append(allies_controlled_factories)
        heuristics.append(axis_total_ipc)
        heuristics.append(axis_controlled_factories)

        # Important territories controlled by Allies
        heuristics.append(len([ter for ter in game.rules.win_cons if game.rules.teams[game.state_dict[ter].owner] == 'Allies']))

        # Get front line units
        allies_units_can_attack = list()
        axis_units_can_attack = list()
        allies_unit_value_can_be_attacked = 0
        axis_unit_value_can_be_attacked = 0
        for ter in vuln.territories.keys():
            allies_can_be_attacked = False
            axis_can_be_attacked = False
            if vuln.territories[ter]['Axis'] or game.state_dict[ter].owner in ('Germany', 'Japan'):
                for country in ('America', 'Britain', 'Russia'):
                    if vuln.territories[ter][country]:
                        axis_can_be_attacked = True
                        for unit_stack in vuln.territories[ter][country]:
                            for unit_state in unit_stack.get_unit_states():
                                if unit_state not in allies_units_can_attack:
                                    allies_units_can_attack.append(unit_state)
            if vuln.territories[ter]['Allies'] or game.state_dict[ter].owner in ('America', 'Britain', 'Russia'):
                for country in ('Germany', 'Japan'):
                    if vuln.territories[ter][country]:
                        allies_can_be_attacked = True
                        for unit_stack in vuln.territories[ter][country]:
                            for unit_state in unit_stack.get_unit_states():
                                if unit_state not in axis_units_can_attack:
                                    axis_units_can_attack.append(unit_state)
            if allies_can_be_attacked:
                allies_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                          for unit_state in vuln.territories[ter]['Allies']])
            if axis_can_be_attacked:
                axis_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                        for unit_state in vuln.territories[ter]['Axis']])
        allies_unit_value_can_attack = sum(game.rules.get_unit(unit_state.type_index).cost for unit_state in allies_units_can_attack)
        axis_unit_value_can_attack = sum(game.rules.get_unit(unit_state.type_index).cost for unit_state in axis_units_can_attack)

        # Percent of unit value that can attack the enemy
        heuristics.append(allies_unit_value_can_attack / allies_unit_value)
        heuristics.append(axis_unit_value_can_attack / axis_unit_value)

        # Percent of unit value that can be attacked by the enemy
        heuristics.append(allies_unit_value_can_be_attacked / allies_unit_value)
        heuristics.append(axis_unit_value_can_be_attacked / axis_unit_value)

        return heuristics


class Prioritization(Heuristics):
    def __init__(self, load_net=True):
        super().__init__('prioritization', load_net)

    def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        # TODO: This needs to be changed to be better
        heuristics = list()
        team = game.rules.teams[player]
        # Controls Suez
        heuristics.append(1 if game.controls_suez(team) else 0)

        # Controls Panama
        heuristics.append(1 if game.controls_panama(team) else 0)

        # Is winning
        heuristics.append(winning)

        # Extra capitals owned by this team
        caps = -3 if team == 'Allies' else -2
        for player_obj in game.players.values():
            caps += (game.rules.teams[game.state_dict[player_obj.capital].owner] == team)
        heuristics.append(caps)

        # Total unit values
        enemy_unit_value = 0
        enemy_land_value = 0
        enemy_sea_value = 0
        enemy_air_value = 0
        team_unit_value = 0
        team_land_value = 0
        team_sea_value = 0
        team_air_value = 0
        player_unit_value = 0
        player_land_value = 0
        player_sea_value = 0
        player_air_value = 0

        # Some other things
        team_total_ipc = 0
        team_controlled_factories = 0
        enemy_total_ipc = 0
        enemy_controlled_factories = 0
        player_total_ipc = 0
        player_controlled_factories = 0
        for territory_key in game.state_dict.keys():
            ipc = game.rules.board[territory_key].ipc
            owner = game.state_dict[territory_key].owner
            if owner == player:
                player_total_ipc += ipc
            if owner in game.rules.teams:
                if game.rules.teams[owner] == team:
                    team_total_ipc += ipc
                else:
                    enemy_total_ipc += ipc
            for unit_state in game.state_dict[territory_key].unit_state_list:
                if game.rules.get_unit(unit_state.type_index).unit_type == 'sea':
                    if unit_state.owner == player:
                        player_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        player_sea_value += game.rules.get_unit(unit_state.type_index).cost
                    if game.rules.teams[unit_state.owner] == team:
                        team_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        team_sea_value += game.rules.get_unit(unit_state.type_index).cost
                    else:
                        enemy_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        enemy_sea_value += game.rules.get_unit(unit_state.type_index).cost
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'land':
                    if unit_state.owner == player:
                        player_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        player_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            player_controlled_factories += 1
                    if game.rules.teams[unit_state.owner] == team:
                        team_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        team_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            team_controlled_factories += 1
                    else:
                        enemy_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        enemy_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            enemy_controlled_factories += 1
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'air':
                    if unit_state.owner == player:
                        player_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        player_air_value += game.rules.get_unit(unit_state.type_index).cost
                    if game.rules.teams[unit_state.owner] == team:
                        team_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        team_air_value += game.rules.get_unit(unit_state.type_index).cost
                    else:
                        enemy_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        enemy_air_value += game.rules.get_unit(unit_state.type_index).cost

        # to determine the baseline for who is winning. Obv they should be 'equal' to start
        # Total unit values
        heuristics.append(enemy_unit_value)
        heuristics.append(enemy_land_value)
        heuristics.append(enemy_sea_value)
        heuristics.append(enemy_air_value)
        heuristics.append(team_unit_value)
        heuristics.append(team_land_value)
        heuristics.append(team_sea_value)
        heuristics.append(team_air_value)
        heuristics.append(player_unit_value)
        heuristics.append(player_land_value)
        heuristics.append(player_sea_value)
        heuristics.append(player_air_value)

        # Some other things
        heuristics.append(team_total_ipc)
        heuristics.append(team_controlled_factories)
        heuristics.append(enemy_total_ipc)
        heuristics.append(enemy_controlled_factories)
        heuristics.append(player_total_ipc)
        heuristics.append(player_controlled_factories)

        # Important territories controlled by team
        heuristics.append(len([ter for ter in game.rules.win_cons if game.rules.teams[game.state_dict[ter].owner] == team]))

        # Get front line units
        allies_units_can_attack = list()
        axis_units_can_attack = list()
        allies_unit_value_can_be_attacked = 0
        axis_unit_value_can_be_attacked = 0
        player_units_can_attack = list()
        player_unit_value_can_be_attacked = 0
        for ter in vuln.territories.keys():
            allies_can_be_attacked = False
            axis_can_be_attacked = False
            if vuln.territories[ter]['Axis'] or game.state_dict[ter].owner in ('Germany', 'Japan'):
                for country in ('America', 'Britain', 'Russia'):
                    if vuln.territories[ter][country]:
                        axis_can_be_attacked = True
                        for unit_stack in vuln.territories[ter][country]:
                            for unit_state in unit_stack.get_unit_states():
                                if unit_state not in allies_units_can_attack:
                                    if country == player:
                                        player_units_can_attack.append(unit_state)
                                    allies_units_can_attack.append(unit_state)
            if vuln.territories[ter]['Allies'] or game.state_dict[ter].owner in ('America', 'Britain', 'Russia'):
                for country in ('Germany', 'Japan'):
                    if vuln.territories[ter][country]:
                        allies_can_be_attacked = True
                        for unit_stack in vuln.territories[ter][country]:
                            for unit_state in unit_stack.get_unit_states():
                                if unit_state not in axis_units_can_attack:
                                    if country == player:
                                        player_units_can_attack.append(unit_state)
                                    axis_units_can_attack.append(unit_state)
            if allies_can_be_attacked:
                allies_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                          for unit_state in vuln.territories[ter]['Allies']])
                if team == 'Allies':
                    player_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                              for unit_state in vuln.territories[ter]['Allies'] if unit_state.owner == player])
            if axis_can_be_attacked:
                axis_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                        for unit_state in vuln.territories[ter]['Axis']])
                if team == 'Axis':
                    player_unit_value_can_be_attacked += sum([game.rules.get_unit(unit_state.type_index).cost
                                                              for unit_state in vuln.territories[ter]['Axis'] if unit_state.owner == player])
        allies_unit_value_can_attack = sum(game.rules.get_unit(unit_state.type_index).cost for unit_state in allies_units_can_attack)
        axis_unit_value_can_attack = sum(game.rules.get_unit(unit_state.type_index).cost for unit_state in axis_units_can_attack)
        player_unit_value_can_attack = sum(game.rules.get_unit(unit_state.type_index).cost for unit_state in player_units_can_attack)

        heuristics.append(player_unit_value_can_attack / player_unit_value)
        heuristics.append(player_unit_value_can_be_attacked / player_unit_value)

        if team == 'Allies':
            heuristics.append(allies_unit_value_can_attack / team_unit_value)
            heuristics.append(allies_unit_value_can_be_attacked / team_unit_value)
            heuristics.append(axis_unit_value_can_attack / enemy_unit_value)
            heuristics.append(axis_unit_value_can_be_attacked / enemy_unit_value)
        else:
            heuristics.append(axis_unit_value_can_attack / team_unit_value)
            heuristics.append(axis_unit_value_can_be_attacked / team_unit_value)
            heuristics.append(allies_unit_value_can_attack / enemy_unit_value)
            heuristics.append(allies_unit_value_can_be_attacked / enemy_unit_value)

        return heuristics


class RiskTolerance(Heuristics):
    def __init__(self, load_net=True):
        super().__init__('should_attack', load_net)

    def get_value(self, game, territory_name='', player='', vuln=None, winning=0.5):
        # This NN outputs 1 or 0 for whether or not to attack for a certain vulnerability
        # So, do a binary search to figure threshold vulnerability
        inputs = np.array([self.get_heuristics(game, player, territory_name, vuln, winning)])
        min_val, max_val = -8, 8
        for _ in range(5):
            current = (min_val + max_val) / 2
            inputs[0][8] = current
            if self.net.predict(inputs)[0] >= 0.5:
                max_val = current
            else:
                min_val = current
        return (min_val + max_val) / 2


class GameController:
    def __init__(self, xml_file='', brain=None):
        self.game = BoardState.Game()
        if xml_file:
            self.game.export_reader(xml_file)
        if not brain:
            self.brain = Brain()
        else:
            self.brain = brain
        while self.do_one_phase():
            pass

    def do_one_phase(self):
        player = self.game.turn_state.player
        phase_num = self.game.turn_state.phase
        priority_names = ['battleship', 'factory', 'carrier', 'cruiser', 'bomber', 'fighter', 'destroyer', 'transport', 'sub', 'tank', 'aa', 'artillery', 'infantry']
        # Purchase phase
        if phase_num == 2:
            prioritizations = self.brain.get_values(self.game, player, prioritization=True)[0]
            print('Running purchase phase for ' + player + '...')
            build = phases.Build(self.game)
            for i in range(13):
                build.prioritizer(priority_names[i], prioritizations[i])
            build.build_units()
            print('The following units were purchased:')
            for unit_state in self.game.purchased_units[player]:
                print(self.game.rules.get_unit(unit_state.type_index).name)
            self.game.turn_state.phase += 1
            print('Purchase phase complete.')
            input('------------------------------------------------------------------------------')
        # Combat move phase is_winning=False, risk=False, importance=False, build=False, prioritization=False
        elif phase_num == 3:
            risk_tolerances, importance_values = self.brain.get_values(self.game, player, risk=True, importance=True)
            print('Running combat move phase for ' + player + '...')
            phases.CombatMove(self.game).do_combat_move(importance_values, risk_tolerances)
            self.game.turn_state.phase += 1
            print('Combat move phase complete.')
            input('------------------------------------------------------------------------------')
        # Battle phase
        elif phase_num == 4:
            importance_values = self.brain.get_values(self.game, player, importance=True)[0]
            print('Running battle phase for ' + player + '...')
            phases.Battles(self.game, importance_values)
            self.game.turn_state.phase += 1
            print('Battle phase complete.')
            input('------------------------------------------------------------------------------')
        # Non combat move phase
        elif phase_num == 5:
            risk_tolerances, importance_values = self.brain.get_values(self.game, player, risk=True, importance=True)
            print('Running non-combat move phase for ' + player + '...')
            phases.NonCombatMove(self.game, importance_values, risk_tolerances).do_non_combat_move()
            self.game.turn_state.phase += 1
            print('Non-combat move phase complete.')
            input('------------------------------------------------------------------------------')
        # Placement phase
        elif phase_num == 6:
            risk_tolerances, build_averages = self.brain.get_values(self.game, player, risk=True, build=True)
            print('Running placement phase for ' + player + '...')
            placement = phases.Place(self.game, self.game.purchased_units[player][:], build_averages, risk_tolerances)
            placement.build_strategy()
            placement.place()
            self.game.turn_state.phase = 2
            print('Placement phase complete.')
            print('Running cleanup phase...')
            cleanup = phases.Cleanup(self.game)
            game_result = cleanup.game_result
            print('Cleanup phase complete.')
            if game_result:
                print(game_result, 'has won the game!')
                return False
            input('------------------------------------------------------------------------------')
        # Other
        else:
            print('Unrecognized phase number (' + str(phase_num) + ')')
            return False
        return True


if __name__ == '__main__':
    # For a specific save, run GameController('path/to/xmlfile.xml')
    GameController()
