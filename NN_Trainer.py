import keras
import BigBrain
import os
import BoardState


class ExpectedValues:
    def __init__(self, game, winner, total_game_turns):
        self.winner = winner
        self.total_game_turns = total_game_turns

        self.is_winning_data = [(BigBrain.IsWinning().get_heuristics(game), [self.get_expected_winner(game)])]
        self.risk_tolerance_data, self.importance_value_data, self.build_average_data = list(), list(), list()

        for player in self.game.players.keys():
            for territory_name in self.game.state_dict:
                self.risk_tolerance_data.append((BigBrain.RiskTolerance().get_heuristics(game, player, territory_name),
                                                 self.get_expected_risk_tolerance(game, player, territory_name)))
                self.importance_value_data.append((BigBrain.ImportanceValue().get_heuristics(game, player, territory_name),
                                                   self.get_expected_importance_value(game, player, territory_name)))
                self.build_average_data.append((BigBrain.BuildAverage().get_heuristics(game, player, territory_name),
                                                self.get_expected_build_average(game, player, territory_name)))

    def get_expected_risk_tolerance(self, game, player, territory_name):
        # TODO: Find a way to get risk tolerance based on values we know
        #  This is what we train the Neural Network with
        #  Output should be normalized to be between 0 and 1
        return 0

    def get_expected_importance_value(self, game, player, territory_name):
        # TODO: Find a way to get importance value of a territory based on values we know
        #  This is what we train the Neural Network with
        #  Output should be normalized to be between 0 and 1
        return 0

    def get_expected_build_average(self, game, player, territory_name):
        # TODO: Find a way to get build average of a territory based on values we know
        #  This is what we train the Neural Network with
        #  Output should be positive integer?
        return 0

    def get_expected_winner(self, game):
        percent_of_game_done = game.turn_state.round_num / self.total_game_turns
        if self.winner == 'Allies':
            return 0.5 + 0.5 * percent_of_game_done
        else:
            return 0.5 - 0.5 * percent_of_game_done


class Trainer:
    def __init__(self, game_folders_and_winners):
        self.is_winning_data, self.risk_tolerance_data, self.importance_value_data, self.build_average_data = list(), list(), list(), list()
        self.load_expected_data(game_folders_and_winners)

    def load_expected_data(self, game_folders_and_winners):
        game = BoardState.Game()
        for game_folder, winner in game_folders_and_winners:
            xml_files = os.listdir(game_folder)
            game.export_reader(os.path.join(game_folder, max(xml_files, key=lambda x: int(str(x).split('.')[0]))))
            total_turns = game.turn_state.round_num
            for xml_file in xml_files:
                game.export_reader(os.path.join(game_folder, xml_file))
                data = ExpectedValues(game, winner, total_turns)
                self.is_winning_data += data.is_winning_data
                self.risk_tolerance_data += data.risk_tolerance_data
                self.importance_value_data += data.importance_value_data
                self.build_average_data += data.build_average_data

    def train_is_winning(self):
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_dim=len(self.is_winner_data[0][0]), activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(1, activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        X, y = [data[0] for data in self.is_winning_data], [data[1] for data in self.is_winning_data]
        model.fit(X, y, epochs=150, batch_size=10)
        _, accuracy = model.evaluate(X, y)
        print('IsWinner accuracy: %.2f' % (accuracy * 100))

        # Save the model for later
        model.save('NNData/is_winning_model.h5')

    def train_risk_tolerance(self):
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_dim=len(self.risk_tolerance_data[0][0]), activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(1, activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        X, y = [data[0] for data in self.risk_tolerance_data], [data[1] for data in self.risk_tolerance_data]
        model.fit(X, y, epochs=150, batch_size=10)
        _, accuracy = model.evaluate(X, y)
        print('RiskTolerance accuracy: %.2f' % (accuracy * 100))

        # Save the model for later
        model.save('NNData/risk_tolerance_model.h5')

    def train_importance_value(self):
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_dim=len(self.importance_value_data[0][0]), activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(1, activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        X, y = [data[0] for data in self.importance_value_data], [data[1] for data in self.importance_value_data]
        model.fit(X, y, epochs=150, batch_size=10)
        _, accuracy = model.evaluate(X, y)
        print('ImportanceValue accuracy: %.2f' % (accuracy * 100))

        # Save the model for later
        model.save('NNData/importance_value_model.h5')

    def train_build_average(self):
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_dim=len(self.build_average_data[0][0]), activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(1, activation='relu'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        X, y = [data[0] for data in self.build_average_data], [data[1] for data in self.build_average_data]
        model.fit(X, y, epochs=150, batch_size=10)
        _, accuracy = model.evaluate(X, y)
        print('BuildAverage accuracy: %.2f' % (accuracy * 100))

        # Save the model for later
        model.save('NNData/build_average_model.h5')

    def train_all(self):
        self.train_is_winning()
        self.train_risk_tolerance()
        self.train_importance_value()
        self.train_build_average()


# Example use:
# trainer = Trainer([('xmlfiles/Game5', 'Axis'),
#                    ('xmlfiles/Game20', 'Allies'),
#                    ('xmlfiles/Game27', 'Axis'),
#                    ('xmlfiles/Game45', 'Allies')])
# trainer.train_all()
