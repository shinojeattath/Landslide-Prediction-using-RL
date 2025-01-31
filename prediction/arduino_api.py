import serial
import time

# Configure the serial port
ser = serial.Serial('COM7', 9600)  # Replace 'COM3' with the correct port for your Arduino
time.sleep(2)  # Wait for the serial connection to initialize

try:
    while True:
        if ser.in_waiting > 0:  # Check if there is data available to read
            line = ser.readline().strip()  # Read the line and decode it
            #  value = int(line)  # Convert the string to an integer
            print(f"Received value: {line}")  # Print the received value
except KeyboardInterrupt:
    print("Program terminated")

ser.close()  # Close the serial connectionpython 