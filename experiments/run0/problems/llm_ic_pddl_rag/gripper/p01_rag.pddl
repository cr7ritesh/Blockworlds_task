(define (problem two-ball-transport-problem)
 (:domain two-ball-transport)
 (:objects robot1 robot2 - robot
 rgripper1 lgripper1 rgripper2 lgripper2 - gripper
 room1 room2 - room
 ball1 ball2 - object)
 (:init
 (at-robot robot1 room1)
 (free robot1 rgripper1)
 (free robot1 lgripper1)
 (at-robot robot2 room1)
 (free robot2 rgripper2)
 (free robot2 lgripper2)
 (at ball1 room1)
 (at ball2 room1)
 )
 (:goal
 (and
 (at ball1 room1)
 (at ball2 room1)
 )
 )
)