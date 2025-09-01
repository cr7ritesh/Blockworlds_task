Here is an optimal plan to solve the problem: 

- Move robot1 from room4 to room3 (precondition: robot1 is in a room; effect: robot1 is now in room3)
- Pick up ball1 in room3 with robot1's left gripper (preconditions: ball1 is in room3, robot1 is in room3, and the left gripper is free; effect: ball1 is held by the left gripper, and the gripper is no longer free)
- Move robot1 from room3 to room5 (precondition: robot1 is in room3; effect: robot1 is now in room5)
- Drop ball1 in room5 (preconditions: robot1 is carrying ball1, and robot1 is in room5; effect: ball1 is now in room5, and the left gripper is free)
- Pick up ball2 in room5 with robot1's left gripper (preconditions: ball2 is in room5, robot1 is in room5, and the left gripper is free; effect: ball2 is held by the left gripper)
- Move robot1 from room5 to room2 (precondition: robot1 is in room5; effect: robot1 is now in room2)
- Drop ball2 in room2 (preconditions: robot1 is carrying ball2, and robot1 is in room2; effect: ball2 is now in room2, and the left gripper is free)
- Move robot1 from room2 to room3 (precondition: robot1 is in room2; effect: robot1 is now in room3)
- Pick up ball3 in room3 with robot1's left gripper (preconditions: ball3 is in room3, robot1 is in room3, and the left gripper is free; effect: ball3 is held by the left gripper)
- Move robot1 from room3 to room1 (precondition: robot1 is in room3; effect: robot1 is now in room1)
- Drop ball3 in room1 (preconditions: robot1 is carrying ball3, and robot1 is in room1; effect: ball3 is now in room1, and the left gripper is free)

This plan ensures that all three balls are transported to their respective destinations in an optimal manner, with the robot making efficient use of its movements and grippers.