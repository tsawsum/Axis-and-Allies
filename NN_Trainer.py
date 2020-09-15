import keras
import os
import numpy as np


class Trainer:
    def __init__(self, data_folder):
        data_files = [os.path.join(data_folder, file_name) for file_name in ('importance_values.txt', 'should_attack.txt', 'build_averages.txt', 'is_winning.txt', 'prioritization.txt')]
        self.train_is_winning(self.get_data(data_files[3]))
        self.train_importance_value(self.get_data(data_files[0]))
        self.train_build_average(self.get_data(data_files[2]))
        self.train_prioritization(self.get_data(data_files[4]))
        self.train_should_attack(self.get_data(data_files[1]))

    def get_data(self, filename):
        inputs, outputs = list(), list()
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(';')
                if len(parts) >= 2:
                    inputs.append([float(k) for k in parts[0].split(',')])
                    outputs.append([float(k) for k in parts[1].split(',')])
        return np.array(inputs), np.array(outputs)

    def train_is_winning(self, data):
        X, Y = data
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_shape=X[0].shape, activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(Y.shape[1], activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        model.fit(X, Y, epochs=150, batch_size=32, validation_split=0.1)
        temp_thing, accuracy = model.evaluate(X, Y)
        print('IsWinner accuracy: %.2f%%' % (accuracy * 100))

        # Save the model for later
        if input('Save this model (y/n)? ') == 'y':
            model.save('NNData/is_winning_model.h5')

    def train_should_attack(self, data):
        X, Y = data
        # Create NN model that outputs whether or not to attack
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_shape=X[0].shape, activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(Y.shape[1], activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        model.fit(X, Y, epochs=150, batch_size=10, validation_split=0.1)
        _, accuracy = model.evaluate(X, Y)
        print('RiskTolerance accuracy: %.2f%%' % (accuracy * 100))

        # Save the model for later
        if input('Save this model (y/n)? ') == 'y':
            model.save('NNData/should_attack_model.h5')

    def train_importance_value(self, data):
        X, Y = data
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_shape=X[0].shape, activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(Y.shape[1], activation='sigmoid'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        model.fit(X, Y, epochs=150, batch_size=10, validation_split=0.1)
        _, accuracy = model.evaluate(X, Y)
        print('ImportanceValue accuracy: %.2f%%' % (accuracy * 100))

        # Save the model for later
        if input('Save this model (y/n)? ') == 'y':
            model.save('NNData/importance_value_model.h5')

    def train_build_average(self, data):
        X, Y = data
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_shape=X[0].shape, activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(Y.shape[1], activation='relu'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        model.fit(X, Y, epochs=250, batch_size=10, validation_split=0.1)
        _, accuracy = model.evaluate(X, Y)
        print('BuildAverage accuracy: %.2f%%' % (accuracy * 100))

        # Save the model for later
        if input('Save this model (y/n)? ') == 'y':
            model.save('NNData/build_average_model.h5')

    def train_prioritization(self, data):
        X, Y = data
        # Create NN model
        # TODO: Later: Experiment with this once everything is working
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(12, input_shape=X[0].shape, activation='relu'))
        model.add(keras.layers.Dense(8, activation='relu'))
        model.add(keras.layers.Dense(Y.shape[1], activation='relu'))
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # Train and test the model
        model.fit(X, Y, epochs=750, batch_size=10, validation_split=0.1)
        _, accuracy = model.evaluate(X, Y)
        print('Prioritization accuracy: %.2f%%' % (accuracy * 100))

        # Save the model for later
        if input('Save this model (y/n)? ') == 'y':
            model.save('NNData/prioritization_model.h5')


if __name__ == '__main__':
    Trainer('NNData')
