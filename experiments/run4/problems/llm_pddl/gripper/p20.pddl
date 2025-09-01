(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 robot3 robot4 
    room1 room2 room3 
    ball1 ball2 
    left_gripper right_gripper 
    )

  (:init 
    (in_room robot1 room1)
    (in_room robot2 room1)
    (in_room robot3 room1)
    (in_room robot4 room1)
    (in_room ball1 room2)
    (in_room ball2 room3)
    (free_gripper left_gripper robot1)
    (free_gripper right_gripper robot1)
    (free_gripper left_gripper robot2)
    (free_gripper right_gripper robot2)
    (free_gripper left_gripper robot3)
    (free_gripper right_gripper robot3)
    (free_gripper left_gripper robot4)
    (free_gripper right_gripper robot4)
    )

  (:goal 
    (and (in_room ball1 room2)
         (in_room ball2 room3)
         )
    )
)