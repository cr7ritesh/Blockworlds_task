(define (domain robot_gripper)

  (:requirements :strips :typing)

  (:types 
    robot room ball

  )

  (:predicates 
    (in-room robot room)
    (in-gripper robot gripper ball)
    (free-gripper robot gripper)

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
      (?r - robot ?rm - room ?g - gripper ?b - ball)
    :precondition 
      (and 
        (in-room ?r ?rm)
        (in-room ?b ?rm)
        (free-gripper ?r ?g)
      )
    :effect 
      (and 
        (in-gripper ?r ?g ?b)
        (not (in-room ?b ?rm))
        (not (free-gripper ?r ?g))
      )
  )

  (:action drop
    :parameters 
      (?r - robot ?rm - room ?g - gripper ?b - ball)
    :precondition 
      (and 
        (in-gripper ?r ?g ?b)
        (in-room ?r ?rm)
      )
    :effect 
      (and 
        (in-room ?b ?rm)
        (free-gripper ?r ?g)
        (not (in-gripper ?r ?g ?b))
      )
  )

)