from time import sleep
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import UnusualActivity , UserRegister
from . import evaluate_dqn
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import time
import smtplib  # For sending email
from email.mime.text import MIMEText  # To format email text
from email.mime.multipart import MIMEMultipart  # To create email with subject and body
from . import ev
from .forms import UserRegisterForm
from django.shortcuts import render
from django.http import JsonResponse
import serial
import numpy as np
import json
import time
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from .models import SensorReading
from .landslide_env import LandslideEnv
from .dqn_agent import DQNAgent
import os
from .models import SensorReading

from django.shortcuts import render
from django.http import JsonResponse
import serial
import numpy as np
import json
import time
from datetime import datetime
from .models import SensorReading
import os
import threading

# Define serial port (update accordingly)
SERIAL_PORT = 'COM7'  # Change this based on your system
BAUD_RATE = 115200
TIMEOUT = 2

# Global variables for sensor data
current_sensor_data = {
    'temperature': 25.0,
    'humidity': 60.0,
    'pressure': 101325.0,  # Standard atmospheric pressure in Pa
    'altitude': 0.0,
    'accel_x': 0.0,
    'accel_y': 0.0,
    'accel_z': 9.8,
    'soil_moisture': 500,
    'rainfall': 0,
    'slope': 0.0,
    'aspect': 0.0,
    'risk_level': 0,
    'timestamp': datetime.now().timestamp()
}

# Flag to track if the background thread is running
sensor_thread_running = False

def index(request):
    """Render the main dashboard page."""
    return render(request, 'dashboard/index.html')

def get_latest_sensor_data(request):
    """API endpoint to get the latest sensor data."""
    global current_sensor_data
    
    # Get the latest 10 readings from database if available
    try:
        recent_readings = SensorReading.objects.order_by('-timestamp')[:10]
        
        # Format historical data for charts
        historical_data = {
            'timestamps': [],
            'temperature': [],
            'humidity': [],
            'pressure': [],
            'soil_moisture': [],
            'slope': []
        }
        
        for reading in reversed(list(recent_readings)):
            historical_data['timestamps'].append(reading.timestamp.strftime('%H:%M:%S'))
            historical_data['temperature'].append(reading.temperature)
            historical_data['humidity'].append(reading.humidity)
            historical_data['pressure'].append(reading.pressure)
            historical_data['soil_moisture'].append(reading.soil_moisture)
            historical_data['slope'].append(reading.slope)
    except:
        # If no database or model not set up, provide empty historical data
        historical_data = {
            'timestamps': [],
            'temperature': [],
            'humidity': [],
            'pressure': [],
            'soil_moisture': [],
            'slope': []
        }
    
    # Create response with current data
    response_data = {
        'current': current_sensor_data,
        'historical': historical_data
    }
    
    return JsonResponse(response_data)

def read_sensor_data():
    """Background function to read data from serial port."""
    global current_sensor_data, sensor_thread_running
    
    print("Starting sensor data reading thread...")
    
    # Try different encodings if needed
    encodings = ['utf-8', 'latin-1', 'ascii']
    current_encoding_index = 0
    
    while sensor_thread_running:
        ser = None
        try:
            # Open serial connection
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            print(f"Connected to serial port {SERIAL_PORT}")
            
            # Wait for serial connection to stabilize
            time.sleep(2)
            
            # Flush input buffer
            ser.reset_input_buffer()
            
            # Read a line from serial
            raw_bytes = ser.readline()
            print(f"Raw bytes: {repr(raw_bytes)}")
            
            # Try current encoding
            encoding = encodings[current_encoding_index]
            line = raw_bytes.decode(encoding).strip()
            print(f"Decoded with {encoding}: {line}")
            
            # Check if the line starts with a digit (likely data not header)
            if line and (line[0].isdigit() or line[0] == '-'):
                values = line.split(",")
                
                if len(values) >= 8:  # At least 8 values expected
                    # Convert values to appropriate types with additional error checking
                    try:
                        temperature = float(values[0])
                        humidity = float(values[1])
                        pressure = float(values[2])
                        altitude = float(values[3])
                        accel_x = float(values[4])
                        accel_y = float(values[5])
                        accel_z = float(values[6])
                        soil_moisture = int(values[7])
                        
                        # Calculate derived values
                        accel_x_normalized = max(min(accel_x/9.81, 1.0), -1.0)  # Clamp between -1 and 1
                        accel_y_normalized = max(min(accel_y/9.81, 1.0), -1.0)  # Clamp between -1 and 1

                        slope_x = np.arcsin(accel_x_normalized) * (180/np.pi)
                        slope_y = np.arcsin(accel_y_normalized) * (180/np.pi)
                        slope = np.sqrt(slope_x**2 + slope_y**2)

                        # Check if slope is valid before proceeding
                        if np.isnan(slope):
                            print(f"Warning: Invalid slope calculation. Using fallback value.")
                            slope = 0.0 
                        
                        aspect = np.arctan2(accel_y, accel_x) * (180/np.pi)
                        if aspect < 0:
                            aspect += 360
                        
                        # Update current_sensor_data
                        current_sensor_data = {
                            'temperature': temperature,
                            'humidity': humidity,
                            'pressure': pressure,
                            'altitude': altitude,
                            'accel_x': accel_x,
                            'accel_y': accel_y,
                            'accel_z': accel_z,
                            'soil_moisture': soil_moisture,
                            'slope': slope,
                            'aspect': aspect,
                            'rainfall': 0 if len(values) <= 8 else float(values[8]),
                            'risk_level': calculate_risk(temperature, humidity, soil_moisture, slope),
                            'timestamp': datetime.now().timestamp()
                        }
                        
                        print(f"Updated sensor data: Temperature={temperature}°C, Humidity={humidity}%, Slope={slope}°")
                        
                        # Save to database if model exists
                        try:
                            SensorReading.objects.create(
                                temperature=temperature,
                                humidity=humidity,
                                pressure=pressure,
                                altitude=altitude,
                                accel_x=accel_x,
                                accel_y=accel_y,
                                accel_z=accel_z,
                                soil_moisture=soil_moisture,
                                slope=slope,
                                aspect=aspect,
                                risk_level=current_sensor_data['risk_level']
                            )
                        except Exception as db_error:
                            print(f"Database error: {db_error}")
                    except (ValueError, IndexError) as parse_error:
                        print(f"Error parsing values: {parse_error}")
                else:
                    print(f"Not enough values in data: {values}")
            
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            # Try different port or wait longer before retry
            time.sleep(15)
            
        except UnicodeDecodeError:
            # Try a different encoding next time
            current_encoding_index = (current_encoding_index + 1) % len(encodings)
            print(f"Switching to encoding: {encodings[current_encoding_index]}")
            
        except Exception as e:
            print(f"General error: {e}")
            
            # Generate random data for testing if serial fails
            temperature = np.random.uniform(20, 30)
            humidity = np.random.uniform(40, 80)
            pressure = np.random.uniform(90000, 102000)
            altitude = np.random.uniform(100, 500)
            accel_x = np.random.uniform(-1, 1)
            accel_y = np.random.uniform(-1, 1)
            accel_z = np.random.uniform(8, 10)
            soil_moisture = np.random.randint(300, 700)
            slope = np.random.uniform(0, 20)
            
            # Update with random data for testing
            current_sensor_data = {
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'altitude': altitude,
                'accel_x': accel_x,
                'accel_y': accel_y,
                'accel_z': accel_z,
                'soil_moisture': soil_moisture,
                'slope': slope,
                'aspect': np.random.uniform(0, 360),
                'rainfall': 0,
                'risk_level': calculate_risk(temperature, humidity, soil_moisture, slope),
                'timestamp': datetime.now().timestamp()
            }
            
            print("Using random data for testing (serial connection failed)")
        
        finally:
            # Ensure serial port is closed regardless of success or failure
            if ser:
                ser.close()
        
        # Wait before next reading
        time.sleep(10)
def calculate_risk(temperature, humidity, soil_moisture, slope):
    """
    Simple risk calculation function as a fallback when DQN model isn't available.
    
    Returns:
        0: No risk
        1: Risk detected
    """
    # High risk conditions (simplified algorithm):
    # - High humidity (>80%) AND high soil moisture (>600) 
    # - OR steep slope (>30°)
    if (humidity > 80 and soil_moisture > 600) or slope > 30:
        return 1
    return 0

def start_sensor_thread():
    """Start the background thread for sensor readings."""
    global sensor_thread_running
    
    if not sensor_thread_running:
        sensor_thread_running = True
        thread = threading.Thread(target=read_sensor_data)
        thread.daemon = True
        thread.start()
        print("Background sensor thread started")

# Start the sensor thread when Django loads the views module
#start_sensor_thread()
# Create your views here.
def homepage(request):
    result = evaluate_dqn.mainFunction()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print("reseult",result, timestamp) 
       # return redirect('homepage')
    return render(request, 'index2.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("autenticated")
        
        if user is not None:
            login(request, user)
            print("Logged in")
            messages.success(request, "Login successful!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "signin.html")

def callEvaluate(request):
    result = evaluate_dqn.mainFunction()
    pred = ev.main()
    print(pred)
    return JsonResponse({"prediction": result})

def send_mail():

    sender_email = "minimol.project@gmail.com"  
    sender_password = "qkkf cwxy czce btps" 
    recipient_emails = ["em.shinojeattath5112@gmail.com","anzilta08@gmail.com","diyaelfadhilph@gmail.com"] 
    subject = "Test Email from Me"
    body = "Warning there is a possible landslide in your area."

    smtp_server = "smtp.gmail.com" 
    smtp_port = 587 

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(sender_email, sender_password)  

        # Step 6: Send email to all recipients
        for recipient in recipient_emails:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send the email
            server.sendmail(sender_email, recipient, msg.as_string())
            print(f"Email sent to {recipient}")


    except Exception as e:
        print(f"Error: {e}")

def news(request):
    return render(request, "news.html")

def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        
def report_activity(request):
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        description = request.POST.get('description')
        location = request.POST.get('location')

        UnusualActivity.objects.create(
            user=request.user,
            activity_type=activity_type,
            description=description,
            location=location
        )
        return redirect('home')
    return render(request, 'report_activity.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def prediction_analysis(request):
    return render(request, 'prediction_analysis.html')


def profile(request):
    return render(request, 'profile.html')
def register(request):
    return render(request, 'register.html') 



def register_view(request):
    if request.method == 'POST':
        Firstname=request.POST['Firstname']
        Lastname=request.POST['Lastname']
        Username = request.POST['Username']
        Email= request.POST['Email']
        if User.objects.filter(username=Username).exists():
        
            messages.error(request, "Username already taken!")
            return redirect('register')

        if User.objects.filter(email=Email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        user = User.objects.create_user(Username=Username, Email=Email, Firstname=Firstname,Lastname=Lastname)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')  # Make sure you have a login URL defined

    return render(request, 'register.html')
