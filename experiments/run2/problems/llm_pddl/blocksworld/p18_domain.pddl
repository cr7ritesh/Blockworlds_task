(defdomain blockworld)

(defstruct block (clear)
  (:print-function (lambda (block) (format nil "b~a" (block-clear block)))))

(defpred clear ?b - block)
(defpred on ?b1 ?b2 - block)

(defmethod (hold) ()
  (and (exists (?b - block) (not (clear ?b)))))

(defmethod (table ?b - block) ()
  (and (clear ?b) (not (hold))))

(defmethod (pickup ?b - block) (hold)
  (and (clear ?b) (not (hold)) (not (on ?b ?b2))))

(defmethod (putdown ?b - block) (not(hold))
  (and (not (clear ?b)) (hold) (not (on ?b ?b2)))))

(defmethod (stack ?b1 ?b2 - block) (and (hold) (clear ?b1) (on ?b2 ?b1))
  (and (not (hold)) (not (clear ?b1)) (on ?b2 ?b1) (not (on ?b1 ?b3)))))

(defmethod (unstack ?b1 ?b2 - block) (and (not(hold)) (clear ?b1) (on ?b2 ?b1))
  (and (hold) (clear ?b2) (not (on ?b2 ?b1)) (not (on ?b1 ?b3)))))