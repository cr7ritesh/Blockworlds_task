(defdomain blockworld)

(defstruct block (on)
  (:print-function (lambda (block) (format nil "BLOCK ~a" (block-on block)))))

(defpred clear ?b - block)
(defpred armempty)
(defpred ontable ?b - block)

(defaction pickup
  :parameters (?b - block)
  :precondition (and (clear ?b) (armempty))
  :effect (and (not (clear ?b)) (not (armempty)) (not (ontable ?b))))

(defaction putdown
  :parameters (?b - block)
  :precondition (not (armempty))
  :effect (and (clear ?b) (armempty) (ontable ?b)))

(defaction stack
  :parameters (?b1 ?b2 - block)
  :precondition (and (not (armempty)) (clear ?b1) (ontable ?b2))
  :effect (and (not (clear ?b1)) (armempty) (not (ontable ?b1)) (on ?b1 ?b2)))

(defaction unstack
  :parameters (?b1 ?b2 - block)
  :precondition (and (armempty) (clear ?b1) (on ?b1 ?b2))
  :effect (and (armempty) (not (clear ?b1)) (ontable ?b1) (not (on ?b1 ?b2))))