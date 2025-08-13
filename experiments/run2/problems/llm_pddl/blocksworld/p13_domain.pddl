(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm)
  (:predicates (clear ?x - block)
              (on ?x - block ?y - block)
              (ontable ?x - block)
              (holding ?x - block ?y - arm))
  (:action pickup
    :parameters (?b - block ?a - arm)
    :precondition (and (clear ?b) (ontable ?b) (empty ?a))
    :effect (and (holding ?b ?a) (not (ontable ?b)) (not (clear ?b))))
  (:action putdown
    :parameters (?b - block ?a - arm)
    :precondition (holding ?b ?a)
    :effect (and (ontable ?b) (clear ?b) (empty ?a) (not (holding ?b ?a))))
  (:action stack
    :parameters (?b1 ?b2 - block ?a - arm)
    :precondition (and (holding ?b1 ?a) (clear ?b2) (on ?b2 ?b1))
    :effect (and (on ?b1 ?b2) (empty ?a) (not (holding ?b1 ?a)) (not (clear ?b2))))
  (:action unstack
    :parameters (?b1 ?b2 - block ?a - arm)
    :precondition (and (empty ?a) (clear ?b1) (on ?b1 ?b2))
    :effect (and (holding ?b1 ?a) (clear ?b2) (not (on ?b1 ?b2)) (not (clear ?b1)))))