(defdomain blockworld)

(declare (action pickup putdown stack unstack))

(declare (obj types block arm table))

(defobjtype block (aspects on clear))

(defobjtype arm (aspects holding))

(defobjtype table (aspects on))

(defaspect on
(parameters ?b - block ?x block table))

(defaspect clear
(parameters ?b - block)
(exclusive with on))

(defaspect holding
(parameters ?b - block)
(exclusive with on))

(defaction pickup
:parameters (?a - arm ?b - block)
:precondition (and (on ?b table) (clear ?b) (not (holding ?a ?b)))
:effect (and (not (on ?b table)) (not (clear ?b)) (holding ?a ?b)))

(defaction putdown
:parameters (?a - arm ?b - block)
:precondition (and (holding ?a ?b) (clear ?b))
:effect (and (on ?b table) (clear ?b) (not (holding ?a ?b))))

(defaction stack
:parameters (?a - arm ?b ?c - block)
:precondition (and (on ?c table) (clear ?c) (holding ?a ?b))
:effect (and (not (on ?c table)) (not (clear ?c)) (on ?b ?c) (not (holding ?a ?b))))

(defaction unstack
:parameters (?a - arm ?b ?c - block)
:precondition (and (on ?b ?c) (clear ?b) (not (holding ?a ?b)))
:effect (and (holding ?a ?b) (clear ?c) (not (on ?b ?c))))