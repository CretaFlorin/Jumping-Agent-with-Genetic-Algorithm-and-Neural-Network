import math
import random


class NeuralNetwork:
    def __init__(self, input_size=8, hidden_size=12, output_size=3):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.w_input_hidden = [
            [random.uniform(-1, 1) for _ in range(self.input_size)] for _ in range(self.hidden_size)
        ]
        self.b_hidden = [
            random.uniform(-1, 1) for _ in range(self.hidden_size)
        ]
        
        self.w_hidden_output = [
            [random.uniform(-1, 1) for _ in range(self.hidden_size)] for _ in range(self.output_size)
        ]
        self.b_output = [
            random.uniform(-1, 1) for _ in range(self.output_size)
        ]
        
    def sigmoid(self, x):
        if x > 100: 
            return 1
        if x < -100:
            return 0
        
        return 1 / (1 + math.exp(-1 * x))
    
    def forward(self, input_layer):
        hidden = []
        # forward to hidden layer
        for i in range(self.hidden_size):
            total = sum(w * a for w, a in zip(self.w_input_hidden[i], input_layer)) + self.b_hidden[i]
            hidden.append(self.sigmoid(total))
            
        output = []
        # forward to output layer
        for i in range(self.output_size):
            result = sum(w * a for w, a in zip(self.w_hidden_output[i], hidden)) + self.b_output[i]
            output.append(self.sigmoid(result))
            
        return output
            
        