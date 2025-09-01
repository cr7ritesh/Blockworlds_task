(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball

  )

  (:predicates 
    (in-room ?r - robot ?rm - room)
    (in-gripper ?b - ball ?g - gripper)
    (free-gripper ?g - gripper)

  )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in-room ?r ?rm1)
    :effect (and
      (in-room ?r ?rm2)
      (not (in-room ?r ?rm1))
    )
  )

  (:action pick
    :parameters (?r - robot ?rm - room ?b - ball ?g - gripper)
    :precondition (and
      (in-room ?b ?rm)
      (in-room ?r ?rm)
      (free-gripper ?g)
    )
    :effect (and
      (in-gripper ?b ?g)
      (not (in-room ?b ?rm))
      (not (free-gripper ?g))
    )
  )

  (:action drop
    :parameters (?r - robot ?rm - room ?b - ball ?g - gripper)
    :precondition (and
      (in-gripper ?b ?g)
      (in-room ?r ?rm)
    )
    :effect (and
      (in-room ?b ?rm)
      (free-gripper ?g)
      (not (in-gripper ?b ?g))
    )
  )

)