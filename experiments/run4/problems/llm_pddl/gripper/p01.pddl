(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 
    room1 room2 
    ball1 ball2 
    left_gripper right_gripper
    )

  (:init 
    (in_room robot1 room1)
    (in_room robot2 room1)
    (in_room ball1 room1)
    (in_room ball2 room1)
    (free_gripper robot1 left_gripper)
    (free_gripper robot1 right_gripper)
    (free_gripper robot2 left_gripper)
    (free_gripper robot2 right_gripper)
    )

  (:goal 
    (and (in_room ball1 room1)
         (in_room ball2 room2)
         )
    )
)