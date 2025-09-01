(define (problem robot_transport_problem)

  (:domain robot_transport)

  (:objects 
    robot1 robot2 robot3 - robot
    room1 room2 room3 room4 - room
    ball1 ball2 ball3 ball4 - ball

  )

  (:init 
    (in-room robot1 room4)
    (in-room robot2 room4)
    (in-room robot3 room1)
    (in-room-robot-free robot1 room4)
    (in-room-robot-free robot2 room4)
    (in-room-robot-free robot3 room1)
    (in-room-gripper-free robot1 room4)
    (in-room-gripper-free robot2 room4)
    (in-room-gripper-free robot3 room1)
    (in-room-ball ball2 room1)
    (in-room-ball ball4 room2)
    (in-room-ball ball1 room1)
    (in-room-ball ball3 room1)

  )

  (:goal 
    (and 
      (in-room-ball ball1 room1)
      (in-room-ball ball2 room1)
      (in-room-ball ball3 room3)
      (in-room-ball ball4 room2)
    )
  )

)