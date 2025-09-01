(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types ball room robot)

  (:predicates
    (in_room ?ball - ball ?room - room)
    (robot_in_room ?robot - robot ?room - room)
    (carrying ?robot - robot ?ball - ball)
    (gripper_free ?robot - robot)
  )

  (:action move
    :parameters (?robot - robot ?from - room ?to - room)
    :precondition (and (robot_in_room ?robot ?from) )
    :effect (and (robot_in_room ?robot ?to)
                 (not (robot_in_room ?robot ?from))
    )
  )

  (:action pick
    :parameters (?robot - robot ?ball - ball ?room - room)
    :precondition (and (in_room ?ball ?room)
                       (robot_in_room ?robot ?room)
                       (gripper_free ?robot)
    )
    :effect (and (carrying ?robot ?ball)
                 (not (in_room ?ball ?room))
                 (not (gripper_free ?robot))
    )
  )

  (:action drop
    :parameters (?robot - robot ?ball - ball ?room - room)
    :precondition (and (carrying ?robot ?ball)
                       (robot_in_room ?robot ?room)
    )
    :effect (and (in_room ?ball ?room)
                 (gripper_free ?robot)
                 (not (carrying ?robot ?ball))
    )
  )
)