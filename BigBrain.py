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


class Brain:
    def __init__(self):
        self.risk = RiskTolerance()
        self.importance = ImportanceValue()
        self.build = BuildAverage()
        self.winning = IsWinning()

    def get_all_values(self, game, player=''):
        vuln = phases.Vulnerability(game)
        winning = self.winning.get_value(game, vuln=vuln)
        if not player:
            player = game.turn_state.player
        risk_tolerances = {territory: self.risk.get_value(game, territory, player, vuln, winning) for territory in game.state_dict.keys()}
        importance_values = {territory: self.importance.get_value(game, territory, player, vuln, winning) for territory in game.state_dict.keys()}
        build_averages = {territory: self.build.get_value(game, territory, player, vuln, winning) for territory in game.state_dict.keys()}
        if game.rules.teams[player] == 'Axis':
            winning = 1 - winning
        return risk_tolerances, importance_values, build_averages, winning


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
        return self.get_generic_heuristics(game, player, territory_name, vuln, winning)

    def get_value(self, game, territory_name='', player='', vuln=None, winning=0.5):
        inputs = self.get_heuristics(game, territory_name, player, vuln, winning)
        return self.net.predict(inputs)

    def get_generic_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        generic_heuristics = list()
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]
        friendly_team, enemy_team = game.rules.teams[player], game.rules.enemy_team(player=player)

        # Turn number
        generic_heuristics.append(game.turn_state.round_num)

        # Who is winning
        generic_heuristics.append(winning)

        # Is capital
        generic_heuristics.append(1 if territory.is_capital else 0)

        # Is water
        generic_heuristics.append(1 if territory.is_water else 0)

        # Defensive power of territory
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == friendly_team:
                power += game.rules.get_unit(unit_state.type_index).defense
        generic_heuristics.append(power)

        # IPC value
        generic_heuristics.append(territory.ipc)

        # Is key territory
        generic_heuristics.append(1 if territory_name in game.rules.win_cons else 0)

        # Vulnerability (player = defender)
        generic_heuristics.append(vuln.get_vulnerability(territory_name, defender=friendly_team))

        # Vulnerability (player = attacker)
        generic_heuristics.append(vuln.get_vulnerability(territory_name, attacker=player))

        # Player's attack power within range of territory
        generic_heuristics.append(sum(unit_stack.get_attack_power() for unit_stack in vuln.territories[territory_name][player]))

        # Enemies' attack power within range of territory
        power = 0
        for other_player, team in game.rules.teams.items():
            if team == enemy_team:
                power += sum(unit_stack.get_attack_power() for unit_stack in vuln.territories[territory_name][other_player])
        generic_heuristics.append(power)

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
                if dists[3] < 0 and game.rules.teams[game.state_dict[ter].owner] == enemy_team:
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
        generic_heuristics += dists

        return generic_heuristics


class RiskTolerance(Heuristics):
    """
    - actual battles in that territory risk tolerance calc
    - what turn is it
    - are you winning?
    - has factory
    - is attacking?
    - hawkes defense score of attacking territiroy
    - ipc
    - distace from capital, etc.
    """
    def __init__(self):
        super().__init__('risk_tolerance')

    # This is currently commented out because it is identical to the function it would override
    """def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        heuristics = self.get_generic_heuristics(game, player, territory_name)
        return heuristics"""


class ImportanceValue(Heuristics):
    """
    - average power in range of territory across the games
    - average number of battles in the territory/turn
    - is victory city
    - is frontline
    - distance to nearest enmny factory
    - distacne to your capital
    - distance to nearest enmny capital
    - ipc value
    -
    """

    def __init__(self):
        super().__init__('importance_value')

    # This is currently commented out because it is identical to the function it would override
    """def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        heuristics = self.get_generic_heuristics(game, player, territory_name)
        return heuristics"""


class BuildAverage(Heuristics):
    """
    - distance to nearest enemny land territory
    - distance to nearest enemy transport
    - distance to nearest enemy military ship
    - in-range enmny power
    - is frontline
    - distance from capital
    - is victory city
    """

    def __init__(self):
        super().__init__('build_average')

    # This is currently commented out because it is identical to the function it would override
    """def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        heuristics = self.get_generic_heuristics(game, player, territory_name)
        return heuristics"""


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

    def __init__(self):
        super().__init__('is_winning')

    def get_heuristics(self, game, player='', territory_name='', vuln=None, winning=0.5):
        heuristics = list()

        # Controls Suez
        heuristics.append(1 if game.controls_suez('Allies') else (0 if game.controls_suez('Axis') else 0.5))

        # Controls Panama
        heuristics.append(1 if game.controls_panama('Allies') else 0)

        # Capitals owned by Allies
        allies_caps = 0
        for player_obj in game.players:
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
        for territory_key in game.state_dict.eys():
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
            if vuln.territories[ter]['Axis']:
                for country in ('America', 'Britain', 'Russia'):
                    if vuln.territories[ter][country]:
                        axis_can_be_attacked = True
                        for unit_stack in vuln.territories[ter][country]:
                            for unit_state in unit_stack.get_unit_states():
                                if unit_state not in allies_units_can_attack:
                                    allies_units_can_attack.append(unit_state)
            if vuln.territories[ter]['Allies']:
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


class GameController:
    def __init__(self, xml_file='', brain=None):
        self.game = BoardState.Game()
        if not xml_file:
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
        risk_tolerances, importance_values, build_averages, is_winning = self.brain.get_all_values(self.game, player)
        # Purchase phase
        if phase_num == 2:
            print('Running purchase phase for ' + player + '...')
            phases.Build(self.game).build_units()
            print('The following units were purchased:')
            for unit_state in self.game.purchased_units[player]:
                print(self.game.rules.get_unit(unit_state).name)
            self.game.turn_state.phase += 1
            print('Purchase phase complete.')
            input('------------------------------------------------------------------------------')
        # Combat move phase
        elif phase_num == 3:
            print('Running combat move phase for ' + player + '...')
            combat_move = phases.CombatMove(self.game)
            combat_move.do_combat_move(importance_values, risk_tolerances)
            self.game.turn_state.phase += 1
            print('Combat move phase complete.')
            input('------------------------------------------------------------------------------')
        # Battle phase
        elif phase_num == 4:
            print('Running battle phase for ' + player + '...')
            phases.Battles(self.game, importance_values)
            self.game.turn_state.phase += 1
            print('Battle phase complete.')
            input('------------------------------------------------------------------------------')
        # Non combat move phase
        elif phase_num == 5:
            print('Running non-combat move phase for ' + player + '...')
            non_combat = phases.NonCombatMove(self.game, importance_values, risk_tolerances)
            non_combat.do_non_combat_move()
            self.game.turn_state.phase += 1
            print('Non-combat move phase complete.')
            input('------------------------------------------------------------------------------')
        # Placement phase
        elif phase_num == 6:
            print('Running placement phase for ' + player + '...')
            phases.Place(self.game, self.game.purchased_units, build_averages, risk_tolerances)
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


# Run with:
# GameController('path/to/xmlfile.xml')

