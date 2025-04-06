import serial
import numpy as np
import os
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from .landslide_env import LandslideEnv
from .dqn_agent import DQNAgent

# Define serial port (update accordingly)
SERIAL_PORT = 'COM7'
BAUD_RATE = 115200
TIMEOUT = 2

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dqn_landslide_model.keras")
DATA_PATH = os.path.join(BASE_DIR, "landslide_data.csv")

# Default values for features not provided by sensors
DEFAULT_VALUES = {
    'id': 1,
    'wind_speed': 0,
    'soil_type': 1,
    'soil_density': 1.6,
    'rock_type': 1,
    'fault_lines': 0,
    'land_cover': 3,
    'vegetation_index': 0.5,
    'previous_landslide': 0,
    'landslide_frequency': 0,
    'groundwater_level': 10,
    'runoff': 0,
    'construction': 0,
    'deforestation': 0
}

# Load the trained model
def load_trained_model(model_path, state_size, action_size):
    print(f"Loading model from {model_path}")
    agent = DQNAgent(state_size, action_size)
    agent.model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")
    return agent

# Map sensor data to complete feature set
def map_sensor_to_features(sensor_data, state_size):
    """
    Map the 9 sensor values to the complete feature set required by the model.
    
    Args:
        sensor_data: Array of sensor readings [temperature, humidity, pressure, altitude, accelX, accelY, accelZ, soil_moisture, rainfall]
        state_size: The size of the state expected by the model
    
    Returns:
        complete_state: A numpy array with all features needed by the model
    """
    # Initialize complete state with zeros
    complete_state = np.zeros(state_size)
    
    # Map sensor data to corresponding features
    # ID
    complete_state[0] = DEFAULT_VALUES['id']
    
    # Rainfall - now directly from rain sensor
    complete_state[1] = sensor_data[8]  # Using the new 9th value
    
    # Temperature - directly from sensor
    complete_state[2] = sensor_data[0]
    
    # Humidity - directly from sensor
    complete_state[3] = sensor_data[1]
    
    # Wind Speed - default value
    complete_state[4] = DEFAULT_VALUES['wind_speed']
    
    # Soil Moisture - directly from sensor
    complete_state[5] = sensor_data[7]
    
    # Soil Type (encoded) - default value
    complete_state[6] = DEFAULT_VALUES['soil_type']
    
    # Soil Density - default value
    complete_state[7] = DEFAULT_VALUES['soil_density']
    
    # Slope Angle - derived from accelerometer data
    slope_x = np.arcsin(sensor_data[4]/9.81) * (180/np.pi)
    slope_y = np.arcsin(sensor_data[5]/9.81) * (180/np.pi)
    slope = np.sqrt(slope_x**2 + slope_y**2)
    complete_state[8] = slope
    
    # Elevation - directly from sensor altitude
    complete_state[9] = sensor_data[3]
    
    # Aspect - derived from accelerometer
    aspect = np.arctan2(sensor_data[5], sensor_data[4]) * (180/np.pi)
    if aspect < 0:
        aspect += 360
    complete_state[10] = aspect
    
    # Rock Type (encoded) - default value
    complete_state[11] = DEFAULT_VALUES['rock_type']
    
    # Fault Lines - default value
    complete_state[12] = DEFAULT_VALUES['fault_lines']
    
    # Land Cover Type (encoded) - default value 
    complete_state[13] = DEFAULT_VALUES['land_cover']
    
    # Vegetation Index - default value
    complete_state[14] = DEFAULT_VALUES['vegetation_index']
    
    # Previous Landslide - default value
    complete_state[15] = DEFAULT_VALUES['previous_landslide']
    
    # Frequency of Landslides - default value
    complete_state[16] = DEFAULT_VALUES['landslide_frequency']
    
    # Groundwater Levels - default value
    complete_state[17] = DEFAULT_VALUES['groundwater_level']
    
    # Runoff - default value or could be derived from rainfall
    complete_state[18] = DEFAULT_VALUES['runoff']
    
    # Construction Activity - default value
    complete_state[19] = DEFAULT_VALUES['construction']
    
    # Deforestation - default value
    complete_state[20] = DEFAULT_VALUES['deforestation']
    
    return complete_state

# Predict landslide function
def predict_landslide(agent, sensor_data, state_size, scaler):
    """
    Predict landslide risk based on sensor data.
    
    Args:
        agent: The DQN agent with loaded model
        sensor_data: Array of sensor readings
        state_size: The size of the state expected by the model
        scaler: MinMaxScaler for normalizing features
    
    Returns:
        action: The predicted action (0: stable, 1: landslide risk)
    """
    # Map sensor data to complete feature set
    complete_state = map_sensor_to_features(sensor_data, state_size)
    
    # Normalize the complete state
    normalized_state = np.zeros_like(complete_state)
    for i in range(len(complete_state)):
        # Reshape for sklearn compatibility
        feature = np.array([[complete_state[i]]])
        normalized_state[i] = scaler.fit_transform(feature)[0][0]
    
    # Reshape for model input
    state = np.reshape(normalized_state, [1, state_size])
    
    # Get action from agent
    action = agent.act(state)
    return action

def main():
    print("Starting Landslide Prediction System...")
    
    # Try to establish serial connection
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"✅ Serial connection established on {SERIAL_PORT}.")
    except serial.SerialException as e:
        print(f"❌ Error opening serial port: {e}")
        return
    
    # Initialize environment & agent
    try:
        env = LandslideEnv(data_path=DATA_PATH)
        state_size = env.state_size
        action_size = env.action_size
        print(f"Environment initialized with state_size={state_size}, action_size={action_size}")
        
        agent = load_trained_model(MODEL_PATH, state_size, action_size)
        
        # Initialize scaler
        scaler = MinMaxScaler(feature_range=(0, 1))
        
        print("✅ System initialized! Waiting for sensor data...\n")
    except Exception as e:
        print(f"❌ Error initializing environment or agent: {e}")
        ser.close()
        return
    
    # Main loop to receive and process sensor data
    try:
        while True:
            try:
                line = ser.readline().decode('latin-1').strip()
                if line:
                    print(f"🔍 Raw Data Received: {line}")
                    values = line.split(",")
                    
                    if len(values) == 9:  # Updated to check for 9 values
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
                                int(values[7]),    # Soil Moisture
                                float(values[8])   # Rainfall - new sensor
                            ])
                            
                            # Log the sensor data
                            print(f"📊 Processed Sensor Data:")
                            print(f"   Temperature: {sensor_data[0]}°C")
                            print(f"   Humidity: {sensor_data[1]}%")
                            print(f"   Pressure: {sensor_data[2]} Pa")
                            print(f"   Altitude: {sensor_data[3]} m")
                            print(f"   Acceleration: X={sensor_data[4]}, Y={sensor_data[5]}, Z={sensor_data[6]} m/s²")
                            print(f"   Soil Moisture: {sensor_data[7]}")
                            print(f"   Rainfall: {sensor_data[8]} mm")
                            
                            # Predict landslide risk
                            action = predict_landslide(agent, sensor_data, state_size, scaler)
                            
                            # Display prediction
                            if action == 1:
                                print("🚨 WARNING! Possible Landslide Risk Detected!")
                                # Here you could add code to trigger alerts, etc.
                            else:
                                print("✅ Terrain is Stable - No Landslide Risk")
                                
                            print("-" * 50)
                            
                        except ValueError as ve:
                            print(f"⚠️ Data conversion error: {ve}")
                    else:
                        print(f"⚠️ Unexpected data format: {values}")
                        
            except UnicodeDecodeError as ude:
                print(f"⚠️ Decoding error: {ude}")
                
    except KeyboardInterrupt:
        print("\n❌ Script stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        ser.close()
        print("✅ Serial connection closed.")

if __name__ == "__main__":
    main()