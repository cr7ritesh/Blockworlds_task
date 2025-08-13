(defdomain blockworld
:requirements :strips
:types block arm - object
:predicates (on ?b1 - block ?b2 - block)
(clear ?b - block)
(on-table ?b - block)
(arm-empty)
(arm-holding ?b - block)
:action pickup
:parameters (?b - block)
:precondition (and (clear ?b) (arm-empty) (on-table ?b))
:effect (and (not (clear ?b)) (not (on-table ?b)) (not (arm-empty)) (arm-holding ?b))
)
:action putdown
:parameters (?b - block)
:precondition (arm-holding ?b)
:effect (and (clear ?b) (on-table ?b) (arm-empty) (not (arm-holding ?b)))
)
:action stack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (arm-holding ?b2))
:effect (and (not (clear ?b1)) (not (arm-holding ?b2)) (arm-empty) (on ?b2 ?b1))
)
:action unstack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (on ?b2 ?b1) (arm-empty))
:effect (and (not (clear ?b1)) (arm-holding ?b2) (not (on ?b2 ?b1)) (clear ?b1))
)