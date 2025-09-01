(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball gripper_state
    )

  (:predicates 
    (in-room ?r - robot ?rm - room)
    (in-gripper ?b - ball ?g - gripper ?r - robot)
    (free-gripper ?g - gripper ?r - robot)
    )

  (:action move
    :parameters (?r - robot ?rm1 ?rm2 - room)
    :precondition (in-room ?r ?rm1)
    :effect (and (in-room ?r ?rm2)
                (not (in-room ?r ?rm1))
                )
    )

  (:action pick
    :parameters (?b - ball ?g - gripper ?r - robot ?rm - room)
    :precondition (and (in-room ?b ?rm)
                      (in-room ?r ?rm)
                      (free-gripper ?g ?r)
                      )
    :effect (and (in-gripper ?b ?g ?r)
                  (not (in-room ?b ?rm))
                  (not (free-gripper ?g ?r))
                  )
    )

  (:action drop
    :parameters (?b - ball ?g - gripper ?r - robot ?rm - room)
    :precondition (and (in-gripper ?b ?g ?r)
                      (in-room ?r ?rm)
                      )
    :effect (and (in-room ?b ?rm)
                  (free-gripper ?g ?r)
                  (not (in-gripper ?b ?g ?r))
                  )
    )
)