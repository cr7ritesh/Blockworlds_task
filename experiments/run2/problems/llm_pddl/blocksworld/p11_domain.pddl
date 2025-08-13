(defdomain blockworld
:requirements :strips
:types block arm - object
:predicates (on ?b1 - block ?b2 - block)
(clear ?b - block)
(holding ?a - arm ?b - block)
(ontable ?b - block)
(empty ?a - arm)
)

(defmethod pickup ?a ?b
:precondition (and (ontable ?b)
                  (clear ?b)
                  (empty ?a))
:effect (and (not (ontable ?b))
             (not (clear ?b))
             (not (empty ?a))
             (holding ?a ?b)))

(defmethod putdown ?a ?b
:precondition (and (holding ?a ?b))
:effect (and (ontable ?b)
             (clear ?b)
             (empty ?a)
             (not (holding ?a ?b))))

(defmethod stack ?a ?b1 ?b2
:precondition (and (holding ?a ?b1)
                  (on ?b2 ?b1)
                  (clear ?b2))
:effect (and (not (holding ?a ?b1))
             (not (clear ?b2))
             (on ?b1 ?b2)))

(defmethod unstack ?a ?b1 ?b2
:precondition (and (empty ?a)
                  (on ?b1 ?b2)
                  (clear ?b1))
:effect (and (holding ?a ?b1)
             (not (on ?b1 ?b2))
             (clear ?b2)
             (not (clear ?b1))))