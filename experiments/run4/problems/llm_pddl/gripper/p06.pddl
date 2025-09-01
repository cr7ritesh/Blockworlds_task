(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 
    room1 room2 room3 
    ball1 
    left right

  )

  (:init 
    (in-room robot1 room3)
    (in-room robot2 room2)
    (in-room ball1 room1)
    (free-gripper robot1 left)
    (free-gripper robot1 right)
    (free-gripper robot2 left)
    (free-gripper robot2 right)
  )

  (:goal 
    (and 
      (in-room ball1 room3)
    )
  )

)