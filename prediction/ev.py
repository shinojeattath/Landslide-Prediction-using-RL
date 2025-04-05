import serial
import numpy as np
import os
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from landslide_env import LandslideEnv
from dqn_agent import DQNAgent

# Define serial port (update accordingly)
try:
    ser = serial.Serial('COM7', 115200, timeout=2)
    print("✅ Serial connection established.")
except serial.SerialException as e:
    print(f"❌ Error opening serial port: {e}")
    exit()

print("✅ Python script is running! Waiting for data...\n")

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dqn_landslide_model.keras")
DATA_PATH = os.path.join(BASE_DIR, "landslide_data.csv")

# Load the trained model
def load_trained_model(model_path, state_size, action_size):
    agent = DQNAgent(state_size, action_size)
    agent.model = tf.keras.models.load_model(model_path)
    return agent

# Predict landslide function
def predict_landslide(agent, state, state_size):
    state = np.reshape(state, [1, state_size])
    action = agent.act(state)
    return action

# Initialize environment & agent
env = LandslideEnv(data_path=DATA_PATH)
state_size = env.state_size
action_size = env.action_size
agent = load_trained_model(MODEL_PATH, state_size, action_size)

# Initialize MinMax Scaler
scaler = MinMaxScaler(feature_range=(0, 1))

try:
    while True:
        try:
            line = ser.readline().decode('latin-1').strip()
            if line:
                print(f"🔍 Raw Data Received: {line}")  # Debugging
                values = line.split(",")

                if len(values) == 8:
                    try:
                        # Convert values to floats/integers
                        sensor_data = np.array([
                            float(values[0]),  # Temperature
                            float(values[1]),  # Humidity
                            float(values[2]),  # Pressure
                            float(values[3]),  # Altitude
                            float(values[4]),  # AccelX
                            float(values[5]),  # AccelY
                            float(values[6]),  # AccelZ
                            int(values[7])      # Soil Moisture
                        ])

                        # Normalize data (ensure the scaler is fitted beforehand)
                        normalized_data = scaler.fit_transform(sensor_data.reshape(-1, 1)).flatten()

                        # Predict landslide
                        action = predict_landslide(agent, normalized_data, state_size)

                        if action == 1:
                            print("🚨 Warning! Possible Landslide")
                        else:
                            print("✅ Terrain is Stable")

                    except ValueError as ve:
                        print(f"⚠️ Data conversion error: {ve}")
                else:
                    print(f"⚠️ Unexpected data format: {values}")

        except UnicodeDecodeError as ude:
            print(f"⚠️ Decoding error: {ude}")

except KeyboardInterrupt:
    print("\n❌ Stopping script.")
    ser.close()
    print("✅ Serial connection closed.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    ser.close()
