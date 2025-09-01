(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 
    room1 room2 room3 
    ball1 ball2 ball3 ball4 
  )

  (:init 
    (in-room robot1 room2)
    (in-room robot2 room3)
    (free-gripper robot1)
    (free-gripper robot2)
    (in-room ball1 room3)
    (in-room ball2 room1)
    (in-room ball3 room1)
    (in-room ball4 room3)
  )

  (:goal 
    (and 
      (in-room ball1 room2)
      (in-room ball2 room2)
      (in-room ball3 room3)
      (in-room ball4 room3)
    )
  )

)