(defdomain blockworld
:requirements :strips
:types block arm - object
:predicates (on ?b1 - block ?b2 - block)
(clear ?b - block)
(armempty)
(armhold ?b - block)
:action pickup
:parameters (?b - block)
:precondition (and (clear ?b) (armempty))
:effect (and (not (clear ?b)) (not (armempty)) (armhold ?b))
)
:action putdown
:parameters (?b - block)
:precondition (armhold ?b)
:effect (and (clear ?b) (armempty) (not (armhold ?b))
)
:action stack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (armhold ?b2))
:effect (and (on ?b2 ?b1) (not (clear ?b1)) (armempty) (not (armhold ?b2))
)
:action unstack
:parameters (?b1 ?b2 - block)
:precondition (and (clear ?b1) (on ?b2 ?b1) (armempty))
:effect (and (armhold ?b2) (not (on ?b2 ?b1)) (clear ?b1) (not (armempty))
)