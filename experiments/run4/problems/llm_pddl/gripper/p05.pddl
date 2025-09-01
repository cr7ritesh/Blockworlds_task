(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 
    room1 room2 
    ball1 ball2 ball3 ball4 ball5 
    left right 

  )

  (:init 
    (in-room robot2 room1)
    (in-room robot1 room2)
    (in-room ball2 room1)
    (in-room ball5 room1)
    (in-room ball1 room1)
    (in-room ball3 room1)
    (in-room ball4 room1)
    (free-gripper left)
    (free-gripper right)

  )

  (:goal 
    (and 
      (in-room ball1 room1)
      (in-room ball2 room1)
      (in-room ball3 room2)
      (in-room ball4 room1)
      (in-room ball5 room1)
  ))

)