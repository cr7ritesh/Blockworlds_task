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
5
Atom in(robot1, room1)
Atom in(robot1, room2)
Atom in(robot1, room3)
Atom in(robot1, room4)
Atom in(robot1, room5)
end_variable
begin_variable
var1
-1
2
Atom handfree(robot1)
NegatedAtom handfree(robot1)
end_variable
begin_variable
var2
-1
6
Atom carrying(robot1, ball1)
Atom in(ball1, room1)
Atom in(ball1, room2)
Atom in(ball1, room3)
Atom in(ball1, room4)
Atom in(ball1, room5)
end_variable
begin_variable
var3
-1
6
Atom carrying(robot1, ball2)
Atom in(ball2, room1)
Atom in(ball2, room2)
Atom in(ball2, room3)
Atom in(ball2, room4)
Atom in(ball2, room5)
end_variable
begin_variable
var4
-1
6
Atom carrying(robot1, ball3)
Atom in(ball3, room1)
Atom in(ball3, room2)
Atom in(ball3, room3)
Atom in(ball3, room4)
Atom in(ball3, room5)
end_variable
1
begin_mutex_group
4
2 0
3 0
4 0
1 0
end_mutex_group
begin_state
3
0
3
5
3
end_state
begin_goal
3
2 5
3 2
4 1
end_goal
50
begin_operator
drop robot1 ball1 room1
1
0 0
2
0 2 0 1
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room2
1
0 1
2
0 2 0 2
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room3
1
0 2
2
0 2 0 3
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room4
1
0 3
2
0 2 0 4
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball1 room5
1
0 4
2
0 2 0 5
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room1
1
0 0
2
0 3 0 1
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room2
1
0 1
2
0 3 0 2
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room3
1
0 2
2
0 3 0 3
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room4
1
0 3
2
0 3 0 4
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball2 room5
1
0 4
2
0 3 0 5
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room1
1
0 0
2
0 4 0 1
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room2
1
0 1
2
0 4 0 2
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room3
1
0 2
2
0 4 0 3
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room4
1
0 3
2
0 4 0 4
0 1 -1 0
1
end_operator
begin_operator
drop robot1 ball3 room5
1
0 4
2
0 4 0 5
0 1 -1 0
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
move robot1 room1 room5
0
1
0 0 0 4
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
move robot1 room2 room5
0
1
0 0 1 4
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
move robot1 room3 room5
0
1
0 0 2 4
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
move robot1 room4 room5
0
1
0 0 3 4
1
end_operator
begin_operator
move robot1 room5 room1
0
1
0 0 4 0
1
end_operator
begin_operator
move robot1 room5 room2
0
1
0 0 4 1
1
end_operator
begin_operator
move robot1 room5 room3
0
1
0 0 4 2
1
end_operator
begin_operator
move robot1 room5 room4
0
1
0 0 4 3
1
end_operator
begin_operator
pick robot1 ball1 room1
1
0 0
2
0 2 1 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball1 room2
1
0 1
2
0 2 2 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball1 room3
1
0 2
2
0 2 3 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball1 room4
1
0 3
2
0 2 4 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball1 room5
1
0 4
2
0 2 5 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball2 room1
1
0 0
2
0 3 1 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball2 room2
1
0 1
2
0 3 2 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball2 room3
1
0 2
2
0 3 3 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball2 room4
1
0 3
2
0 3 4 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball2 room5
1
0 4
2
0 3 5 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball3 room1
1
0 0
2
0 4 1 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball3 room2
1
0 1
2
0 4 2 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball3 room3
1
0 2
2
0 4 3 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball3 room4
1
0 3
2
0 4 4 0
0 1 0 1
1
end_operator
begin_operator
pick robot1 ball3 room5
1
0 4
2
0 4 5 0
0 1 0 1
1
end_operator
0
