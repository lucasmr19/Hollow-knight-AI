# Hollow-knight-AI

This project focuses on training an AI to play **Hollow Knight** using **Reinforcement Learning (RL)** and **real-time object detection** powered by YOLO/ROBOFLOW. The pipeline involves collecting in-game images, labeling them, training an object detection model, and integrating it into an environment for RL training.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Data Collection and Labeling](#data-collection-and-labeling)  
3. [Object Detection Model Training](#object-detection-model-training)  
4. [Reinforcement Learning Environment](#reinforcement-learning-environment)  
5. [Running the Project](#running-the-project)  
6. [Future Work](#future-work)  

---

## Project Overview

The goal of this project is to train an AI agent that can play **Hollow Knight**, a popular Metroidvania game. To achieve this:
1. A **YOLO-based object detection model** is trained to identify key elements from the game, such as health bars, mana, enemies, and interactable objects.
2. These detections are used as observations for a **Reinforcement Learning (RL) agent** that interacts with the game environment to learn optimal strategies.

This project involves:
- Collecting and labeling game frames to create a custom object detection dataset.
- Training a YOLO model for real-time detection.
- Implementing an OpenAI Gym-like environment to interface with the game.
- Training an AI agent using RL algorithms.

---

## Data Collection and Labeling

To train the YOLO object detection model, we first need a labeled dataset of Hollow Knight gameplay frames.

### Step 1: Collecting Game Images
- Game footage was recorded using screen capture tools like OBS Studio.  
- Frames were extracted from gameplay videos at regular intervals.  
- A variety of situations were captured, including combat, exploration, and interaction with NPCs, to ensure model robustness.

### Step 2: Labeling the Dataset
- **LabelImg** or similar tools were used to annotate the frames.  
- Objects of interest include:
  - **Health bar**: Indicates the player's remaining health.
  - **Mana**: Shows the player's available energy for abilities.
  - **Enemies**: Various types of enemies encountered in the game.
  - **Interactable Objects**: Switches, platforms, or other important elements.  

### Step 3: Preparing the Dataset
- The labeled data was split into training (80%) and validation (20%) subsets.  
- Images were resized to 640x640 pixels for compatibility with YOLO's architecture.

---

## Object Detection Model Training

A custom YOLO model was trained to detect the labeled objects in real-time.  

### Step 1: Setting Up the YOLO Model
- The **YOLOv5/YOLOv8** framework was used for training due to its speed and accuracy.  
- Training was performed on a GPU-enabled machine for faster convergence.  

### Step 2: Training
- The dataset was fed into the YOLO training pipeline with the following configurations:
  - Input image size: 640x640
  - Batch size: 16
  - Epochs: 100+
  - Learning rate: Adjusted dynamically.  
- The model achieved high accuracy in detecting all defined classes.

### Step 3: Validation and Testing
- Validation metrics included mAP (mean Average Precision) and F1-Score.  
- Real-time testing was conducted to ensure the model could perform at 30+ FPS.

---

## Reinforcement Learning Environment

To train an AI to play the game, an **OpenAI Gym-like environment** was implemented to simulate the game mechanics and integrate the object detection model.

### Environment Features
- **Observation Space**:  
  The environment captures game frames and uses the YOLO model to detect game elements. The observations include:
  - Player health and mana levels.
  - Positions of enemies and interactable objects.
  - Relative distances and actions taken.
  
- **Action Space**:  
  A multi-binary action space that represents possible keyboard inputs:
  - Movement: `W`, `A`, `S`, `D`
  - Abilities: `Space`, `J`, `K`, etc.

- **Rewards System**:  
  The agent is rewarded or penalized based on game outcomes:
  - Gaining health/mana: Positive reward.
  - Taking damage or dying: Negative reward.
  - Defeating enemies or completing objectives: Positive reward.

### Reinforcement Learning Algorithm
- Algorithms like **Proximal Policy Optimization (PPO)** or **Deep Q-Learning (DQN)** were used for training.  
- The agent interacts with the environment, observes rewards, and learns policies to maximize performance.

---

## Running the Project

Follow these steps to set up and run the project:

### Prerequisites
- Python 3.8+
- Required libraries:  
  ```bash
  pip install torch gym numpy opencv-python pyautogui yolov5
  ```
- A GPU-enabled machine for model training and RL experiments.

### Steps
1. **Train the YOLO Model**:  
   Use the labeled dataset to train the YOLO model or load the pre-trained weights provided in `best.pt`.  
   ```bash
   python train.py --data data.yaml --weights yolov5s.pt --epochs 100
   ```
2. **Run the Environment**:  
   Launch the game and initialize the environment:
   ```bash
   python hollow_knight_env.py
   ```
3. **Train the RL Agent**:  
   Train the agent using your preferred RL algorithm:
   ```bash
   python train_agent.py
   ```

---

## Future Work

- **Fine-Tuning the Object Detection Model**: Improve detection accuracy for more complex scenarios in the game.  
- **Enhancing the Reward System**: Make rewards more granular to encourage better strategies.  
- **Multitask Learning**: Train the AI to complete specific objectives or explore the map efficiently.  
- **Integration with Advanced RL Algorithms**: Experiment with more complex RL methods like SAC (Soft Actor-Critic) or A3C.  
