(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects 
    robot1 robot2 
    room1 room2 room3 room4 room5 
    ball1 ball2 
  )

  (:init 
    (in robot1 room1)
    (in robot2 room2)
    (in ball1 room1)
    (in ball2 room1)
    (free-gripper robot1)
    (free-gripper robot2)
  )

  (:goal 
    (and (in ball1 room5)
         (in ball2 room4)
    )
  )
)