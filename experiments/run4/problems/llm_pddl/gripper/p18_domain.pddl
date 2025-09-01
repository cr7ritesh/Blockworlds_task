(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types robot room ball gripper_state)

  (:predicates
    (in-room ?robot -robot ?room -room)
    (in-gripper ?ball -ball ?gripper -gripper_state)
    (free-gripper ?gripper -gripper_state)
  )

  (:functions
    (room-count)
    (ball-count)
  )

  (:action move
    :parameters (?robot -robot ?from -room ?to -room)
    :precondition (in-room ?robot ?from)
    :effect (and
      (not (in-room ?robot ?from))
      (in-room ?robot ?to)
    )
  )

  (:action pick
    :parameters (?robot -robot ?ball -ball ?gripper -gripper_state ?room -room)
    :precondition (and
      (in-room ?robot ?room)
      (in-room ?ball ?room)
      (free-gripper ?gripper)
    )
    :effect (and
      (not (in-room ?ball ?room))
      (in-gripper ?ball ?gripper)
      (not (free-gripper ?gripper))
    )
  )

  (:action drop
    :parameters (?robot -robot ?ball -ball ?gripper -gripper_state ?room -room)
    :precondition (and
      (in-gripper ?ball ?gripper)
      (in-room ?robot ?room)
    )
    :effect (and
      (in-room ?ball ?room)
      (free-gripper ?gripper)
      (not (in-gripper ?ball ?gripper))
    )
  )
)