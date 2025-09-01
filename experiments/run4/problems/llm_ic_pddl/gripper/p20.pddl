(define (problem four-robots-two-balls)
(:domain multi-gripper-transport)
(:objects robot1 robot2 robot3 robot4 - robot
rgripper1 lgripper1 rgripper2 lgripper2 rgripper3 lgripper3 rgripper4 lgripper4 - gripper
room1 room2 room3 - room
ball1 ball2 - ball)
(:init
(at-robot robot1 room1)
(free robot1 rgripper1)
(free robot1 lgripper1)
(at-robot robot2 room1)
(free robot2 rgripper2)
(free robot2 lgripper2)
(at-robot robot3 room1)
(free robot3 rgripper3)
(free robot3 lgripper3)
(at-robot robot4 room1)
(free robot4 rgripper4)
(free robot4 lgripper4)
(at ball1 room2)
(at ball2 room3)
)
(:goal
(and
(at ball1 room2)
(at ball2 room3)
)
)
)