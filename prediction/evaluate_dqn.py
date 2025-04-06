import numpy as np
from .landslide_env import LandslideEnv
from .dqn_agent import DQNAgent
import tensorflow as tf
import os
import time
from . import views

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "landslide_data.csv")

def load_trained_model(model_path, state_size, action_size):
    agent = DQNAgent(state_size, action_size)
    agent.model = tf.keras.models.load_model(model_path)
    return agent


def predict_landslide(agent, state, state_size):
    state = np.reshape(state, [1, state_size])
    action = agent.act(state)
    return action

def mainFunction():
    model_path = os.path.join(BASE_DIR, "dqn_landslide_model.keras")   
    env = LandslideEnv(data_path=DATA_PATH)
    state_size = env.state_size
    action_size = env.action_size
    agent = load_trained_model(model_path, state_size, action_size)

    # Test prediction
    new_state = np.random.rand(state_size) 
    action = predict_landslide(agent, new_state, state_size)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    if action == 1:
        print("Landslide predicted.", timestamp)
        #views.send_mail()
        # views.send_mail()
    else:
        print(f"No landslide predicted. {timestamp}")
    return "Warning! Possible Landslide" if action == 1 else "Terrain is Stable..!"

if __name__ == "__main__":
    mainFunction()