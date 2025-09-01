(define (domain gripper-planning)
    (:requirements :strips :typing) 
    (:types room object robot gripper)
    (:predicates (at-robot ?r - robot ?x - room)
                (at ?o - object ?x - room)
                (free ?r - robot ?g - gripper)
                (carry ?r - robot ?o - object ?g - gripper))

    (:action move
        :parameters (?r - robot ?from ?to - room)
        :precondition (and (at-robot ?r ?from))
        :effect (and (at-robot ?r ?to)
                     (not (at-robot ?r ?from))))

    (:action pick
        :parameters (?r - robot ?obj - object ?room - room ?g - gripper)
        :precondition (and (at ?obj ?room) (at-robot ?r ?room) (free ?r ?g))
        :effect (and (carry ?r ?obj ?g)
                     (not (at ?obj ?room)) 
                     (not (free ?r ?g))))

    (:action drop
        :parameters (?r - robot ?obj - object ?room - room ?g - gripper)
        :precondition (and (carry ?r ?obj ?g) (at-robot ?r ?room))
        :effect (and (at ?obj ?room)
                     (free ?r ?g)
                     (not (carry ?r ?obj ?g))))
)