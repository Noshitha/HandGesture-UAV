<img width="350" alt="image" src="https://github.com/user-attachments/assets/803a1a46-4306-4d3b-81ae-88c190250f2f">

**Collect Data from IMU Sensor (MPU6050):**
The Inertial Measurement Unit (IMU) sensor, MPU6050, captures real-time motion data from the user’s hand. This data includes information about acceleration (from the accelerometer) and angular velocity (from the gyroscope). This raw data is crucial for identifying the hand gestures made by the user.

**Pre-process Data:**
Once the motion data is captured, it goes through a pre-processing step. Fast Fourier Transform (FFT) is applied to clean up the noise in the data and extract relevant features, such as frequency components of the gesture movements. Pre-processing is important for improving the accuracy of the gesture recognition model by providing cleaner data inputs.

**Feed Pre-processed Data to ML Model:**
The pre-processed data is then fed into a machine learning (ML) model, which has been trained to recognize specific hand gestures like UP, DOWN, LEFT, and RIGHT. This model analyzes the incoming data and classifies it based on the patterns it has learned during the training phase.

**Gesture Prediction from ML Model:**
The ML model outputs a prediction, identifying the specific gesture performed by the user. The recognized gesture is converted into a command that the UAV can understand, such as move up, down, or rotate.

**Connect to UAV using Bluetooth:**
The system establishes a Bluetooth connection with the UAV (Unmanned Aerial Vehicle) to transmit the recognized gesture in real time. Bluetooth is chosen for its low latency and ease of integration with mobile systems.

**Send Predicted Gesture to UAV:**
The predicted gesture is sent to the UAV via the Bluetooth connection. The UAV’s flight controller receives this command and prepares to execute the corresponding action.

**UAV Executes the Command:**
Based on the gesture received, the UAV performs the corresponding flight maneuver. For example, an UP gesture may cause the UAV to ascend, while a LEFT gesture could trigger a leftward movement. This gesture-based control provides an intuitive and interactive method for operating the UAV.

**End:**
The process can repeat as new gestures are made, allowing for continuous real-time control of the UAV. Once the task is completed, the system can be turned off or reset for further operation.
