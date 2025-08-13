(define (problem BW-3blocks-problem)
(:domain blocksworld-3blocks)
(:objects b1 b2 b3)
(:init
(arm-empty)
(on b3 b2)
(on b1 b3)
(on-table b2)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b3 b1)
)
)
)