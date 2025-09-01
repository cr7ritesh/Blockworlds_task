(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 - robot 
    room1 room2 room3 room4 room5 - room 
    ball1 ball2 ball3 - ball 
  )

  (:init 
    (in robot1 room4)
    (handFree robot1)
    (in ball1 room3)
    (in ball2 room5)
    (in ball3 room3)
  )

  (:goal 
    (and 
      (in ball1 room5)
      (in ball2 room2)
      (in ball3 room1)
  ))
)