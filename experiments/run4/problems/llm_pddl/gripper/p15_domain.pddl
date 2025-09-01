(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types 
    robot room ball
  )

  (:predicates 
    (in ?r - robot ?room - room)
    (in ?b - ball ?room - room)
    (carrying ?r - robot ?b - ball)
    (handFree ?r - robot)
  )

  (:action move
    :parameters (?r - robot ?room1 ?room2 - room)
    :precondition (and (in ?r ?room1) )
    :effect (and (in ?r ?room2)
                 (not (in ?r ?room1))
    )
  )

  (:action pick
    :parameters (?r - robot ?b - ball ?room - room)
    :precondition (and (in ?b ?room)
                        (in ?r ?room)
                        (handFree ?r)
    )
    :effect (and (carrying ?r ?b)
                 (not (in ?b ?room))
                 (not (handFree ?r))
    )
  )

  (:action drop
    :parameters (?r - robot ?b - ball ?room - room)
    :precondition (and (carrying ?r ?b)
                        (in ?r ?room)
    )
    :effect (and (in ?b ?room)
                 (handFree ?r)
                 (not (carrying ?r ?b))
    )
  )
)