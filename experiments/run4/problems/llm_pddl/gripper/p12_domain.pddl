(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types ball room)

  (:predicates
    (in ?b - ball ?r - room)
    (holding ?b - ball)
    (in_room ?r - room)
    (free_gripper)
  )

  (:action move
    :parameters (?r1 - room ?r2 - room)
    :precondition (and (in_room ?r1) (not (in_room ?r2)))
    :effect (and (in_room ?r2) (not (in_room ?r1)))
  )

  (:action pick
    :parameters (?b - ball ?r - room)
    :precondition (and (in ?b ?r) (in_room ?r) (free_gripper))
    :effect (and (holding ?b) (not (in ?b ?r)) (not (free_gripper)))
  )

  (:action drop
    :parameters (?b - ball ?r - room)
    :precondition (and (holding ?b) (in_room ?r))
    :effect (and (in ?b ?r) (free_gripper) (not (holding ?b)))
  )
)