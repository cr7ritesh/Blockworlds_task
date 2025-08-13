(defproblem block-rearrangement
(:domain blockworld)

(:objects
b1 b2 b3 b4 b5 b6 b7 b8
arm
-
block
)

(:initial-state
(on b7 b8)
(on b8 b1)
(on b1 b6)
(on b6 b4)
(ontable b4)
(ontable b2)
(ontable b3)
(ontable b5)
(clear b7)
(clear b5)
(clear b2)
(clear b3)
(holding arm -)
)

(:goal (and
(on b1 b3)
(on b2 b8)
(on b3 b2)
(on b4 b7)
(on b5 b6)
(on b6 b4)
(on b7 b1)
))