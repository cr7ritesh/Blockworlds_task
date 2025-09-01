begin_version
3
end_version
begin_metric
0
end_metric
5
begin_variable
var0
-1
2
Atom in_room(robot1, room1)
Atom in_room(robot1, room2)
end_variable
begin_variable
var1
-1
4
Atom free_gripper(robot1)
Atom holding(robot1, ball1)
Atom holding(robot1, ball2)
Atom holding(robot1, ball3)
end_variable
begin_variable
var2
-1
3
Atom in_room(ball1, room1)
Atom in_room(ball1, room2)
<none of those>
end_variable
begin_variable
var3
-1
3
Atom in_room(ball2, room1)
Atom in_room(ball2, room2)
<none of those>
end_variable
begin_variable
var4
-1
3
Atom in_room(ball3, room1)
Atom in_room(ball3, room2)
<none of those>
end_variable
3
begin_mutex_group
3
1 1
2 0
2 1
end_mutex_group
begin_mutex_group
3
1 2
3 0
3 1
end_mutex_group
begin_mutex_group
3
1 3
4 0
4 1
end_mutex_group
begin_state
0
0
0
0
0
end_state
begin_goal
3
2 0
3 0
4 1
end_goal
14
begin_operator
drop robot1 ball1 room1
1
0 0
2
0 1 1 0
0 2 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room2
1
0 1
2
0 1 1 0
0 2 -1 1
1
end_operator
begin_operator
drop robot1 ball2 room1
1
0 0
2
0 1 2 0
0 3 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room2
1
0 1
2
0 1 2 0
0 3 -1 1
1
end_operator
begin_operator
drop robot1 ball3 room1
1
0 0
2
0 1 3 0
0 4 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room2
1
0 1
2
0 1 3 0
0 4 -1 1
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
move robot1 room2 room1
0
1
0 0 1 0
1
end_operator
begin_operator
pick robot1 ball1 room1
1
0 0
2
0 1 0 1
0 2 0 2
1
end_operator
begin_operator
pick robot1 ball1 room2
1
0 1
2
0 1 0 1
0 2 1 2
1
end_operator
begin_operator
pick robot1 ball2 room1
1
0 0
2
0 1 0 2
0 3 0 2
1
end_operator
begin_operator
pick robot1 ball2 room2
1
0 1
2
0 1 0 2
0 3 1 2
1
end_operator
begin_operator
pick robot1 ball3 room1
1
0 0
2
0 1 0 3
0 4 0 2
1
end_operator
begin_operator
pick robot1 ball3 room2
1
0 1
2
0 1 0 3
0 4 1 2
1
end_operator
0
