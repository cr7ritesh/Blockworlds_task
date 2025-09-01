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
      (?r - robot ?room1 ?room2 - room)
    :precondition 
      (and 
        (in-room ?r ?room1)
      )
    :effect 
      (and 
        (in-room ?r ?room2)
        (not (in-room ?r ?room1))
      )
  )

  (:action pick
    :parameters 
      (?r - robot ?b - ball ?room - room)
    :precondition 
      (and 
        (in-room ?r ?room)
        (in-room ?b ?room)
        (free-gripper ?r)
      )
    :effect 
      (and 
        (in-gripper ?r ?b)
        (not (in-room ?b ?room))
        (not (free-gripper ?r))
      )
  )

  (:action drop
    :parameters 
      (?r - robot ?b - ball ?room - room)
    :precondition 
      (and 
        (in-gripper ?r ?b)
        (in-room ?r ?room)
      )
    :effect 
      (and 
        (in-room ?b ?room)
        (free-gripper ?r)
        (not (in-gripper ?r ?b))
      )
  )

)