(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 - robot 
    room1 room2 room3 - room 
    ball1 ball2 - ball 

  )

  (:init 
    (in_room robot1 room1)
    (in_room_ball ball1 room3)
    (in_room_ball ball2 room3)
    (free_gripper robot1)

  )

  (:goal 
    (and 
      (in_room_ball ball1 room1)
      (in_room_ball ball2 room1)

  ))

)