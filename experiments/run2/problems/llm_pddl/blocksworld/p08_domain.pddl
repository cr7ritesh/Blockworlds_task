(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (on ?b1 - block ?b2 - block)
               (clear ?b - block)
               (holding ?a - arm ?b - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (clear ?b) (not (holding ?a ?_)))
    :effect (and (holding ?a ?b) (not (clear ?b)) (not (holding ?a ?_))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (not (holding ?a ?b)) (clear ?b)))
  (:action stack
    :parameters (?a - arm ?b1 ?b2 - block)
    :precondition (and (holding ?a ?b1) (clear ?b2))
    :effect (and (on ?b1 ?b2) (not (holding ?a ?b1)) (not (clear ?b2))))
  (:action unstack
    :parameters (?a - arm ?b1 ?b2 - block)
    :precondition (and (on ?b1 ?b2) (clear ?a))
    :effect (and (holding ?a ?b1) (clear ?b2) (not (on ?b1 ?b2)))))