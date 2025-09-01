(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types 
    robot room ball
  )

  (:predicates 
    (in ?r - robot ?rm - room)
    (in ?b - ball ?rm - room)
    (carrying ?r - robot ?b - ball)
    (free-gripper ?r - robot)
  )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (and (in ?r ?rm1) )
    :effect (and (in ?r ?rm2)
                 (not (in ?r ?rm1))
    )
  )

  (:action pick
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and (in ?b ?rm)
                        (in ?r ?rm)
                        (free-gripper ?r)
                    )
    :effect (and (carrying ?r ?b)
                 (not (in ?b ?rm))
                 (not (free-gripper ?r))
    )
  )

  (:action drop
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and (carrying ?r ?b)
                        (in ?r ?rm)
                    )
    :effect (and (in ?b ?rm)
                 (free-gripper ?r)
                 (not (carrying ?r ?b))
    )
  )
)