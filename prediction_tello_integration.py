import joblib
import numpy as np
from djitellopy import Tello
from mpu6050 import mpu6050
import time

# Load the trained SVM model
svm_model = joblib.load('svm_model.pkl')
print("SVM model loaded.")

# Initialize the MPU6050 sensor
imu_sensor = mpu6050(0x68)  # Adjust I2C address as needed

# Initialize Tello UAV
tello = Tello()
tello.connect()
print(f"Tello Battery: {tello.get_battery()}%")

# Gesture-to-command mapping (excluding takeoff, as it happens automatically)
command_map = {
    1: lambda: tello.move_up(50),      # Gesture 1: Move up
    2: lambda: tello.move_down(50),    # Gesture 2: Move down
    3: lambda: tello.move_left(50),    # Gesture 3: Move left
    4: lambda: tello.move_right(50),   # Gesture 4: Move right
    5: lambda: tello.move_forward(50), # Gesture 5: Move forward
    6: lambda: tello.move_back(50),    # Gesture 6: Move back
    7: lambda: tello.rotate_counter_clockwise(45), # Gesture 7: Rotate left
    8: lambda: tello.rotate_clockwise(45),         # Gesture 8: Rotate right
    9: tello.land                     # Gesture 9: Land
}

# Function to collect IMU data for 5 seconds
def collect_imu_data(duration=5, sampling_rate=0.1):
    imu_data = []
    start_time = time.time()

    while time.time() - start_time < duration:
        # Fetch IMU data
        accel_data = imu_sensor.get_accel_data()
        gyro_data = imu_sensor.get_gyro_data()

        # Append the IMU values as a single row
        imu_data.append([
            accel_data['x'], accel_data['y'], accel_data['z'],
            gyro_data['x'], gyro_data['y'], gyro_data['z']
        ])

        time.sleep(sampling_rate)  # Sampling interval

    # Flatten the data to match the SVM model input
    return np.array(imu_data).flatten()

# Main loop
try:
    print("Taking off...")
    tello.takeoff()  # Automatically take off at the start
    print("Perform a gesture for 5 seconds to control the UAV...")

    while True:
        # Collect 5 seconds of IMU data
        imu_data = collect_imu_data(duration=5)

        # Predict the gesture using the SVM model
        gesture = svm_model.predict([imu_data])[0]
        print(f"Predicted Gesture: {gesture}")

        # Execute the corresponding command
        if gesture in command_map:
            print(f"Executing command for gesture: {gesture}")
            command_map[gesture]()

            # If "land" gesture is detected, exit the loop
            if gesture == 9:
                print("UAV has landed. Exiting...")
                break

except KeyboardInterrupt:
    # Safely land the UAV when the script is interrupted
    print("Landing the UAV due to interruption...")
    tello.land()
