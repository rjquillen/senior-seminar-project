import time
import Robot

LEFT_TRIM   = 0
RIGHT_TRIM  = -1

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

robot.forward(150, 1.0)   # Move forward at speed 150 for 1 second.
robot.left(100, 0.5)      # Spin left at speed 200 for 0.5 seconds.
robot.forward(150, 1.0)   # Repeat the same movement 3 times below...
robot.left(100, 0.5)
robot.forward(150, 1.0)
robot.left(100, 0.5)
robot.forward(150, 1.0)
robot.right(100, 0.5)

robot.backward(150, 1.0)
robot.right(100, 0.5)
robot.backward(150, 1.0)
robot.right(100, 0.5)
robot.backward(150, 1.0)
robot.right(100, 0.5)
robot.backward(150, 1.0)
