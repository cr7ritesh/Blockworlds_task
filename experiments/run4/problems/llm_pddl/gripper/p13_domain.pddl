(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types 
    robot room ball

  )

  (:predicates 
    (in_room ?r - robot ?rm - room)
    (in_gripper ?r - robot ?b - ball)
    (in_room_ball ?b - ball ?rm - room)
    (free_gripper ?r - robot)

  )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in_room ?r ?rm1)
    :effect (and
      (in_room ?r ?rm2)
      (not (in_room ?r ?rm1))
    )
  )

  (:action pick
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and
      (in_room_ball ?b ?rm)
      (in_room ?r ?rm)
      (free_gripper ?r)
    )
    :effect (and
      (in_gripper ?r ?b)
      (not (in_room_ball ?b ?rm))
      (not (free_gripper ?r))
    )
  )

  (:action drop
    :parameters (?r - robot ?b - ball ?rm - room)
    :precondition (and
      (in_gripper ?r ?b)
      (in_room ?r ?rm)
    )
    :effect (and
      (in_room_ball ?b ?rm)
      (free_gripper ?r)
      (not (in_gripper ?r ?b))
    )
  )

)