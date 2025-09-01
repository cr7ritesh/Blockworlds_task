(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 robot3 
    room1 room2 
    ball1 ball2 ball3 ball4 
    left_gripper right_gripper 
    )

  (:init 
    (in-room robot3 room2)
    (in-room robot1 room1)
    (in-room robot2 room1)
    (in-room ball3 room2)
    (in-room ball4 room2)
    (in-room ball2 room2)
    (in-room ball1 room2)
    (free-gripper left_gripper robot1)
    (free-gripper right_gripper robot1)
    (free-gripper left_gripper robot2)
    (free-gripper right_gripper robot2)
    (free-gripper left_gripper robot3)
    (free-gripper right_gripper robot3)
    )

  (:goal 
    (and (in-room ball1 room2)
         (in-room ball2 room1)
         (in-room ball3 room1)
         (in-room ball4 room1)
         )
    )
)