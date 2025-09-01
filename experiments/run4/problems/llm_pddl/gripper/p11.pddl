(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 - robot 
    room1 room2 - room 
    ball1 ball2 ball3 - ball 
  )

  (:init 
    (in_room robot1 room1)
    (in_room ball1 room1)
    (in_room ball2 room1)
    (in_room ball3 room1)
    (free_gripper robot1)
  )

  (:goal 
    (and 
      (in_room ball1 room1) 
      (in_room ball2 room1) 
      (in_room ball3 room2) 
    )
  )

)