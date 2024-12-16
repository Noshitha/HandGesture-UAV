import joblib
import numpy as np
import serial
import time
from djitellopy import Tello

# Serial port and baud rate for ESP32
SERIAL_PORT = '/dev/tty.usbserial-2130'  # Update based on your system
BAUD_RATE = 115200
DURATION = 5  # Duration to record gesture data (seconds)

# Load the SVM model
SVM_MODEL_PATH = 'svm_model.pkl'
svm_model = joblib.load(SVM_MODEL_PATH)
print("SVM model loaded.")

# Gesture-to-command mapping
gesture_command_map = {
    0: lambda drone: drone.move_up(50),  # Gesture 0: Move up
    1: lambda drone: drone.move_down(50),  # Gesture 1: Move down
    2: lambda drone: drone.move_right(50),  # Gesture 2: Move right
    3: lambda drone: drone.move_left(50),  # Gesture 3: Move left
    4: lambda drone: drone.move_forward(50),  # Gesture 4: Move forward
    5: lambda drone: drone.move_back(50),  # Gesture 5: Move back
    6: lambda drone: drone.rotate_counter_clockwise(50),  # Gesture 6: Rotate left
    7: lambda drone: drone.rotate_clockwise(50),  # Gesture 7: Rotate right
    8: lambda drone: drone.land()  # Gesture 8: Land
}

labels_map = {
    0: "UP", 1: "DOWN", 2: "RIGHT", 3: "LEFT", 
    4: "FRONT", 5: "BACK", 6: "ROTATE LEFT", 
    7: "ROTATE RIGHT", 8: "LAND"
}

def expand_by_interpolation(imu_data, target_rows=500):
    current_rows = len(imu_data)
    factor = target_rows / current_rows
    
    # Interpolating rows
    interpolated_indices = np.linspace(0, current_rows - 1, target_rows)
    expanded_data = np.array([np.interp(interpolated_indices, range(current_rows), imu_data[:, col]) 
                              for col in range(imu_data.shape[1])]).T
    return expanded_data

def init_serial_connection(port, baud_rate):
    """
    Initialize the serial connection to ESP32.
    """
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Serial connection established on {port} at {baud_rate} baud.")
        return ser
    except Exception as e:
        print(f"Error initializing serial connection: {e}")
        return None

def clear_serial_buffer(ser):
    """
    Clear any residual data in the serial buffer.
    """
    while ser.in_waiting > 0:
        ser.readline()

def record_imu_data(ser, duration):
    """
    Record IMU data from ESP32 for the specified duration.
    """
    imu_data = []
    start_time = time.time()
    while time.time() - start_time < duration:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                print(f"Received line: {line}")
                data = line.split(',')
                data = data[1:-1]  
                if len(data) == 6:  # Expecting accel (x, y, z) and gyro (x, y, z)
                    imu_data.append(list(map(float, data)))
                else:
                    print(f"Unexpected data format: {data}")
            except Exception as e:
                print(f"Error parsing data: {e}")
    imu_data = np.array(imu_data)
    # Normalize the IMU data
    imu_data = (imu_data - imu_data.min(axis=0)) / (imu_data.max(axis=0) - imu_data.min(axis=0))
    print(f"IMU data shape: {imu_data.shape}")
    if imu_data.shape[0] >= 500:
            #sampled_indices = np.random.choice(imu_data.shape[0], size=395, replace=False)
            imu_data = imu_data[:500,:]
    else:
            imu_data=expand_by_interpolation(imu_data, target_rows=500)
            print(f"Warning: Not enough data collected for sampling. Using all {imu_data.shape[0]} records.")
    print(f"IMU data shape after sampling: {imu_data.shape}")
    # Reshape for the ML model (flattening the array)
    return imu_data.flatten().reshape(1, -1)

def main():
    """
    Main function to control the Tello UAV based on gestures.
    """
    # Initialize Tello
    tello = Tello()
    tello.connect()
    print(f"Tello Battery: {tello.get_battery()}%")
    try:
        print("Calibrating IMU...")
        tello.send_control_command("imu_calibration")
        print("IMU calibration complete.")
    except Exception as e:
        print(f"IMU calibration failed: {e}")

    # Initialize Serial connection to ESP32
    ser = init_serial_connection(SERIAL_PORT, BAUD_RATE)
    if ser is None:
        return

    try:
        print("Taking off...")
        tello.takeoff()  # Automatically take off at the start
        print("Perform a gesture for 5 seconds to control the UAV...")

        while True:
            # Clear serial buffer before recording new data
            input("Press Enter to proceed to the next gesture...")
            clear_serial_buffer(ser)
            
            # Record IMU data from the sensor
            imu_data = record_imu_data(ser, duration=DURATION)

            # Predict the gesture using the SVM model
            gesture = svm_model.predict(imu_data)[0]
            print(f"Predicted Gesture: {labels_map[gesture]}")

            # Execute the corresponding Tello command
            if gesture in gesture_command_map:
                gesture_command_map[gesture](tello)

            # Exit loop if "land" gesture is detected
            if gesture == 8:
                print("Landing the UAV. Exiting...")
                break

    except KeyboardInterrupt:
        print("Interrupted! Landing the UAV safely...")
    finally:
        tello.land()  # Ensure safe landing
        ser.close()

if __name__ == "__main__":
    main()
