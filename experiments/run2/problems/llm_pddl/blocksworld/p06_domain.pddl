(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (on ?b1 - block ?b2 - block)
               (clear ?b - block)
               (holding ?a - arm ?b - block)
               (ontable ?b - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (ontable ?b) (clear ?b) (not (holding ?a ?b)))
    :effect (and (holding ?a ?b) (not (ontable ?b)) (not (clear ?b)) (not (holding ?a ?b)))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (ontable ?b) (clear ?b) (not (holding ?a ?b)))))
  (:action stack
    :parameters (?b1 ?b2 - block)
    :precondition (and (clear ?b1) (holding ?arm ?b2) (not (on ?b1 ?b2)))
    :effect (and (on ?b1 ?b2) (not (clear ?b1)) (not (holding ?arm ?b2)))))
  (:action unstack
    :parameters (?b1 ?b2 - block)
    :precondition (and (on ?b1 ?b2) (clear ?b1) (not (holding ?arm)))
    :effect (and (holding ?arm ?b2) (not (on ?b1 ?b2)) (clear ?b1) (not (holding ?arm ?b2)))))