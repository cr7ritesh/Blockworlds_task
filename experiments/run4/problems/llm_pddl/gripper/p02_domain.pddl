(define (domain robot_gripper)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball
  )

  (:predicates 
    (in-room robot room)
    (in-gripper robot ball)
    (free-gripper robot)
    (in-room ball room)
  )

  (:action move
    :parameters 
      (?r - robot ?rm - room ?rm2 - room)
    :precondition 
      (and 
        (in-room ?r ?rm)
      )
    :effect 
      (and 
        (in-room ?r ?rm2)
        (not (in-room ?r ?rm))
      )
  )

  (:action pick
    :parameters 
      (?r - robot ?b - ball ?rm - room)
    :precondition 
      (and 
        (in-room ?r ?rm)
        (in-room ?b ?rm)
        (free-gripper ?r)
      )
    :effect 
      (and 
        (in-gripper ?r ?b)
        (not (in-room ?b ?rm))
        (not (free-gripper ?r))
      )
  )

  (:action drop
    :parameters 
      (?r - robot ?b - ball ?rm - room)
    :precondition 
      (and 
        (in-gripper ?r ?b)
        (in-room ?r ?rm)
      )
    :effect 
      (and 
        (in-room ?b ?rm)
        (free-gripper ?r)
        (not (in-gripper ?r ?b))
      )
  )

)