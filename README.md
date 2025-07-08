# Jumping Agent with Genetic Algorithm and Neural Network

A simulation where agents learn to jump across platforms using a Neural Network powered by a Genetic Algorithm. Over multiple generations, agents evolve their "brains" to improve their jumping skills and survive longer.

## 🧠 Overview

Each agent in the simulation is controlled by a simple feedforward neural network. Agents receive inputs (such as their position, velocity, and platform distance) and output actions (jump or not). A genetic algorithm is used to evolve the weights of the neural networks across generations.

The goal: **Jump as high as possible**

## 🔁 How It Works

1. **Initialization**: A population of agents is created with random neural network weights.
2. **Simulation**: Agents attempt to survive by jumping across platforms.
3. **Scoring**: Each agent is scored based on how high it gets.
4. **Selection**: Top-performing agents are selected as parents.
5. **Crossover & Mutation**: New agents are generated from parent genes with crossover and mutation to introduce variability.
6. **Repeat**: The new generation starts again, gradually evolving better jumpers.

## 🧬 Technologies & Concepts

- **Neural Networks**: Each agent is powered by a feedforward network (no backpropagation).
- **Genetic Algorithm**: Used to evolve the population:
  - Selection
  - Crossover
  - Mutation
- **Physics Simulation**: Basic 2D physics to model jumping and falling.

## 🛠️ Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Jumping-Agent-with-Genetic-Algorithm-and-Neural-Network.git
   cd Jumping-Agent-with-Genetic-Algorithm-and-Neural-Network
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the simulation
    ```bash
    python main.py
    ```