import BoardState
import phases
import BigBrain
import random


class FakeBrain(BigBrain.Brain):
    def __init__(self):
        self.risk = None
        self.importance = None
        self.build = None
        self.winning = None

    def get_all_values(self, game, player=''):
        risk_tolerances = {territory: 0.85 + random.random()/5 for territory in game.state_dict.keys()}
        importance_values = {territory: game.rules.board[territory].ipc / 12 for territory in game.state_dict.keys()}
        build_averages = {territory: max(0, random.randint(-15, 5)) for territory in game.state_dict.keys()}
        winning = random.random()
        return risk_tolerances, importance_values, build_averages, winning


class Testcases:
    def test_all(self):
        if self.test_export_reader():
            print('Export reader test successful')
        else:
            print('Export reader test failed')
        if self.test_calc_movement():
            print('Calc movement test successful')
        else:
            print('Calc movement test failed')
        if self.test_check_two_unit_transport():
            print('Check unit transport test successful')
        else:
            print('Check unit transport test failed')
        if self.test_phases():
            print('Phases test successful')
        else:
            print('Phases test failed')

    def is_unit_equal(self, unit_1, unit_2):
        if not unit_1 and not unit_2:
            return True
        if unit_1.owner == unit_2.owner and unit_1.type_index == unit_2.type_index and \
                self.is_unit_equal(unit_1.attached_to, unit_2.attached_to) and self.is_unit_list_equal(unit_1.attached_units, unit_2.attached_units):
            return True
        return False

    def is_unit_list_equal(self, unit_list_1, unit_list_2):
        if len(unit_list_1) != len(unit_list_2):
            print('Unit lists have different amounts of units')
            return False
        if len(unit_list_1) == 0:
            return True
        units_1, units_2 = unit_list_1[:], unit_list_2[:]
        for unit_1 in units_1:
            found_unit = None
            for unit_2 in units_2:
                if self.is_unit_equal(unit_1, unit_2):
                    found_unit = unit_2
                    break
            if found_unit:
                units_2.remove(found_unit)
            else:
                print('Unit lists have different units')
                return False
        return True

    def is_game_equal(self, game1, game2):
        # Check state dict
        if len(game1.state_dict) != len(game2.state_dict):
            print('State dicts are different lengths')
            return False
        for ter in game1.state_dict.keys():
            if ter not in game2.state_dict:
                print(ter + ' was in one game but not the other')
                return False
            ter_state_1, ter_state_2 = game1.state_dict[ter], game2.state_dict[ter]
            if ter_state_1.owner != ter_state_2.owner:
                print(ter + ' has different owners in each game')
                return False
            if ter_state_1.just_captured != ter_state_2.just_captured:
                print(ter + ' just_captured value is different')
                return False
            units_1, units_2 = ter_state_1.unit_state_list, ter_state_2.unit_state_list
            if not self.is_unit_list_equal(units_1, units_2):
                print(ter + ' has different units')
                return False
        for k in game1.purchased_units.keys():
            if not self.is_unit_list_equal(game1.purchased_units[k], game2.purchased_units[k]):
                print('Different purchased units')
                return False
        if game1.turn_state.player != game2.turn_state.player \
                or game1.turn_state.round_num != game2.turn_state.round_num \
                or game1.turn_state.phase != game2.turn_state.phase:
            print('Different turn states')
            return False
        return True

    def test_export_reader(self):
        # Test 1
        game1 = BoardState.Game()
        game2 = BoardState.Game()
        game2.export_reader('testcases/turn1.xml')
        if not self.is_game_equal(game1, game2):
            print('Failed export reader test 1.')
            return False

        # Test 2
        game2.export_reader('testcases/turn2.xml')
        game1.state_dict['Archangel'].unit_state_list = [BoardState.UnitState('Russia', 11)]
        game1.state_dict['Russia'].unit_state_list = [BoardState.UnitState('Russia', 4),
                                                      BoardState.UnitState('Russia', 0),
                                                      BoardState.UnitState('Russia', 3),
                                                      BoardState.UnitState('Russia', 11),
                                                      BoardState.UnitState('Russia', 11)]
        game1.state_dict['Caucasus'].unit_state_list = [BoardState.UnitState('Russia', 4),
                                                        BoardState.UnitState('Russia', 1),
                                                        BoardState.UnitState('Russia', 3)]
        game1.state_dict['West Russia'].unit_state_list = [BoardState.UnitState('Russia', 0),
                                                           BoardState.UnitState('Russia', 0),
                                                           BoardState.UnitState('Russia', 0),
                                                           BoardState.UnitState('Russia', 0),
                                                           BoardState.UnitState('Russia', 0),
                                                           BoardState.UnitState('Russia', 2),
                                                           BoardState.UnitState('Russia', 2),
                                                           BoardState.UnitState('Russia', 2),
                                                           BoardState.UnitState('Russia', 2),
                                                           BoardState.UnitState('Russia', 1)]
        game1.state_dict['West Russia'].owner = 'Russia'
        game1.turn_state.player = 'Germany'
        if not self.is_game_equal(game1, game2):
            print('Failed export reader test 2.')
            return False
        return True

    def test_calc_movement_one_unit(self, game, unit_type, current_ter, starting_ter, goal_ter, phase, expected_length, expected_path=None):
        unit = None
        for unit_state in game.state_dict[current_ter].unit_state_list:
            if unit_state.type_index == unit_type:
                unit = unit_state
                break
        if not unit:
            print('Incorrect unit for calc_movement with the following values:', unit_type, current_ter, starting_ter, goal_ter, phase)
            print('No unit with type index', unit_type, 'found in', current_ter)
            return False

        dist, path = game.calc_movement(unit, starting_ter, goal_ter, phase)
        if dist != expected_length:
            print('Incorrect moves used for calc_movement with the following values:', unit_type, current_ter, starting_ter, goal_ter, phase)
            print('Expected to get dist =', expected_length, 'but got', dist, 'instead')
            return False
        if expected_path is not None and expected_path != path:
            print('Incorrect path for calc_movement with the following values:', unit_type, current_ter, starting_ter, goal_ter, phase)
            print('Expected to get path =', expected_path, 'but got', path, 'instead')
            return False
        for i in range(len(path)-1):
            t1, t2 = path[i], path[i+1]
            if t2 not in game.rules.board[t1].neighbors:
                print('Incorrect path for calc_movement with the following values:', unit_type, current_ter, starting_ter, goal_ter, phase)
                print('Return path not all neighbors')
                return False
        return True

    def test_calc_movement(self):
        game = BoardState.Game()
        total = 0

        # Infantry
        count = 24
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Buryatia S.S.R.', 3, 1, ['Manchuria', 'Buryatia S.S.R.'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Buryatia S.S.R.', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Mongolia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Mongolia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', '62 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', '62 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Japan', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Japan', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Anhwei', 3, 1, ['Manchuria', 'Anhwei'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Anhwei', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Kiangsu', 3, 1, ['Manchuria', 'Kiangsu'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Kiangsu', 5, 1, ['Manchuria', 'Kiangsu'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Manchuria', 3, 0, ['Manchuria'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Manchuria', 5, 0, ['Manchuria'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Kiangsu', 'Manchuria', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Kiangsu', 'Manchuria', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Kiangsu', 'Kiangsu', '61 Sea Zone', 3, 0, ['Kiangsu', '61 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Kiangsu', 'Kiangsu', '61 Sea Zone', 5, 0, ['Kiangsu', '61 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Kwangtung', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Manchuria', 'Manchuria', 'Kwangtung', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 0, 'Burma', 'Burma', 'Yunnan', 3, 1, ['Burma', 'Yunnan'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Burma', 'Burma', 'Yunnan', 5, 1, ['Burma', 'Yunnan'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 0, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        total += count
        if count:
            print('Failed', count, 'out of 24 infantry tests')

        # Artillery
        count = 20
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Yunnan', 3, 1, ['Kwangtung', 'Yunnan'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Yunnan', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Szechwan', 3, 1, ['Kwangtung', 'Szechwan'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Szechwan', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Mongolia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Mongolia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Japan', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Japan', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Anhwei', 3, 1, ['Kwangtung', 'Anhwei'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Anhwei', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Kiangsu', 3, 1, ['Kwangtung', 'Kiangsu'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Kiangsu', 5, 1, ['Kwangtung', 'Kiangsu'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Kwangtung', 3, 0, ['Kwangtung'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Kwangtung', 5, 0, ['Kwangtung'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', '61 Sea Zone', 3, 0, ['Kwangtung', '61 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', '61 Sea Zone', 5, 0, ['Kwangtung', '61 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Manchuria', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Kwangtung', 'Kwangtung', 'Manchuria', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 1, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 1, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        total += count
        if count:
            print('Failed', count, 'out of 20 artillery tests')

        # Tank
        count = 34
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Ukraine S.S.R.', 3, 0, ['Ukraine S.S.R.'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Ukraine S.S.R.', 5, 0, ['Ukraine S.S.R.'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Caucasus', 3, 2, ['Ukraine S.S.R.', 'Caucasus'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Caucasus', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', '16 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', '16 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Turkey', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Turkey', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Bulgaria Romania', 3, 1, ['Ukraine S.S.R.', 'Bulgaria Romania'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Bulgaria Romania', 5, 1, ['Ukraine S.S.R.', 'Bulgaria Romania'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Southern Europe', 3, 2, ['Ukraine S.S.R.', 'Bulgaria Romania', 'Southern Europe'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Southern Europe', 5, 2, ['Ukraine S.S.R.', 'Bulgaria Romania', 'Southern Europe'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Italy', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Italy', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Italy', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Italy', 'Germany', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Germany', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Germany', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Poland', 3, 1, ['Ukraine S.S.R.', 'Poland'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Poland', 5, 1, ['Ukraine S.S.R.', 'Poland'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Baltic States', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Baltic States', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Karelia S.S.R.', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Karelia S.S.R.', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Archangel', 3, 2, ['Ukraine S.S.R.', 'West Russia', 'Archangel'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Archangel', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Russia', 3, 2, ['Ukraine S.S.R.', 'West Russia', 'Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Ukraine S.S.R.', 'Ukraine S.S.R.', 'Archangel', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Italy', 'Italy', '15 Sea Zone', 3, 0, ['Italy', '15 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Italy', 'Italy', '15 Sea Zone', 5, 0, ['Italy', '15 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 2, 'France', 'France', '15 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'France', 'France', '15 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        total += count
        if count:
            print('Failed', count, 'out of 34 tank tests')

        # AA guns
        count = 20
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', '15 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', '15 Sea Zone', 5, 0, ['Italy', '15 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 3, 'France', 'France', '15 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'France', 'France', '15 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'France', 'France', '14 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'France', 'France', '14 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Germany', 5, 1, ['Italy', 'Germany'])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Switzerland', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Switzerland', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Northwestern Europe', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Northwestern Europe', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Italy', 3, 0, ['Italy'])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'Italy', 'Italy', 5, 0, ['Italy'])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'France', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Italy', 'France', 'Germany', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Russia', 'Russia', 'West Russia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Russia', 'Russia', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 3, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        total += count
        if count:
            print('Failed', count, 'out of 20 AA gun tests')

        # Factories
        count = 16
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', '15 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', '15 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Germany', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Switzerland', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Switzerland', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Germany', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Italy', 3, 0, ['Italy'])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Italy', 'Italy', 5, 0, ['Italy'])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Germany', 'France', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Italy', 'Germany', 'France', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Russia', 'Russia', 'West Russia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Russia', 'Russia', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 4, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 16 factory tests')

        # Transports
        count = 32
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '11 Sea Zone', 3, 0, ['11 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '11 Sea Zone', 5, 0, ['11 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '10 Sea Zone', '11 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '10 Sea Zone', '11 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Eastern United States', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Eastern United States', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Central United States', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Central United States', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '55 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '55 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '18 Sea Zone', 3, 1, ['11 Sea Zone', '18 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '18 Sea Zone', 5, 1, ['11 Sea Zone', '18 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '19 Sea Zone', 3, 2, ['11 Sea Zone', '18 Sea Zone', '19 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '19 Sea Zone', 5, 2, ['11 Sea Zone', '18 Sea Zone', '19 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '22 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '22 Sea Zone', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '23 Sea Zone', 3, 2, ['11 Sea Zone', '12 Sea Zone', '23 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '23 Sea Zone', 5, 2, ['11 Sea Zone', '12 Sea Zone', '23 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '25 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '25 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '13 Sea Zone', 3, 2, ['11 Sea Zone', '12 Sea Zone', '13 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '13 Sea Zone', 5, 2, ['11 Sea Zone', '12 Sea Zone', '13 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '12 Sea Zone', 3, 1, ['11 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '12 Sea Zone', 5, 1, ['11 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '10 Sea Zone', 3, 1, ['11 Sea Zone', '10 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '10 Sea Zone', 5, 1, ['11 Sea Zone', '10 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '1 Sea Zone', 3, 2, ['11 Sea Zone', '10 Sea Zone', '1 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '1 Sea Zone', 5, 2, ['11 Sea Zone', '10 Sea Zone', '1 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '9 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', '9 Sea Zone', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Venezuela', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 5, '11 Sea Zone', '11 Sea Zone', 'Venezuela', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 32 transport tests')

        # Submarines
        count = 30
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '9 Sea Zone', 3, 0, ['9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '9 Sea Zone', 5, 0, ['9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '5 Sea Zone', '5 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '5 Sea Zone', '5 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '8 Sea Zone', 3, 1, ['9 Sea Zone', '8 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '8 Sea Zone', 5, 1, ['9 Sea Zone', '8 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '2 Sea Zone', 3, 1, ['9 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '2 Sea Zone', 5, 1, ['9 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '1 Sea Zone', 3, 2, ['9 Sea Zone', '2 Sea Zone', '1 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '1 Sea Zone', 5, 2, ['9 Sea Zone', '2 Sea Zone', '1 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'Greenland', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'Greenland', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'France', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'France', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'Spain Portugal', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', 'Spain Portugal', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '22 Sea Zone', 3, 2, ['9 Sea Zone', '12 Sea Zone', '22 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '22 Sea Zone', 5, 2, ['9 Sea Zone', '12 Sea Zone', '22 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '10 Sea Zone', 3, 2, ['9 Sea Zone', '10 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '10 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '11 Sea Zone', 3, 2, ['9 Sea Zone', '12 Sea Zone', '11 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '11 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '6 Sea Zone', 3, 2, ['9 Sea Zone', '8 Sea Zone', '6 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '6 Sea Zone', 5, 2, ['9 Sea Zone', '8 Sea Zone', '6 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '13 Sea Zone', 3, 1, ['9 Sea Zone', '13 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '13 Sea Zone', 5, 1, ['9 Sea Zone', '13 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '14 Sea Zone', 3, 2, ['9 Sea Zone', '13 Sea Zone', '14 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '14 Sea Zone', 5, 2, ['9 Sea Zone', '13 Sea Zone', '14 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '25 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '9 Sea Zone', '9 Sea Zone', '25 Sea Zone', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 30 submarine tests')

        # Destroyers
        count = 30
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '7 Sea Zone', 3, 0, ['7 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '7 Sea Zone', 5, 0, ['7 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '9 Sea Zone', 3, 1, ['7 Sea Zone', '9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '9 Sea Zone', 5, 1, ['7 Sea Zone', '9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '12 Sea Zone', 3, 2, ['7 Sea Zone', '9 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '12 Sea Zone', 5, 2, ['7 Sea Zone', '9 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '22 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '22 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '10 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '10 Sea Zone', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '2 Sea Zone', 3, 1, ['7 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '2 Sea Zone', 5, 1, ['7 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '5 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', '5 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'Eire', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'Eire', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'United Kingdom', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'United Kingdom', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'Norway', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '7 Sea Zone', '7 Sea Zone', 'Norway', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '15 Sea Zone', 3, 2, ['17 Sea Zone', '15 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '15 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '14 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '14 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '34 Sea Zone', 3, 1, ['17 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '34 Sea Zone', 5, 1, ['17 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '35 Sea Zone', 3, 2, ['17 Sea Zone', '34 Sea Zone', '35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '35 Sea Zone', 5, 2, ['17 Sea Zone', '34 Sea Zone', '35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '33 Sea Zone', 3, 2, ['17 Sea Zone', '34 Sea Zone', '33 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '17 Sea Zone', '17 Sea Zone', '33 Sea Zone', 5, 2, ['17 Sea Zone', '34 Sea Zone', '33 Sea Zone'])
        total += count
        if count:
            print('Failed', count, 'out of 30 destroyer tests')

        # Cruisers
        count = 22
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '35 Sea Zone', 3, 0, ['35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '35 Sea Zone', 5, 0, ['35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '50 Sea Zone', '36 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '50 Sea Zone', '36 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', 'India', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', 'India', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', 'Saudi Arabia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', 'Saudi Arabia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '31 Sea Zone', 3, 1, ['35 Sea Zone', '31 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '31 Sea Zone', 5, 1, ['35 Sea Zone', '31 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '34 Sea Zone', 3, 1, ['35 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '34 Sea Zone', 5, 1, ['35 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '17 Sea Zone', 3, 2, ['35 Sea Zone', '34 Sea Zone', '17 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '17 Sea Zone', 5, 2, ['35 Sea Zone', '34 Sea Zone', '17 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '37 Sea Zone', 3, 2, ['35 Sea Zone', '37 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '37 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '46 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '46 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '30 Sea Zone', 3, 2, ['35 Sea Zone', '31 Sea Zone', '30 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '30 Sea Zone', 5, 2, ['35 Sea Zone', '31 Sea Zone', '30 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '28 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 8, '35 Sea Zone', '35 Sea Zone', '28 Sea Zone', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 22 cruiser tests')

        # Carriers
        count = 22
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '35 Sea Zone', 3, 0, ['35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '35 Sea Zone', 5, 0, ['35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '50 Sea Zone', '36 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '50 Sea Zone', '36 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', 'India', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', 'India', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', 'Saudi Arabia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', 'Saudi Arabia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '31 Sea Zone', 3, 1, ['35 Sea Zone', '31 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '31 Sea Zone', 5, 1, ['35 Sea Zone', '31 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '34 Sea Zone', 3, 1, ['35 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '34 Sea Zone', 5, 1, ['35 Sea Zone', '34 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '17 Sea Zone', 3, 2, ['35 Sea Zone', '34 Sea Zone', '17 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '17 Sea Zone', 5, 2, ['35 Sea Zone', '34 Sea Zone', '17 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '37 Sea Zone', 3, 2, ['35 Sea Zone', '37 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '37 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '46 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '46 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '30 Sea Zone', 3, 2, ['35 Sea Zone', '31 Sea Zone', '30 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '30 Sea Zone', 5, 2, ['35 Sea Zone', '31 Sea Zone', '30 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '28 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 9, '35 Sea Zone', '35 Sea Zone', '28 Sea Zone', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 22 carrier tests')

        # Battleships
        count = 28
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '7 Sea Zone', 3, 0, ['7 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '7 Sea Zone', 5, 0, ['7 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '9 Sea Zone', 3, 1, ['7 Sea Zone', '9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '9 Sea Zone', 5, 1, ['7 Sea Zone', '9 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '12 Sea Zone', 3, 2, ['7 Sea Zone', '9 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '12 Sea Zone', 5, 2, ['7 Sea Zone', '9 Sea Zone', '12 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '22 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '22 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '10 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '10 Sea Zone', 5, 2)
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '2 Sea Zone', 3, 1, ['7 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '2 Sea Zone', 5, 1, ['7 Sea Zone', '2 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '5 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', '5 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'Eire', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'Eire', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'United Kingdom', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'United Kingdom', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'Norway', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '7 Sea Zone', '7 Sea Zone', 'Norway', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '14 Sea Zone', 3, 1, ['15 Sea Zone', '14 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '14 Sea Zone', 5, 1, ['15 Sea Zone', '14 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '13 Sea Zone', 3, 2, ['15 Sea Zone', '14 Sea Zone', '13 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '13 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '17 Sea Zone', 3, 2, ['15 Sea Zone', '17 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '17 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '34 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '15 Sea Zone', '15 Sea Zone', '34 Sea Zone', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 28 battleship tests')

        # Fighters
        count = 38
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Germany', 3, 0, ['Germany'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Germany', 5, 0, ['Germany'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Poland', 'Germany', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Poland', 'Germany', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Poland', 3, 1, ['Germany', 'Poland'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Poland', 5, 1, ['Germany', 'Poland'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Spain Portugal', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Spain Portugal', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', '8 Sea Zone', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', '8 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', '9 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', '9 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Poland', 'Poland', 'Morocco', 3, 4)
        count -= self.test_calc_movement_one_unit(game, 11, 'Poland', 'Poland', 'Morocco', 5, 4)
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Russia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Caucasus', 3, 3)
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Caucasus', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Karelia S.S.R.', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 11, 'Germany', 'Germany', 'Karelia S.S.R.', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '32 Sea Zone', 3, 2, ['37 Sea Zone', '31 Sea Zone', '32 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '32 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '33 Sea Zone', 3, 3, ['37 Sea Zone', '31 Sea Zone', '32 Sea Zone', '33 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '33 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', 'French Madagascar', 3, 3)
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '33 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '27 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '27 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '35 Sea Zone', 3, 1, ['37 Sea Zone', '35 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 11, '37 Sea Zone', '37 Sea Zone', '35 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Hawaiian Islands', 'Hawaiian Islands', '53 Sea Zone', 3, 1, ['Hawaiian Islands', '53 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Hawaiian Islands', 'Hawaiian Islands', '53 Sea Zone', 5, 1, ['Hawaiian Islands', '53 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Hawaiian Islands', 'Hawaiian Islands', '41 Sea Zone', 3, 3)
        count -= self.test_calc_movement_one_unit(game, 11, 'Hawaiian Islands', 'Hawaiian Islands', '41 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Western United States', 'Western United States', '41 Sea Zone', 3, 4)
        count -= self.test_calc_movement_one_unit(game, 11, 'Western United States', 'Western United States', '41 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        total += count
        if count:
            print('Failed', count, 'out of 38 fighter tests')

        # Bombers
        count = 24
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Eastern United States', 3, 0, ['Eastern United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Eastern United States', 5, 0, ['Eastern United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 3, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Eastern Canada', 5, 1, ['Eastern United States', 'Eastern Canada'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'United Kingdom', 'Eastern United States', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'United Kingdom', 'Eastern United States', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Central United States', 3, 1, ['Eastern United States', 'Central United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Central United States', 5, 1, ['Eastern United States', 'Central United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Western United States', 3, 2, ['Eastern United States', 'Central United States', 'Western United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Western United States', 5, 2, ['Eastern United States', 'Central United States', 'Western United States'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Brazil', 3, 4)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Brazil', 5, 4)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Venezuela', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Venezuela', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '26 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '26 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Soviet Far East', 3, 6)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Soviet Far East', 5, 6)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '53 Sea Zone', 3, 4, ['Eastern United States', 'Central United States', 'Western United States', '56 Sea Zone', '53 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '53 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Finland', 3, 5)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Finland', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Vologda', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Vologda', 5, -1, [])
        total += count
        if count:
            print('Failed', count, 'out of 24 bomber tests')

        # Other tests that require pieces to be moved
        count = 96
        # just_captured test
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '27 Sea Zone', 3, 5)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Union of South Africa', 3, 6)
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Union of South Africa', 5, 6)
        game.state_dict['Union of South Africa'].just_captured = True
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', '27 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Union of South Africa', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 12, 'Eastern United States', 'Eastern United States', 'Union of South Africa', 5, -1, [])
        # Battleships use all movement when entering combat
        game.state_dict['27 Sea Zone'].unit_state_list = [BoardState.UnitState('Britain', 10)]
        game.state_dict['28 Sea Zone'].unit_state_list = [BoardState.UnitState('Germany', 10)]
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, -1, [])
        # Ships can move through subs and transports
        game.state_dict['27 Sea Zone'].unit_state_list = [BoardState.UnitState('Britain', 10), BoardState.UnitState('Britain', 9),
                                                          BoardState.UnitState('Britain', 8), BoardState.UnitState('Britain', 7),
                                                          BoardState.UnitState('Britain', 6), BoardState.UnitState('Britain', 5)]
        game.state_dict['28 Sea Zone'].unit_state_list = [BoardState.UnitState('Germany', 6), BoardState.UnitState('Germany', 5)]
        count -= self.test_calc_movement_one_unit(game, 5, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 5, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 7, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 8, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 9, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 3, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 3, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '28 Sea Zone', 5, 1, ['27 Sea Zone', '28 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 10, '27 Sea Zone', '27 Sea Zone', '29 Sea Zone', 5, 2, ['27 Sea Zone', '28 Sea Zone', '29 Sea Zone'])
        # Subs can move through non-destroyer sea zones
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '27 Sea Zone', 3, 2, ['28 Sea Zone', '27 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '26 Sea Zone', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '27 Sea Zone', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '26 Sea Zone', 5, -1, [])
        game.state_dict['27 Sea Zone'].unit_state_list.pop(3)
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '27 Sea Zone', 3, 1, ['28 Sea Zone', '27 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '26 Sea Zone', 3, 2, ['28 Sea Zone', '27 Sea Zone', '26 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '27 Sea Zone', 5, 1, ['28 Sea Zone', '27 Sea Zone'])
        count -= self.test_calc_movement_one_unit(game, 6, '28 Sea Zone', '28 Sea Zone', '26 Sea Zone', 5, 2, ['28 Sea Zone', '27 Sea Zone', '26 Sea Zone'])
        # Tanks can blitz
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 3, 2, ['Caucasus', 'West Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 5, -1, [])
        game.state_dict['West Russia'].unit_state_list.clear()
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 3, 1, ['Caucasus', 'West Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 3, 2, ['Caucasus', 'West Russia', 'Belorussia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 5, -1, [])
        # Tank that has already moved
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 3, 1, ['Caucasus', 'Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 3, 2, ['Caucasus', 'Russia', 'Vologda'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 5, 1, ['Caucasus', 'Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 5, 2, ['Caucasus', 'Russia', 'Vologda'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 3, 2, ['Caucasus', 'Ukraine S.S.R.'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 5, -1, [])
        for unit_state in game.state_dict['Caucasus'].unit_state_list:
            if unit_state.type_index == 2:
                unit_state.moves_used = 1
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 3, 1, ['Caucasus', 'West Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 3, 1, ['Caucasus', 'Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 5, 1, ['Caucasus', 'Russia'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 3, 1, ['Caucasus', 'Ukraine S.S.R.'])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 5, -1, [])
        for unit_state in game.state_dict['Caucasus'].unit_state_list:
            if unit_state.type_index == 2:
                unit_state.moves_used = 2
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Belorussia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Vologda', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 2, 'Caucasus', 'Caucasus', 'Ukraine S.S.R.', 5, -1, [])
        # Fighter that has already moved
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'West Russia', 3, 1, ['Russia', 'West Russia'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Belorussia', 3, 2, ['Russia', 'West Russia', 'Belorussia'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Belorussia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Baltic States', 3, 3)
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Baltic States', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Yakut S.S.R.', 3, 3)
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Yakut S.S.R.', 5, 3)
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Evenki National Okrug', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Evenki National Okrug', 5, 2)
        for unit_state in game.state_dict['Russia'].unit_state_list:
            if unit_state.type_index == 11:
                unit_state.moves_used = 2
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'West Russia', 3, 1, ['Russia', 'West Russia'])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'West Russia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Belorussia', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Belorussia', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Baltic States', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Baltic States', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Yakut S.S.R.', 3, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Yakut S.S.R.', 5, -1, [])
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Evenki National Okrug', 3, 2)
        count -= self.test_calc_movement_one_unit(game, 11, 'Russia', 'Russia', 'Evenki National Okrug', 5, 2)
        total += count
        if count:
            print('Failed', count, 'out of 96 other tests')

        if total:
            print('Failed', total, 'tests overall')
        return total == 0

    def test_check_two_unit_transport(self):
        game = BoardState.Game()

        inf_1, inf_2, aa_1 = game.state_dict['Western United States'].unit_state_list[:3]
        inf_3, inf_4 = game.state_dict['Midway'].unit_state_list[0], game.state_dict['Hawaiian Islands'].unit_state_list[0]
        trans = game.state_dict['56 Sea Zone'].unit_state_list[0]
        failed = list()
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(1)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(2)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(3)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(4)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(5)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(6)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(7)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(8)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(9)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_2, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(10)

        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(11)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(12)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(13)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(14)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(15)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(16)
        if not game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(17)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(18)
        if game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(19)
        if not game.check_two_unit_transport(inf_1, 'Western United States', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(20)

        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(21)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(22)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(23)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(24)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(25)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(26)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(27)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(28)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(29)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(30)

        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(31)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(32)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(33)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(34)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(35)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(36)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(37)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(38)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(39)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(40)

        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(41)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(42)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(43)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(44)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(45)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(46)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(47)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(48)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(49)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_3, 'Midway', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(50)

        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(51)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(52)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(53)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(54)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(55)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(56)
        if not game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(57)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(58)
        if not game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(59)
        if game.check_two_unit_transport(inf_3, 'Midway', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(60)

        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(61)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(62)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(63)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(64)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '55 Sea Zone', 3):
            failed.append(65)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(66)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(67)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(68)
        if not game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(69)
        if game.check_two_unit_transport(inf_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '55 Sea Zone', 5):
            failed.append(70)

        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(71)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(72)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(73)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(74)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '55 Sea Zone', 3):
            failed.append(75)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(76)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(77)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(78)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(79)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_4, 'Hawaiian Islands', trans, '56 Sea Zone', '55 Sea Zone', 5):
            failed.append(80)

        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(81)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(82)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(83)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '52 Sea Zone', 3):
            failed.append(84)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '55 Sea Zone', 3):
            failed.append(85)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(86)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(87)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(88)
        if not game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '52 Sea Zone', 5):
            failed.append(89)
        if game.check_two_unit_transport(inf_4, 'Hawaiian Islands', aa_1, 'Western United States', trans, '56 Sea Zone', '55 Sea Zone', 5):
            failed.append(90)

        game.state_dict['Western United States'].unit_state_list.remove(inf_1)
        game.state_dict['56 Sea Zone'].unit_state_list.append(inf_1)
        trans.attached_units.append(inf_1)
        inf_1.attached_to = trans

        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(91)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(92)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(93)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(94)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(95)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(96)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(97)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(98)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(99)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', inf_2, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(100)

        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(101)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(102)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(103)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(104)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(105)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(106)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(107)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(108)
        if game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(109)
        if not game.check_two_unit_transport(inf_1, '56 Sea Zone', aa_1, 'Western United States', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(110)

        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', 'Iwo Jima', 3):
            failed.append(111)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '59 Sea Zone', 3):
            failed.append(112)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', 'Wake Island', 3):
            failed.append(113)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '51 Sea Zone', 3):
            failed.append(114)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '54 Sea Zone', 3):
            failed.append(115)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', 'Iwo Jima', 5):
            failed.append(116)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '59 Sea Zone', 5):
            failed.append(117)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', 'Wake Island', 5):
            failed.append(118)
        if game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '51 Sea Zone', 5):
            failed.append(119)
        if not game.check_two_unit_transport(aa_1, 'Western United States', inf_1, '56 Sea Zone', trans, '56 Sea Zone', '54 Sea Zone', 5):
            failed.append(120)

        if failed:
            print('Check unit transport failed on the following tests:', failed)
        return not failed

    def test_phases(self):
        BigBrain.GameController(brain=FakeBrain())
        return True


Testcases().test_all()
