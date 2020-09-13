import BoardState
import BigBrain
import os
import phases
import xml.etree.cElementTree as ET


class CreateData:
    def __init__(self, game_folders_and_winners, data_folder):
        self.data_files = [os.path.join(data_folder, file_name) for file_name in ('importance_values.txt', 'should_attack.txt', 'build_averages.txt', 'is_winning.txt', 'prioritization.txt')]
        for data_file in self.data_files:
            with open(data_file, 'w+'):
                pass
        self.games = list()
        game = BoardState.Game()
        for game_folder, winner in game_folders_and_winners:
            xml_files = os.listdir(game_folder)
            game.export_reader(os.path.join(game_folder, max(xml_files, key=lambda x: int(str(x).split('.')[0]))))
            total_turns = game.turn_state.round_num
            self.games.append([winner, total_turns, [os.path.join(game_folder, xml_file) for xml_file in xml_files]])

    def get_built_units(self, game, prev_units, prev_player, prev_turn, current_units):
        if prev_units is None:
            return None
        if game.turn_state.player != game.rules.turn_order[prev_player]:
            return None
        if prev_player == 'America':
            if prev_turn + 1 != game.turn_state.round_num:
                return None
        else:
            if prev_turn != game.turn_state.round_num:
                return None
        built_units = dict()
        for unit_id in current_units.keys():
            if unit_id not in prev_units.keys():
                ter, unit_state, transport = current_units[unit_id]
                if ter not in built_units:
                    built_units[ter] = list()
                built_units[ter].append(unit_state)
        return built_units

    def get_expected_importances(self, game, vuln):
        importances = dict()
        for ter, ter_state in game.state_dict.items():
            if ter_state.owner == 'Sea Zone' or ter_state.owner == game.turn_state.player:
                importances[ter] = vuln.get_vulnerability(ter, defender=game.turn_state.player)
        max_vuln = max(importances.values())
        min_vuln = min(importances.values())
        for ter in importances.keys():
            importances[ter] = (importances[ter] + min_vuln) / (max_vuln - min_vuln)
        return importances

    def can_build_here(self, game, ter, must_be_land=False):
        ter_state = game.state_dict[ter]
        territory = game.rules.board[ter]
        if territory.is_water:
            if must_be_land:
                return False
            for neighbor in territory.neighbors:
                if self.can_build_here(game, neighbor, True):
                    return True
            return False
        for unit_state in ter_state.unit_state_list:
            if unit_state.type_index == 4 and unit_state.owner == game.turn_state.player:
                return True
        return False

    def parse_one_game(self, game, xml_file, prev_units, prev_player, prev_turn, winner, total_turns):
        current_units = game.export_reader(xml_file)
        player = game.turn_state.player

        # IsWinner data
        vuln = phases.Vulnerability(game)
        expected_winner = 0.5 + 0.5 * game.turn_state.round_num / total_turns
        winner_heuristics = BigBrain.IsWinning(False).get_heuristics(game, vuln=vuln)
        with open(self.data_files[3], 'a') as f:
            f.write(','.join(str(k) for k in winner_heuristics) + ';' + str(expected_winner) + '\n')

        # Importance Values
        heuristics = {ter: ','.join([str(k) for k in BigBrain.Heuristics('', False).get_heuristics(game, player, ter, vuln, expected_winner)]) for ter in game.state_dict.keys()}
        expected_importances = self.get_expected_importances(game, vuln)
        with open(self.data_files[0], 'a') as f:
            for ter, val in expected_importances.items():
                f.write(heuristics[ter] + ';' + str(val) + '\n')

        # Build averages
        built_units = self.get_built_units(game, prev_units, prev_player, prev_turn, current_units)
        if built_units is not None:
            with open(self.data_files[2], 'a') as f:
                for ter in game.state_dict.keys():
                    if self.can_build_here(game, ter):
                        if ter in built_units:
                            f.write(heuristics[ter] + ';' + str(len(built_units[ter])) + '\n')
                        else:
                            f.write(heuristics[ter] + ';0\n')

        # Prioritizations
        if winner == 'Axis':
            expected_winner = 1 - expected_winner
        if built_units is not None:
            priority_names = ['battleship', 'factory', 'carrier', 'cruiser', 'bomber', 'fighter', 'destroyer', 'transport', 'sub', 'tank', 'aa', 'artillery', 'infantry']
            expected_priorities = {unit_name: 0 for unit_name in priority_names}
            for units in built_units.values():
                for unit_state in units:
                    unit = game.rules.get_unit(unit_state.type_index)
                    expected_priorities[unit.name] += unit.cost
            with open(self.data_files[4], 'a') as f:
                f.write(','.join(str(k) for k in BigBrain.Prioritization(False).get_heuristics(game, player, vuln=vuln, winning=expected_winner)) + ';' + ','.join(str(expected_priorities[unit]) for unit in priority_names) + '\n')

        # Should attack
        root = ET.parse(xml_file).getroot()
        attacked = {territory.get("name") for territory in root.find("attackedTerritories").findall("territory")}
        with open(self.data_files[1], 'a') as f:
            for ter in game.state_dict.keys():
                if vuln.territories[ter][player]:
                    res = 1 if ter in attacked else 0
                    f.write(heuristics[ter] + ';' + str(res) + '\n')

        return current_units, player, game.turn_state.round_num

    def parse_full_game(self, winner, total_turns, xml_files):
        prev_units, prev_player, prev_turn = None, None, None
        game = BoardState.Game()
        for xml_file in xml_files:
            prev_units, prev_player, prev_turn = self.parse_one_game(game, xml_file, prev_units, prev_player, prev_turn, winner, total_turns)

    def parse_games(self):
        for winner, total_turns, xml_files in self.games:
            self.parse_full_game(winner, total_turns, xml_files)


if __name__ == '__main__':
    CreateData([('training_data/Game27', 'Allies'), ('training_data/Game45', 'Axis')], 'NNData').parse_games()
