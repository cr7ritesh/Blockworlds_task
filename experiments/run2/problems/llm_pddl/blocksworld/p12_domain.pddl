(defdomain blockworld
(:requirements :strips :equality)

(:types block arm - object)

(:predicates
(on ?b1 - block ?b2 - block)
(clear ?b - block)
(ontable ?b - block)
(holding ?a - arm ?b - block))

(:action pickup
:parameters (?a - arm ?b - block)
:precondition (and (ontable ?b) (clear ?b) (not (holding ?a ?b_)))
:effect (and (not (ontable ?b)) (not (clear ?b)) (holding ?a ?b) (not (holding ?a ?b_))))

(:action putdown
:parameters (?a - arm ?b - block)
:precondition (holding ?a ?b)
:effect (and (ontable ?b) (clear ?b) (not (holding ?a ?b))))

(:action stack
:parameters (?a - arm ?b1 ?b2 - block)
:precondition (and (holding ?a ?b1) (on ?b2 ?b1) (clear ?b2))
:effect (and (not (holding ?a ?b1)) (on ?b1 ?b2) (not (clear ?b2))))

(:action unstack
:parameters (?a - arm ?b1 ?b2 - block)
:precondition (and (not (holding ?a ?b1)) (on ?b1 ?b2) (clear ?b1))
:effect (and (holding ?a ?b1) (not (on ?b1 ?b2)) (clear ?b2))))