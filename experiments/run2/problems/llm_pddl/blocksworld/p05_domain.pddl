(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (on ?b1 - block ?b2 - block)
               (clear ?b - block)
               (ontable ?b - block)
               (holding ?a - arm ?b - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (ontable ?b) (clear ?b) (not (holding ?a ?b)))
    :effect (and (holding ?a ?b) (not (ontable ?b)) (not (clear ?b)) (not (holding ?a ?c)))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (ontable ?b) (clear ?b) (not (holding ?a ?b))))
  (:action stack
    :parameters (?b1 ?b2 - block)
    :precondition (and (holding ?a ?b1) (clear ?b2) (on ?x ?b2))
    :effect (and (on ?b1 ?b2) (not (clear ?b2)) (not (holding ?a ?b1))))
  (:action unstack
    :parameters (?b1 ?b2 - block)
    :precondition (and (clear ?b1) (on ?b1 ?b2))
    :effect (and (holding ?a ?b1) (clear ?b2) (not (on ?b1 ?b2)))))