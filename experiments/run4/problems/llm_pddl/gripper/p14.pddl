(define (problem robot_transport)

  (:domain robot_gripper)

  (:objects
    robot1 - robot
    room1 room2 room3 room4 - room
    ball1 ball2 ball3 ball4 ball5 - ball
  )

  (:init
    (robot_in_room robot1 room2)
    (in_room ball2 room1)
    (in_room ball4 room3)
    (in_room ball5 room2)
    (in_room ball1 room2)
    (in_room ball3 room1)
    (gripper_free robot1)
  )

  (:goal (and (in_room ball1 room2)
              (in_room ball2 room4)
              (in_room ball3 room4)
              (in_room ball4 room3)
              (in_room ball5 room2)
  ))
)