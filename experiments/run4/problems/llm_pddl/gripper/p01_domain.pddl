(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball gripper_state
    )

  (:predicates 
    (in_room ?r - robot ?rm - room)
    (in_room ?b - ball ?rm - room)
    (holding ?r - robot ?b - ball ?g - gripper_state)
    (free_gripper ?r - robot ?g - gripper_state)
    )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in_room ?r ?rm1)
    :effect (and (in_room ?r ?rm2)
                (not (in_room ?r ?rm1))
                )
    )

  (:action pick
    :parameters (?r - robot ?b - ball ?g - gripper_state ?rm - room)
    :precondition (and (in_room ?b ?rm)
                       (in_room ?r ?rm)
                       (free_gripper ?r ?g)
                       )
    :effect (and (holding ?r ?b ?g)
                 (not (in_room ?b ?rm))
                 (not (free_gripper ?r ?g))
                 )
    )

  (:action drop
    :parameters (?r - robot ?b - ball ?g - gripper_state ?rm - room)
    :precondition (and (holding ?r ?b ?g)
                       (in_room ?r ?rm)
                       )
    :effect (and (in_room ?b ?rm)
                 (free_gripper ?r ?g)
                 (not (holding ?r ?b ?g))
                 )
    )
)