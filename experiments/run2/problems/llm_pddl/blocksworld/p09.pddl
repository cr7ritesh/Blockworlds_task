(defproblem block-rearrangement
:domain blockworld
:objects
b1 b2 b3 b4 b5 b6 b7 arm table
:initial-state
(on b4 b7)
(on b3 b6)
(on b7 b3)
(on b2 table)
(on b6 table)
(on b1 table)
(on b5 table)
(clear b1)
(clear b5)
(clear b2)
(clear b4)
(holding arm nil)
:goal
(and (on b1 b2)
(on b2 b6)
(on b3 b7)
(on b5 b3)
(on b6 b5)
(on b7 b4)))