# Pedestrian Evacuation Simulation

Implementation of a pedestrian evacuation model based on the Floor Field Model from Burstedde et al.

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- PyYAML

```bash
pip install -r requirements.txt
```

# Setup

## 1- Clone repository:
```bash
git clone https://github.com/yourusername/pedestrian-simulation.git
cd pedestrian-simulation
```

## 2 -Configure the number of pedestrians in utils.py:
simulation:
  num_pedestrians: 10

# Usage
## Run simulation:
```bash
main.py
```

# Model Components
## Floor Field
Base environment grid representation
Cell values:

- 0: Empty cell
- 1: Pedestrian
- 2: Exit
- 3: Wall

## Static Field

- Fixed field that guides pedestrians to exits
- Calculated using A* pathfinding
- Influences pedestrian movement decisions

## Dynamic Field

- Real-time field tracking pedestrian density
- Updates based on pedestrian movements
- Implements decay and diffusion mechanisms
- Helps avoid congestion

## Pedestrian Logic

- Movement based on field values
- Congestion avoidance
- Exit selection strategy
- Conflict resolution for multiple pedestrians

# Project Structure
```bash
pedestrian_simulation/
├── src/
│   ├── Cache/         # Core classes
│   │   └── cache.py
│   │ 
│   ├── fields/         # Field implementations
│   │   ├── floor_field.py
│   │   ├── static_field.py
│   │   └── dynamic_field.py
│   │ 
│   ├── Matrix/         # Preference Matrix class
│   │   ├── matrix_operations.py 
│   │   └── preference_matrix.py
│   │ 
│   ├── PathFinding/         # Pedestrian related classes
│   │   └── AStar.py
│   │ 
│   ├── Pedestrians/         # A* implementation
│   │   ├── pedestrian.py 
│   │   └── pedestrians_group.py
│   │ 
│   ├── animation.py # Create animation frames
│   │ 
│   ├── main.py # Run aplication
│   │ 
│   └── utils.py # Core values to animation
```

# Implementation Details
## Configuration
utils.py
# simulation:
```bash
  width: 50
  height: 50
  num_pedestrians: 100
```
  
# exits:
```bash
  - [30, 0]    # Left wall
  - [49, 25]   # Top exit 
  - [30, 49]   # Right wall
```
# movement:
 ## preference_matrix:
```bash
    - [0.055, 0.850, 0.055]
    - [0.010, 0.000, 0.010]
    - [0.007, 0.006, 0.007]
```
