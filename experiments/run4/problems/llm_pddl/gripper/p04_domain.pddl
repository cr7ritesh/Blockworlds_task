(define (domain robot_transport)

  (:requirements :strips :equality :typing)

  (:types 
    robot room ball

  )

  (:predicates 
    (in-room robot room)
    (in-robot ball robot)
    (in-room-robot-free robot room)
    (in-room-ball ball room)
    (in-room-gripper-free robot room)

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
        (in-room-ball ?b ?room)
        (in-room-robot-free ?r ?room)
        (in-room-gripper-free ?r ?room)
      )
    :effect 
      (and 
        (in-robot ?b ?r)
        (not (in-room-ball ?b ?room))
        (not (in-room-gripper-free ?r ?room))
      )
  )

  (:action drop
    :parameters 
      (?r - robot ?b - ball ?room - room)
    :precondition 
      (and 
        (in-robot ?b ?r)
        (in-room ?r ?room)
      )
    :effect 
      (and 
        (in-room-ball ?b ?room)
        (in-room-gripper-free ?r ?room)
        (not (in-robot ?b ?r))
      )
  )

)