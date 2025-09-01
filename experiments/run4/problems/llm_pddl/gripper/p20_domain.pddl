(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball gripper_state
    )

  (:predicates 
    (in_room ?r - robot ?rm - room)
    (in_gripper ?b - ball ?g - gripper_state ?r - robot)
    (free_gripper ?g - gripper_state ?r - robot)
    )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in_room ?r ?rm1)
    :effect (and (in_room ?r ?rm2)
                (not (in_room ?r ?rm1))
                )
    )

  (:action pick
    :parameters (?b - ball ?g - gripper_state ?r - robot ?rm - room)
    :precondition (and (in_room ?b ?rm)
                       (in_room ?r ?rm)
                       (free_gripper ?g ?r)
                       )
    :effect (and (in_gripper ?b ?g ?r)
                 (not (in_room ?b ?rm))
                 (not (free_gripper ?g ?r))
                 )
    )

  (:action drop
    :parameters (?b - ball ?g - gripper_state ?r - robot ?rm - room)
    :precondition (and (in_gripper ?b ?g ?r)
                       (in_room ?r ?rm)
                       )
    :effect (and (in_room ?b ?rm)
                 (free_gripper ?g ?r)
                 (not (in_gripper ?b ?g ?r))
                 )
    )
)