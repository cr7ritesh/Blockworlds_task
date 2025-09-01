(define (domain multi-gripper-transport)
  (:requirements :strips :typing) 
  (:types robot room gripper ball)
  (:predicates (at-robot ?r - robot ?x - room)
	      (at ?b - ball ?x - room)
	      (free ?r - robot ?g - gripper)
	      (carry ?r - robot ?b - ball ?g - gripper))

  (:action move
      :parameters  (?r - robot ?from ?to - room)
      :precondition (and  (at-robot ?r ?from))
      :effect (and  (at-robot ?r ?to)
		    (not (at-robot ?r ?from))))

  (:action pick
      :parameters (?r - robot ?b - ball ?room - room ?g - gripper)
      :precondition  (and  (at ?b ?room) (at-robot ?r ?room) (free ?r ?g))
      :effect (and (carry ?r ?b ?g)
		   (not (at ?b ?room)) 
		   (not (free ?r ?g))))

  (:action drop
      :parameters (?r - robot ?b - ball ?room - room ?g - gripper)
      :precondition  (and  (carry ?r ?b ?g) (at-robot ?r ?room))
      :effect (and (at ?b ?room)
		   (free ?r ?g)
		   (not (carry ?r ?b ?g)))))