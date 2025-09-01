(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects
    r1 r2 r3 -room
    rob1 rob2 rob3 rob4 -robot
    b1 b2 b3 b4 b5 b6 -ball
    left right -gripper_state
  )

  (:init
    (in-room rob3 r3)
    (in-room rob2 r3)
    (in-room rob4 r1)
    (in-room rob1 r3)
    (in-room b2 r2)
    (in-room b4 r3)
    (in-room b3 r1)
    (in-room b6 r3)
    (in-room b1 r2)
    (in-room b5 r3)
    (free-gripper left)
    (free-gripper right)
  )

  (:goal (and
    (in-room b1 r1)
    (in-room b2 r1)
    (in-room b3 r2)
    (in-room b4 r3)
    (in-room b5 r3)
    (in-room b6 r3)
  ))
)