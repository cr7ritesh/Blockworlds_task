begin_version
3
end_version
begin_metric
0
end_metric
7
begin_variable
var0
-1
4
Atom robot_in_room(robot1, room1)
Atom robot_in_room(robot1, room2)
Atom robot_in_room(robot1, room3)
Atom robot_in_room(robot1, room4)
end_variable
begin_variable
var1
-1
6
Atom carrying(robot1, ball1)
Atom carrying(robot1, ball2)
Atom carrying(robot1, ball3)
Atom carrying(robot1, ball4)
Atom carrying(robot1, ball5)
Atom gripper_free(robot1)
end_variable
begin_variable
var2
-1
5
Atom in_room(ball1, room1)
Atom in_room(ball1, room2)
Atom in_room(ball1, room3)
Atom in_room(ball1, room4)
<none of those>
end_variable
begin_variable
var3
-1
5
Atom in_room(ball2, room1)
Atom in_room(ball2, room2)
Atom in_room(ball2, room3)
Atom in_room(ball2, room4)
<none of those>
end_variable
begin_variable
var4
-1
5
Atom in_room(ball3, room1)
Atom in_room(ball3, room2)
Atom in_room(ball3, room3)
Atom in_room(ball3, room4)
<none of those>
end_variable
begin_variable
var5
-1
5
Atom in_room(ball4, room1)
Atom in_room(ball4, room2)
Atom in_room(ball4, room3)
Atom in_room(ball4, room4)
<none of those>
end_variable
begin_variable
var6
-1
5
Atom in_room(ball5, room1)
Atom in_room(ball5, room2)
Atom in_room(ball5, room3)
Atom in_room(ball5, room4)
<none of those>
end_variable
5
begin_mutex_group
5
1 0
2 0
2 1
2 2
2 3
end_mutex_group
begin_mutex_group
5
1 1
3 0
3 1
3 2
3 3
end_mutex_group
begin_mutex_group
5
1 2
4 0
4 1
4 2
4 3
end_mutex_group
begin_mutex_group
5
1 3
5 0
5 1
5 2
5 3
end_mutex_group
begin_mutex_group
5
1 4
6 0
6 1
6 2
6 3
end_mutex_group
begin_state
1
5
1
0
0
2
1
end_state
begin_goal
5
2 1
3 3
4 3
5 2
6 1
end_goal
52
begin_operator
drop robot1 ball1 room1
1
0 0
2
0 1 0 5
0 2 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room2
1
0 1
2
0 1 0 5
0 2 -1 1
1
end_operator
begin_operator
drop robot1 ball1 room3
1
0 2
2
0 1 0 5
0 2 -1 2
1
end_operator
begin_operator
drop robot1 ball1 room4
1
0 3
2
0 1 0 5
0 2 -1 3
1
end_operator
begin_operator
drop robot1 ball2 room1
1
0 0
2
0 1 1 5
0 3 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room2
1
0 1
2
0 1 1 5
0 3 -1 1
1
end_operator
begin_operator
drop robot1 ball2 room3
1
0 2
2
0 1 1 5
0 3 -1 2
1
end_operator
begin_operator
drop robot1 ball2 room4
1
0 3
2
0 1 1 5
0 3 -1 3
1
end_operator
begin_operator
drop robot1 ball3 room1
1
0 0
2
0 1 2 5
0 4 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room2
1
0 1
2
0 1 2 5
0 4 -1 1
1
end_operator
begin_operator
drop robot1 ball3 room3
1
0 2
2
0 1 2 5
0 4 -1 2
1
end_operator
begin_operator
drop robot1 ball3 room4
1
0 3
2
0 1 2 5
0 4 -1 3
1
end_operator
begin_operator
drop robot1 ball4 room1
1
0 0
2
0 1 3 5
0 5 -1 0
1
end_operator
begin_operator
drop robot1 ball4 room2
1
0 1
2
0 1 3 5
0 5 -1 1
1
end_operator
begin_operator
drop robot1 ball4 room3
1
0 2
2
0 1 3 5
0 5 -1 2
1
end_operator
begin_operator
drop robot1 ball4 room4
1
0 3
2
0 1 3 5
0 5 -1 3
1
end_operator
begin_operator
drop robot1 ball5 room1
1
0 0
2
0 1 4 5
0 6 -1 0
1
end_operator
begin_operator
drop robot1 ball5 room2
1
0 1
2
0 1 4 5
0 6 -1 1
1
end_operator
begin_operator
drop robot1 ball5 room3
1
0 2
2
0 1 4 5
0 6 -1 2
1
end_operator
begin_operator
drop robot1 ball5 room4
1
0 3
2
0 1 4 5
0 6 -1 3
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
move robot1 room1 room4
0
1
0 0 0 3
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
move robot1 room2 room4
0
1
0 0 1 3
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
move robot1 room3 room4
0
1
0 0 2 3
1
end_operator
begin_operator
move robot1 room4 room1
0
1
0 0 3 0
1
end_operator
begin_operator
move robot1 room4 room2
0
1
0 0 3 1
1
end_operator
begin_operator
move robot1 room4 room3
0
1
0 0 3 2
1
end_operator
begin_operator
pick robot1 ball1 room1
1
0 0
2
0 1 5 0
0 2 0 4
1
end_operator
begin_operator
pick robot1 ball1 room2
1
0 1
2
0 1 5 0
0 2 1 4
1
end_operator
begin_operator
pick robot1 ball1 room3
1
0 2
2
0 1 5 0
0 2 2 4
1
end_operator
begin_operator
pick robot1 ball1 room4
1
0 3
2
0 1 5 0
0 2 3 4
1
end_operator
begin_operator
pick robot1 ball2 room1
1
0 0
2
0 1 5 1
0 3 0 4
1
end_operator
begin_operator
pick robot1 ball2 room2
1
0 1
2
0 1 5 1
0 3 1 4
1
end_operator
begin_operator
pick robot1 ball2 room3
1
0 2
2
0 1 5 1
0 3 2 4
1
end_operator
begin_operator
pick robot1 ball2 room4
1
0 3
2
0 1 5 1
0 3 3 4
1
end_operator
begin_operator
pick robot1 ball3 room1
1
0 0
2
0 1 5 2
0 4 0 4
1
end_operator
begin_operator
pick robot1 ball3 room2
1
0 1
2
0 1 5 2
0 4 1 4
1
end_operator
begin_operator
pick robot1 ball3 room3
1
0 2
2
0 1 5 2
0 4 2 4
1
end_operator
begin_operator
pick robot1 ball3 room4
1
0 3
2
0 1 5 2
0 4 3 4
1
end_operator
begin_operator
pick robot1 ball4 room1
1
0 0
2
0 1 5 3
0 5 0 4
1
end_operator
begin_operator
pick robot1 ball4 room2
1
0 1
2
0 1 5 3
0 5 1 4
1
end_operator
begin_operator
pick robot1 ball4 room3
1
0 2
2
0 1 5 3
0 5 2 4
1
end_operator
begin_operator
pick robot1 ball4 room4
1
0 3
2
0 1 5 3
0 5 3 4
1
end_operator
begin_operator
pick robot1 ball5 room1
1
0 0
2
0 1 5 4
0 6 0 4
1
end_operator
begin_operator
pick robot1 ball5 room2
1
0 1
2
0 1 5 4
0 6 1 4
1
end_operator
begin_operator
pick robot1 ball5 room3
1
0 2
2
0 1 5 4
0 6 2 4
1
end_operator
begin_operator
pick robot1 ball5 room4
1
0 3
2
0 1 5 4
0 6 3 4
1
end_operator
0
