(defproblem block-rearrangement
:domain blockworld
:objects b1 b2 b3 b4 b5 b6 b7 b8 - block
          arm1 - arm
:init (on b7 b5)
       (on b4 b2)
       (on b8 b3)
       (on b3 b7)
       (on b2 b1)
       (on b6 b4)
       (on b5 b6)
       (ontable b1)
       (clear b8)
       (empty arm1)
:goal (and (on b1 b8)
           (on b2 b3)
           (on b3 b5)
           (on b4 b2)
           (on b8 b7))