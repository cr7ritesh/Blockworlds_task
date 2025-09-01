(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types ball robot room gripper_state)

  (:predicates
    (in_room ?r - robot ?rm - room)
    (in_gripper ?b - ball ?g - gripper ?r - robot)
    (free_gripper ?g - gripper ?r - robot)
    (in ?b - ball ?rm - room)
  )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (and (in_room ?r ?rm1) )
    :effect (and (in_room ?r ?rm2)
                 (not (in_room ?r ?rm1))
    )
  )

  (:action pick
    :parameters (?b - ball ?g - gripper ?r - robot ?rm - room)
    :precondition (and (in ?b ?rm)
                       (in_room ?r ?rm)
                       (free_gripper ?g ?r)
    )
    :effect (and (in_gripper ?b ?g ?r)
                 (not (in ?b ?rm))
                 (not (free_gripper ?g ?r))
    )
  )

  (:action drop
    :parameters (?b - ball ?g - gripper ?r - robot ?rm - room)
    :precondition (and (in_gripper ?b ?g ?r)
                       (in_room ?r ?rm)
    )
    :effect (and (in ?b ?rm)
                 (free_gripper ?g ?r)
                 (not (in_gripper ?b ?g ?r))
    )
  )
)