(defproblem block-rearrangement)

(defobject b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)

(initial (on b4 b10) (on b11 b4) (on b5 b8) (on b12 b2) (on b3 b9) (on b1 b12) (on b10 b3) (on b9 b1) (on b7 table) (on b2 table) (on b6 table) (on b8 table) (clear b6) (clear b11) (clear b7) (clear b5) (empty))

(goal (and (on b1 b6) (on b5 b3) (on b6 b2) (on b8 b9) (on b9 b10) (on b10 b1) (on b11 b12) (on b12 b8)))