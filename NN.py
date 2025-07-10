import math
import random
import numpy as np

from constants import MAX_VISION_DISTANCE


import math
import random
import numpy as np

from constants import MAX_VISION_DISTANCE


class NeuralNetwork:
    def __init__(self, input_size=9, hidden_size1=24, hidden_size2=12, output_size=3):
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size

        # Weights and biases between input and first hidden layer
        self.w_input_hidden1 = np.random.uniform(
            -1, 1, (self.hidden_size1, self.input_size)
        )
        self.b_hidden1 = np.random.uniform(-1, 1, (self.hidden_size1,))

        # Weights and biases between first hidden and second hidden layer
        self.w_hidden1_hidden2 = np.random.uniform(
            -1, 1, (self.hidden_size2, self.hidden_size1)
        )
        self.b_hidden2 = np.random.uniform(-1, 1, (self.hidden_size2,))

        # Weights and biases between second hidden and output layer
        self.w_hidden2_output = np.random.uniform(
            -1, 1, (self.output_size, self.hidden_size2)
        )
        self.b_output = np.random.uniform(-1, 1, (self.output_size,))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -100, 100)))

    def forward(self, input_layer):
        input_layer = np.array(input_layer).flatten()
        normalized_input = input_layer / MAX_VISION_DISTANCE

        # Input to first hidden layer
        hidden1 = self.sigmoid(
            np.dot(self.w_input_hidden1, normalized_input) + self.b_hidden1
        )

        # First hidden to second hidden layer
        hidden2 = self.sigmoid(
            np.dot(self.w_hidden1_hidden2, hidden1) + self.b_hidden2
        )

        # Second hidden to output layer
        output = self.sigmoid(np.dot(self.w_hidden2_output, hidden2) + self.b_output)

        return output.tolist()
