(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types 
    robot room ball

  )

  (:predicates 
    (in_room ?r - robot ?rm - room)
    (in_room ?b - ball ?rm - room)
    (holding ?r - robot ?b - ball)
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
    :precondition (and (in_room ?b ?rm)
                       (in_room ?r ?rm)
                       (free_gripper ?r)
    )
    :effect (and (holding ?r ?b)
                (not (in_room ?b ?rm))
                (not (free_gripper ?r))
    )
  )

  (:action drop
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and (holding ?r ?b)
                       (in_room ?r ?rm)
    )
    :effect (and (in_room ?b ?rm)
                (free_gripper ?r)
                (not (holding ?r ?b))
    )
  )
)