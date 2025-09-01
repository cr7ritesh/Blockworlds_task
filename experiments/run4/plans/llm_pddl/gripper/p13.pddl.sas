begin_version
3
end_version
begin_metric
0
end_metric
4
begin_variable
var0
-1
3
Atom in_room(robot1, room1)
Atom in_room(robot1, room2)
Atom in_room(robot1, room3)
end_variable
begin_variable
var1
-1
2
Atom free_gripper(robot1)
NegatedAtom free_gripper(robot1)
end_variable
begin_variable
var2
-1
4
Atom in_gripper(robot1, ball1)
Atom in_room_ball(ball1, room1)
Atom in_room_ball(ball1, room2)
Atom in_room_ball(ball1, room3)
end_variable
begin_variable
var3
-1
4
Atom in_gripper(robot1, ball2)
Atom in_room_ball(ball2, room1)
Atom in_room_ball(ball2, room2)
Atom in_room_ball(ball2, room3)
end_variable
1
begin_mutex_group
3
1 0
2 0
3 0
end_mutex_group
begin_state
0
0
3
3
end_state
begin_goal
2
2 1
3 1
end_goal
18
begin_operator
drop robot1 ball1 room1
1
0 0
2
0 1 -1 0
0 2 0 1
1
end_operator
begin_operator
drop robot1 ball1 room2
1
0 1
2
0 1 -1 0
0 2 0 2
1
end_operator
begin_operator
drop robot1 ball1 room3
1
0 2
2
0 1 -1 0
0 2 0 3
1
end_operator
begin_operator
drop robot1 ball2 room1
1
0 0
2
0 1 -1 0
0 3 0 1
1
end_operator
begin_operator
drop robot1 ball2 room2
1
0 1
2
0 1 -1 0
0 3 0 2
1
end_operator
begin_operator
drop robot1 ball2 room3
1
0 2
2
0 1 -1 0
0 3 0 3
1
end_operator
begin_operator
move robot1 room1 room2
0
1
0 0 0 1
1
end_operator
begin_operator
move robot1 room1 room3
0
1
0 0 0 2
1
end_operator
begin_operator
move robot1 room2 room1
0
1
0 0 1 0
1
end_operator
begin_operator
move robot1 room2 room3
0
1
0 0 1 2
1
end_operator
begin_operator
move robot1 room3 room1
0
1
0 0 2 0
1
end_operator
begin_operator
move robot1 room3 room2
0
1
0 0 2 1
1
end_operator
begin_operator
pick robot1 ball1 room1
1
0 0
2
0 1 0 1
0 2 1 0
1
end_operator
begin_operator
pick robot1 ball1 room2
1
0 1
2
0 1 0 1
0 2 2 0
1
end_operator
begin_operator
pick robot1 ball1 room3
1
0 2
2
0 1 0 1
0 2 3 0
1
end_operator
begin_operator
pick robot1 ball2 room1
1
0 0
2
0 1 0 1
0 3 1 0
1
end_operator
begin_operator
pick robot1 ball2 room2
1
0 1
2
0 1 0 1
0 3 2 0
1
end_operator
begin_operator
pick robot1 ball2 room3
1
0 2
2
0 1 0 1
0 3 3 0
1
end_operator
0
