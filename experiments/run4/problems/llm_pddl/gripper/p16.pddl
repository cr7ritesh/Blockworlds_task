(define (problem robot_gripper_problem)

  (:domain robot_gripper)

  (:objects
    R1 R2 R3 R4
    RM1 RM2 RM3 RM4
    B1 B2 B3 B4 B5 B6 B7 B8
    GL GR
    - gripper_state
  )

  (:init
    (in_room R3 RM3)
    (in_room R4 RM4)
    (in_room R1 RM1)
    (in_room R2 RM4)
    (in_room B3 RM1)
    (in_room B4 RM3)
    (in_room B2 RM3)
    (in_room B5 RM4)
    (in_room B7 RM1)
    (in_room B6 RM4)
    (in_room B1 RM3)
    (in_room B8 RM1)
    (free_gripper R1 GL)
    (free_gripper R1 GR)
    (free_gripper R2 GL)
    (free_gripper R2 GR)
    (free_gripper R3 GL)
    (free_gripper R3 GR)
    (free_gripper R4 GL)
    (free_gripper R4 GR)
  )

  (:goal (and (in_room B1 RM2)
             (in_room B2 RM3)
             (in_room B3 RM1)
             (in_room B4 RM3)
             (in_room B5 RM1)
             (in_room B6 RM1)
             (in_room B7 RM4)
             (in_room B8 RM2)))