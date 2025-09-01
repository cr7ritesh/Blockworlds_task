(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects
    robot1 - robot
    room1 room2 room3 - room
    ball1 ball2 ball3 ball4 ball5 - ball
  )

  (:init
    (in_room room2)
    (in ball1 room3)
    (in ball3 room2)
    (in ball2 room2)
    (in ball5 room2)
    (in ball4 room1)
    (free_gripper)
  )

  (:goal
    (and
      (in ball1 room3)
      (in ball2 room1)
      (in ball3 room2)
      (in ball4 room2)
      (in ball5 room3)
    )
  )
)