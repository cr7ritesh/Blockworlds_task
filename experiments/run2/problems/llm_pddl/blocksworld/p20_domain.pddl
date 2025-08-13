(defdomain blockworld)

(defstruct block (on))

(defrole arm
  :initial (empty)
  :either (empty holding)
  :inverse (holding arm))

(defrole table
  :types block
  :initial (clear not-clear)
  :either (clear not-clear)
  :inverse (on table))

(defrole on
  :types block
  :inverse (on block))

(defaction pickup
  :parameters (?b - block)
  :precondition (and (clear ?b) (empty))
  :effect (and (not (clear ?b)) (not (empty)) (holding ?b) (not (on ?b table))))

(defaction putdown
  :parameters (?b - block)
  :precondition (holding ?b)
  :effect (and (empty) (not (holding ?b)) (clear ?b) (on ?b table)))

(defaction stack
  :parameters (?b1 ?b2 - block)
  :precondition (and (holding ?b1) (clear ?b2) (on ?b2 table))
  :effect (and (empty) (not (holding ?b1)) (not (clear ?b2)) (on ?b1 ?b2) (not (on ?b2 table))))

(defaction unstack
  :parameters (?b1 ?b2 - block)
  :precondition (and (empty) (clear ?b1) (on ?b1 ?b2))
  :effect (and (holding ?b1) (clear ?b2) (on ?b2 table) (not (on ?b1 ?b2)) (not (clear ?b1))))