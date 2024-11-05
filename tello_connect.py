from djitellopy import Tello

# Initialize the Tello drone
drone = Tello()
drone.connect()
print(f"Battery level: {drone.get_battery()}%")

# Takeoff
drone.takeoff()

# Define gesture-based functions
def move_right():
    print("Moving right")
    drone.move_right(50)  # Move right by 50 cm

def rotate_clockwise():
    print("Gesture detected: Rotating clockwise")
    drone.rotate_clockwise(45)  # Rotate by 45 degrees 

def rotate_counterclockwise():
    print("Gesture detected: Rotating counterclockwise")
    drone.rotate_counter_clockwise(45) 

def move_left():
    print("Moving left")
    drone.move_left(50)  # Move left by 50 cm

def move_up():
    print("Moving up")
    drone.move_up(50)  # Move up by 50 cm

def move_down():
    print("Moving down")
    drone.move_down(50)  # Move down by 50 cm

def move_forward():
    print("Moving forward")
    drone.move_forward(50)  # Move forward by 50 cm

def move_backward():
    print("Moving backward")
    drone.move_back(50)  # Move back by 50 cm

# Gesture control loop
while True:
    gesture = input("Enter gesture (right, left, up, down, forward, backward, land): ").lower()
    
    if gesture == "right":
        move_right()
    elif gesture == "left":
        move_left()
    elif gesture == "up":
        move_up()
    elif gesture == "down":
        move_down()
    elif gesture == "forward":
        move_forward()
    elif gesture == "backward":
        move_backward()
    elif gesture == "rotate_left":
        rotate_counterclockwise()
    elif gesture == "rotate_right":
        rotate_clockwise()
    elif gesture == "land":
        print("Landing")
        drone.land()
        break
    else:
        print("Unknown gesture. Please try again.")

# End the drone connection
drone.end()
