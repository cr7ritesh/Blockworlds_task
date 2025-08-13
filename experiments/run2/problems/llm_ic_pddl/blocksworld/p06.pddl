(define (problem BW-new-5)
(:domain blocksworld-new)
(:objects b1 b2 b3 b4 b5)
(:init
(arm-empty)
(on b5 b3)
(on b4 b2)
(on b2 b1)
(on b3 b4)
(on-table b1)
(clear b5)
)
(:goal
(and
(on b1 b2)
(on b3 b5)
(on b4 b1)
)
)