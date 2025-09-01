(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 robot3 
    room1 room2 room3 room4 
    ball1 ball2 ball3 
  )

  (:init 
    (in_room robot1 room4)
    (in_room robot2 room2)
    (in_room robot3 room1)
    (free_gripper robot1)
    (free_gripper robot2)
    (free_gripper robot3)
    (in_ball ball1 room4)
    (in_ball ball2 room4)
    (in_ball ball3 room2)
  )

  (:goal 
    (and (in_ball ball1 room2)
         (in_ball ball2 room3)
         (in_ball ball3 room3)
  )
)