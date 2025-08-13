(defdomain blockworld
:requirements :strips
:types block arm - object
:predicates (on ?b1 - block ?b2 - block)
(clear ?b - block)
(on-table ?b - block)
(arm-empty)
(holding ?b - block)
:action pickup
:parameters (?b - block)
:precondition (and (clear ?b) (arm-empty) (on-table ?b))
:effect (and (not (clear ?b)) (not (on-table ?b)) (not (arm-empty)) (holding ?b))
)
:action putdown
:parameters (?b - block)
:precondition (holding ?b)
:effect (and (clear ?b) (on-table ?b) (arm-empty) (not (holding ?b)))
)
:action stack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (holding ?b2))
:effect (and (not (clear ?b1)) (not (holding ?b2)) (on ?b2 ?b1))
)
:action unstack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (on ?b2 ?b1) (arm-empty))
:effect (and (not (on ?b2 ?b1)) (not (clear ?b1)) (holding ?b2) (arm-empty))
)