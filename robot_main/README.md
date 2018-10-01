# Disaster Response Robot

The files in this directory make up the main code of the disaster response robot. The purpose of each file is as follows:

* *main:* Initializes robot and places it in either manual or automatic mode.
* *automatic:* Robot moves in an autonomous mode, searching the given area in a grid-like fashion.
* *manual:* Controls robot in manual mode by querying the the server for a direction and moving the robot in that direction.
* *robot:* Abstracts the robot's communication with the server, sensors and motors into higher-level commands.
* *sensors:* Reads from and controls the different analog sensors and component on the robot. This includes a photoresistor, temperature sensor, ultrasonic sensor, servo motor and infrared LED.
* *camera:* Initializes the robot's camera. During the robots run, the camera will send a livestream of photos to the server as well as search for any human faces. Once a face is detected, an image is taken, cropped to the face size, and sent to the server.
* *motor:* Controls the robot's two motors.

The provided Fritzing file shows the robot schematic including all sensors and actuators.