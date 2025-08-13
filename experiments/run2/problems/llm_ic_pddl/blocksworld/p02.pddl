(define (problem BW-3blocks)
(:domain blocksworld-3ops)
(:objects b1 b2 b3)
(:init
(arm-empty)
(on b1 b3)
(on b3 b2)
(on-table b2)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b3 b1))
)
)