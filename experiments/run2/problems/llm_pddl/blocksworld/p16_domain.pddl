(defdomain blockworld
:requirements :strips
:types block arm - object
:predicates (on ?b1 ?b2)
(clear ?b)
(holding ?a ?b)
(ontable ?b)
:action pickup
:parameters (?a - arm ?b - block)
:precondition (and (clear ?b) (ontable ?b) (not (holding ?a ?b)))
:effect (and (not (ontable ?b)) (not (clear ?b)) (holding ?a ?b))
)
:action putdown
:parameters (?a - arm ?b - block)
:precondition (holding ?a ?b)
:effect (and (ontable ?b) (clear ?b) (not (holding ?a ?b)))
)
:action stack
:parameters (?b1 ?b2 - block ?a - arm)
:precondition (and (holding ?a ?b1) (clear ?b2) (on ?b2 ?b1))
:effect (and (not (holding ?a ?b1)) (not (clear ?b2)) (on ?b1 ?b2))
)
:action unstack
:parameters (?b1 ?b2 - block ?a - arm)
:precondition (and (clear ?b1) (on ?b1 ?b2) (not (holding ?a ?b1)))
:effect (and (holding ?a ?b1) (clear ?b2) (not (on ?b1 ?b2))))