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

    def get_generic_heuristics(self, game, player='', territory_name=''):
        generic_heuristics = list()

        generic_heuristics.append(game.turn_state.round_num)   # turn number
        generic_heuristics.append(1 if is_winning else 0) # TODO. Brett. Somehow use is_winning here
        generic_heuristics.append(1 if territory_name.is_capital else 0)         # is capital
        generic_heuristics.append(1 if territory_name.is_water else 0)           # is water
        power = 0
        for unit_state in territory_state.unit_state_list:
            if game.rules.teams[unit_state.owner] == game.rules.teams[player]:
                power += game.rules.get_unit(unit_state.type_index).defense
        generic_heuristics.append(power)                                    # defensive power in territory
        generic_heuristics.append(territory.ipc)                            # IPC value of territory
        generic_heuristics.append()  # TODO. Brett. Distace from your capital
        generic_heuristics.append()  # TODO. Brett. Distace from nearest enemny capital
        generic_heuristics.append()  # TODO. Brett. Distance to nearest enemny factory
        generic_heuristics.append()  # TODO. Brett. Is_vulerable yes or no
        generic_heuristics.append()  # TODO. Brett. Power in range of territory
        generic_heuristics.append(1 if territory_name in game.rules.win_cons else 0)
        generic_heuristics.append()  # TODO. Brett. Distance to nearest enemy land terrtiory
        generic_heuristics.append()  # TODO. Brett. Distance to nearest enemny transport
        generic_heuristics.append()  # TODO. Brett. Distance to nearest enemny warship

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
        self.Heuristics = Heuristics # TODO: Brett. is this okay?

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = get_generic_heuristics(game, player, territory_name)
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

        heuristics.append()  # TODO. Brett. Defensibility value of attacking territory

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
        self.Heuristics = Heuristics  # TODO: Brett. is this okay?

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = get_generic_heuristics(game, player, territory_name)
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

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
        self.Heuristics = Heuristics  # TODO: Brett. is this okay?

    def get_heuristics(self, game, player='', territory_name=''):
        if not territory_name or not player:
            print('Must input both territory_name and player')
        heuristics = get_generic_heuristics(game, player, territory_name)
        territory = game.rules.board[territory_name]
        territory_state = game.state_dict[territory_name]

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

        # Total unit values
        axis_unit_value = 0
        axis_land_value = 0
        axis_sea_value = 0
        axis_air_value = 0
        allies_unit_value = 0
        allies_land_value = 0
        allies_sea_value = 0
        allies_air_value = 0

        #Some other things
        allies_total_ipc = 0
        allies_control_suez = 0
        allies_control_panama = 0
        allies_controlled_capitals = 0
        allies_controlled_factories = 0
        axis_total_ipc = 0
        axis_control_suez = 0
        axis_control_panama = 0
        axis_controlled_capitals = 0
        axis_controlled_factories = 0
        for territory_key in game.state_dict:
            for unit_state in game.state_dict[territory_key]:
                if game.rules.get_unit(unit_state.type_index).unit_type == 'sea':
                    if game.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_sea_value += game.rules.get_unit(unit_state.type_index).cost
                    elif game.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_sea_value += game.rules.get_unit(unit_state.type_index).cost
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'land':
                    if game.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            axis_controlled_factories += 0
                    elif game.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_land_value += game.rules.get_unit(unit_state.type_index).cost
                        if unit_state.type_index == 4:
                            allies_controlled_factories += 0
                elif game.rules.get_unit(unit_state.type_index).unit_type == 'air':
                    if game.teams[unit_state.owner] == "Axis":
                        axis_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        axis_air_value += game.rules.get_unit(unit_state.type_index).cost
                    elif game.teams[unit_state.owner] == "Allies":
                        allies_unit_value += game.rules.get_unit(unit_state.type_index).cost
                        allies_air_value += game.rules.get_unit(unit_state.type_index).cost

            if game.rules.teams[game.state_dict[territory_key].owner] == "Allies":
                allies_total_ipc += game.rules.board[territory_key].ipc
                if territory_key == "Egypt" \
                and game.rules.teams[game.state_dict["Trans-Jordan"].owner] == "Allies":
                    allies_control_suez = 1
                if territory_key == "Central America":
                    allies_control_panama = 1
                if game.rules.board[territory_key].is_capital:
                    allies_controlled_capitals = 0
            elif game.rules.teams[game.state_dict[territory_key].owner] == "Axis":
                axis_total_ipc += game.rules.board[territory_key].ipc
                if territory_key == "Egypt" \
                and game.rules.teams[game.state_dict["Trans-Jordan"].owner] == "Axis":
                    axis_control_suez = 1
                if territory_key == "Central America":
                    axis_control_panama = 1
                if game.rules.board[territory_key].is_capital:
                    axis_controlled_capitals = 0

        # TODO: Brett. we can use the total unit value ratio combined with controlled ipc at the beginning
        # to determine the baseline for who is winning. Obv they should be 'equal' to start
        heuristics.append(axis_unit_value/allies_unit_value) #TODO. Brett. this is clearly redudant but might be good? keep?
        heuristics.append(axis_unit_value)
        heuristics.append(axis_land_value)
        heuristics.append(axis_sea_value)
        heuristics.append(axis_air_value)
        heuristics.append(allies_unit_value)
        heuristics.append(allies_land_value)
        heuristics.append(allies_sea_value)
        heuristics.append(allies_air_value)

        heuristics.append(allies_total_ipc)
        heuristics.append(allies_control_suez)
        heuristics.append(allies_control_panama)
        heuristics.append(allies_controlled_capitals)
        heuristics.append(allies_controlled_factories)
        heuristics.append(axis_total_ipc)
        heuristics.append(axis_control_suez)
        heuristics.append(axis_control_panama)
        heuristics.append(axis_controlled_capitals)
        heuristics.append(axis_controlled_factories)

        # for all these consider if needs to deliniate axis and allies as different values
        heuristics.append() # TODO: BRett. percent of unit value in range fo front line
        heuristics.append()  # TODO: BRett. number of important territoryes you contorl/ have power over
        heuristics.append()  # TODO: BRett. number of factories in danger
        heuristics.append()  # TODO: BRett. luck value? see above comment in triple quotes

        # TODO: Add more heuristics to the examples above
        #  Note: This function shouldn't use player or territory_name, those are only there because it inherits the method

        return heuristics


# Example uses:
# brain = Brain()
# brain.get_importance_values(game, 'America')  # Returns dict of importance values between 0 and 1 for America
# brain.get_build_average(game)  # Returns dict of build averages for whichever player's turn it is
# brain.get_risk_tolerances(game, 'Russia')  # Returns dict of risk tolerances for each territory for when Russia is attacking
# brain.get_winning_team(game)  # Returns winner (either 'Axis' or 'Allies'), and how much they're winning by (0 = tied, 1 = almost guaranteed win)
