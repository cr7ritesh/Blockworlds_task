(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm - object)
  (:predicates (on ?b1 - block ?b2 - block)
               (clear ?b - block)
               (holding ?a - arm ?b - block)
               (ontable ?b - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (ontable ?b) (clear ?b) (not (holding ?a ?b)))
    :effect (and (holding ?a ?b) (not (ontable ?b)) (not (clear ?b)) (not (holding ?a ?b))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (ontable ?b) (clear ?b) (not (holding ?a ?b))))
  (:action stack
    :parameters (?a - arm ?b1 ?b2 - block)
    :precondition (and (holding ?a ?b1) (on ?b2 ?b1) (clear ?b2) (not (holding ?a ?b2)))
    :effect (and (on ?b1 ?b2) (not (clear ?b2)) (not (holding ?a ?b1))))
  (:action unstack
    :parameters (?a - arm ?b1 ?b2 - block)
    :precondition (and (not (holding ?a ?b1)))
    :effect (and (holding ?a ?b1) (clear ?b1) (not (on ?b1 ?b2)))))