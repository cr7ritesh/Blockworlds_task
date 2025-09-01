(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball
  )

  (:predicates 
    (in_room ?r - robot ?rm - room)
    (in_ball ?b - ball ?rm - room)
    (carrying ?r - robot ?b - ball)
    (free_gripper ?r - robot)
  )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in_room ?r ?rm1)
    :effect (and (in_room ?r ?rm2)
                (not (in_room ?r ?rm1))
    )
  )

  (:action pick
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and (in_room ?r ?rm)
                       (in_ball ?b ?rm)
                       (free_gripper ?r)
    )
    :effect (and (carrying ?r ?b)
                 (not (in_ball ?b ?rm))
                 (not (free_gripper ?r))
    )
  )

  (:action drop
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and (carrying ?r ?b)
                       (in_room ?r ?rm)
    )
    :effect (and (in_ball ?b ?rm)
                 (free_gripper ?r)
                 (not (carrying ?r ?b))
    )
  )
)