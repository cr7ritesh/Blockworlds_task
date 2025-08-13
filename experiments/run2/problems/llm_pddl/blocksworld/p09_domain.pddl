(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (on ?b1 - block ?b2 - block)
               (clear ?b - block)
               (holding ?a - arm ?b - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (clear ?b) (not (holding ?a ?b)))
    :effect (and (holding ?a ?b) (not (clear ?b)) (not (holding ?a ?b)))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (not (holding ?a ?b)) (clear ?b))))
  (:action stack
    :parameters (?b1 ?b2 - block)
    :precondition (and (clear ?b1) (not (clear ?b2)) (not (on ?b1 ?b2)))
    :effect (and (on ?b1 ?b2) (not (clear ?b1)))))
  (:action unstack
    :parameters (?b1 ?b2 - block)
    :precondition (and (clear ?b1) (on ?b1 ?b2))
    :effect (and (not (on ?b1 ?b2)) (clear ?b2) (not (clear ?b1))))))