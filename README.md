**Gesture-Controlled UAV using ESP32 S3 and IMU Sensor**
_**Overview**_
This project enables real-time control of an Unmanned Aerial Vehicle (UAV) using hand gestures. The system utilizes the ESP32 S3 microcontroller and an MPU6050 IMU sensor to capture motion data from the user’s hand, process the data, and send corresponding commands to the UAV via Bluetooth.

<img width="350" alt="image" src="https://github.com/user-attachments/assets/803a1a46-4306-4d3b-81ae-88c190250f2f">

_**Process Flow**_

_1. Collect Data from IMU Sensor (MPU6050)_
The MPU6050 IMU sensor captures real-time motion data from the user’s hand. This data includes:
Acceleration (via accelerometer)
Angular velocity (via gyroscope)
These measurements are essential for identifying the user’s hand gestures.

_2. Pre-process Data_
Once collected, the motion data undergoes a pre-processing step:

Fast Fourier Transform (FFT) is applied to reduce noise and extract relevant features such as frequency components.
This step improves gesture recognition accuracy by providing cleaner, more meaningful data to the machine learning model.

_3. Feed Pre-processed Data to ML Model_
The cleaned, pre-processed data is fed into a pre-trained machine learning (ML) model. This model is designed to recognize specific gestures.
The model analyzes the data and classifies the hand gestures based on patterns learned during training.

_4. Gesture Prediction from ML Model_
The ML model outputs a prediction of the gesture performed by the user. This prediction is converted into a command that can be understood by the UAV.

_5. Connect to UAV using Bluetooth_
A Bluetooth connection is established between the ESP32 S3 and the UAV. Bluetooth is used due to its low latency and ease of integration for real-time control applications.

_6. Send Predicted Gesture to UAV_
The predicted gesture is transmitted via the Bluetooth connection to the UAV. The UAV’s flight controller receives the command and prepares to execute the corresponding action.

_7. UAV Executes the Command_
The UAV performs the maneuver based on the recognized gesture. For example:
An UP gesture may trigger the UAV to ascend.
A LEFT gesture may cause the UAV to move left.
This gesture-based interaction allows for intuitive, real-time control of the UAV.

_8. Repeat or End_
The process can be repeated continuously as new gestures are performed. The system can also be reset or turned off once the desired operation is complete.

**_Conclusion_**
This project showcases the use of embedded systems, sensor data processing, and machine learning to develop a gesture-controlled UAV. By using the ESP32 S3 and MPU6050 IMU sensor, we enable real-time, gesture-based control, providing an intuitive interface for UAV operation.

