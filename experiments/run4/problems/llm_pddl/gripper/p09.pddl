(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 robot3 
    room1 room2 room3 room4 
    ball1 ball2 ball3 ball4 ball5 ball6 ball7
  )

  (:init 
    (in-room robot3 room3)
    (in-room robot2 room1)
    (in-room robot1 room4)
    (in-room ball1 room4)
    (in-room ball7 room3)
    (in-room ball3 room3)
    (in-room ball4 room2)
    (in-room ball6 room1)
    (in-room ball2 room3)
    (in-room ball5 room2)
    (free-gripper robot1)
    (free-gripper robot2)
    (free-gripper robot3)
  )

  (:goal 
    (and 
      (in-room ball1 room1)
      (in-room ball2 room4)
      (in-room ball3 room3)
      (in-room ball4 room4)
      (in-room ball5 room3)
      (in-room ball6 room2)
      (in-room ball7 room1)
    )
  )

)