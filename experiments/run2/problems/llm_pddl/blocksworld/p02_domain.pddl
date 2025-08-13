(define (domain block-world)
  (:requirements :strips :equality)
  (:types block arm - object)
  (:predicates (clear ?x - block)
               (on ?x - block ?y - block)
               (holding ?x - arm ?y - block))
  (:action pickup
    :parameters (?a - arm ?b - block)
    :precondition (and (clear ?b) (not (holding ?a ?_)))
    :effect (and (holding ?a ?b) (not (clear ?b)) (not (holding ?a ?_))))
  (:action putdown
    :parameters (?a - arm ?b - block)
    :precondition (holding ?a ?b)
    :effect (and (clear ?b) (not (holding ?a ?b)) (not (holding ?a ?_))))
  (:action stack
    :parameters (?a - arm ?x - block ?y - block)
    :precondition (and (holding ?a ?x) (clear ?y))
    :effect (and (on ?x ?y) (not (holding ?a ?x)) (not (clear ?y)) (not (holding ?a ?_)))))
  (:action unstack
    :parameters (?a - arm ?x - block ?y - block)
    :precondition (and (on ?x ?y) (clear ?a))
    :effect (and (holding ?a ?x) (not (on ?x ?y)) (clear ?y) (not (holding ?a ?_)))))