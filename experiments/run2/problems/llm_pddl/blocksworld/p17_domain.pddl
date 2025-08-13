(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (on ?b1 - block ?b2 - block)
              (clear ?b - block)
              (ontable ?b - block)
              (emptyarm))
  (:functions (total-cost))
  (:action pickup
    :parameters (?b - block)
    :precondition (and (ontable ?b) (emptyarm) (clear ?b))
    :effect (and (not (ontable ?b)) (not (emptyarm)) (not (clear ?b))))
  (:action putdown
    :parameters (?b - block)
    :precondition (not (emptyarm))
    :effect (and (ontable ?b) (emptyarm) (clear ?b)))
  (:action stack
    :parameters (?b1 ?b2 - block)
    :precondition (and (on ?b2 ?b1) (clear ?b1) (not (emptyarm)) (holding ?b2))
    :effect (and (not (on ?b2 ?b1)) (not (clear ?b1)) (emptyarm) (holding ?b1)))
  (:action unstack
    :parameters (?b1 ?b2 - block)
    :precondition (and (on ?b1 ?b2) (clear ?b2) (emptyarm))
    :effect (and (not (on ?b1 ?b2)) (not (emptyarm)) (holding ?b2) (clear ?b1))))