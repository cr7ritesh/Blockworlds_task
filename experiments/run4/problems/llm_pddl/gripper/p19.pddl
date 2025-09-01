(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects
    r1 r2 r3 r4 - robot
    g1 g2 - gripper
    rm1 rm2 rm3 rm4 rm5 - room
    b1 b2 b3 b4 b5 b6 - ball
  )

  (:init
    (in_room r4 rm4)
    (in_room r3 rm4)
    (in_room r2 rm1)
    (in_room r1 rm4)
    (in b2 rm2)
    (in b6 rm1)
    (in b3 rm5)
    (in b4 rm3)
    (in b5 rm4)
    (in b1 rm2)
    (free_gripper g1 r1)
    (free_gripper g2 r1)
    (free_gripper g1 r2)
    (free_gripper g2 r2)
    (free_gripper g1 r3)
    (free_gripper g2 r3)
    (free_gripper g1 r4)
    (free_gripper g2 r4)
  )

  (:goal (and (in b1 rm3)
             (in b2 rm3)
             (in b3 rm1)
             (in b4 rm2)
             (in b5 rm1)
             (in b6 rm2)
  ))
)