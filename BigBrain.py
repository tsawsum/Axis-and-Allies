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


class Brain:
    def __init__(self):
        self.risk = RiskTolerance()
        self.importance = ImportanceValue()
        self.build = BuildAverage()
        self.winning = IsWinning()

    def get_risk_tolerances(self, game, player=''):
        if not player:
            player = game.turn_state.player
        return {territory: self.risk.get_value(game, territory, player) for territory in game.state_dict.keys()}

    def get_importance_values(self, game, player=''):
        if not player:
            player = game.turn_state.player
        return {territory: self.importance.get_value(game, territory, player) for territory in game.state_dict.keys()}

    def get_build_average(self, game, player=''):
        if not player:
            player = game.turn_state.player
        return {territory: self.build.get_value(game, territory, player) for territory in game.state_dict.keys()}

    def get_winning_team(self, game):
        result = self.winning.get_value(game)
        if result >= 0.5:
            return 'Allies', (2 * result - 1)
        else:
            return 'Axis', (1 - 2 * result)


class Heuristics:
    def __init__(self, name, load_net=True):
        self.name = name
        self.net = None
        if load_net:
            self.load_neural_net()

    def load_neural_net(self):
        model_file = 'NNData/' + self.name + '_model.h5'
        self.net = keras.models.load_model(model_file)

    def get_heuristics(self, game, player='', territory_name=''):
        return list()

    def get_value(self, game, territory_name='', player=''):
        inputs = self.get_heuristics(game, territory_name, player)
        return self.net.predict(inputs)


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

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = list()
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

        # IPC value of territory
        heuristics.append(territory.ipc)

        # Defensive power in territory
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == game.rules.teams[player]:
                power += game.rules.get_unit(unit_state.type_index).defense
        heuristics.append(power)

        # Is capital
        heuristics.append(1 if territory.is_capital else 0)

        # Is water
        heuristics.append(1 if territory.is_water else 0)

        # TODO: Add more heuristics to the example above

        return heuristics


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

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = list()
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

        # IPC value of territory
        heuristics.append(territory.ipc)

        # Defensive power in territory
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == game.rules.teams[player]:
                power += game.rules.get_unit(unit_state.type_index).defense
        heuristics.append(power)

        # Is capital
        heuristics.append(1 if territory.is_capital else 0)

        # Is water
        heuristics.append(1 if territory.is_water else 0)

        # TODO: Add more heuristics to the examples above

        return heuristics


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

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = list()
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

        # IPC value of territory
        heuristics.append(territory.ipc)

        # Defensive power in territory
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == game.rules.teams[player]:
                power += game.rules.get_unit(unit_state.type_index).defense
        heuristics.append(power)

        # Is capital
        heuristics.append(1 if territory.is_capital else 0)

        # Is water
        heuristics.append(1 if territory.is_water else 0)

        # TODO: Add more heuristics to the examples above

        return heuristics


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

    def get_heuristics(self, game, player='', territory_name=''):
        heuristics = list()

        # Controls Suez
        heuristics.append(1 if game.controls_suez('Allies') else 0)

        # Capitals owned by Allies
        allies_caps = 0
        for player_obj in self.players:
            allies_caps += (game.rules.teams[game.state_dict[player_obj.capital].owner] == 'Allies')
        heuristics.append(allies_caps)

        # TODO: Add more heuristics to the examples above
        #  Note: This function shouldn't use player or territory_name, those are only there because it inherits the method

        return heuristics


# Example uses:
# brain = Brain()
# brain.get_importance_values(game, 'America')  # Returns dict of importance values between 0 and 1 for America
# brain.get_build_average(game)  # Returns dict of build averages for whichever player's turn it is
# brain.get_risk_tolerances(game, 'Russia')  # Returns dict of risk tolerances for each territory for when Russia is attacking
# brain.get_winning_team(game)  # Returns winner (either 'Axis' or 'Allies'), and how much they're winning by (0 = tied, 1 = almost guaranteed win)
