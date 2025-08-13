(defproblem block-problem)

(defobject b1 b2 b3 b4 b5 - block)

(initial
  (ontable b5)
  (on b4 b1)
  (on b1 b2)
  (on b2 b3)
  (on b3 b5)
  (clear b4)
  (armempty))

(goal (and (on b1 b3) (on b3 b5)))