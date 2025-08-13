begin_version
3
end_version
begin_metric
0
end_metric
15
begin_variable
var0
-1
2
Atom on(b3, b2)
NegatedAtom on(b3, b2)
end_variable
begin_variable
var1
-1
2
Atom on(b3, b3)
NegatedAtom on(b3, b3)
end_variable
begin_variable
var2
-1
2
Atom on(b1, b3)
NegatedAtom on(b1, b3)
end_variable
begin_variable
var3
-1
2
Atom on(b2, b1)
NegatedAtom on(b2, b1)
end_variable
begin_variable
var4
-1
2
Atom on(b2, b2)
NegatedAtom on(b2, b2)
end_variable
begin_variable
var5
-1
2
Atom on(b1, b2)
NegatedAtom on(b1, b2)
end_variable
begin_variable
var6
-1
2
Atom on(b1, b1)
NegatedAtom on(b1, b1)
end_variable
begin_variable
var7
-1
2
Atom holding(arm1, b1)
NegatedAtom holding(arm1, b1)
end_variable
begin_variable
var8
-1
2
Atom clear(b1)
NegatedAtom clear(b1)
end_variable
begin_variable
var9
-1
2
Atom clear(b2)
NegatedAtom clear(b2)
end_variable
begin_variable
var10
-1
2
Atom holding(arm1, b2)
NegatedAtom holding(arm1, b2)
end_variable
begin_variable
var11
-1
2
Atom holding(arm1, b3)
NegatedAtom holding(arm1, b3)
end_variable
begin_variable
var12
-1
2
Atom clear(b3)
NegatedAtom clear(b3)
end_variable
begin_variable
var13
-1
2
Atom on(b3, b1)
NegatedAtom on(b3, b1)
end_variable
begin_variable
var14
-1
2
Atom on(b2, b3)
NegatedAtom on(b2, b3)
end_variable
0
begin_state
1
1
1
1
1
1
1
1
1
0
1
1
1
0
0
end_state
begin_goal
2
13 0
14 0
end_goal
24
begin_operator
pickup arm1 b1
0
2
0 8 0 1
0 7 1 0
1
end_operator
begin_operator
pickup arm1 b2
0
2
0 9 0 1
0 10 1 0
1
end_operator
begin_operator
pickup arm1 b3
0
2
0 12 0 1
0 11 1 0
1
end_operator
begin_operator
putdown arm1 b1
0
2
0 8 -1 0
0 7 0 1
1
end_operator
begin_operator
putdown arm1 b2
0
2
0 9 -1 0
0 10 0 1
1
end_operator
begin_operator
putdown arm1 b3
0
2
0 12 -1 0
0 11 0 1
1
end_operator
begin_operator
stack arm1 b1 b1
0
3
0 8 0 1
0 7 0 1
0 6 -1 0
1
end_operator
begin_operator
stack arm1 b1 b2
0
3
0 9 0 1
0 7 0 1
0 5 -1 0
1
end_operator
begin_operator
stack arm1 b1 b3
0
3
0 12 0 1
0 7 0 1
0 2 -1 0
1
end_operator
begin_operator
stack arm1 b2 b1
0
3
0 8 0 1
0 10 0 1
0 3 -1 0
1
end_operator
begin_operator
stack arm1 b2 b2
0
3
0 9 0 1
0 10 0 1
0 4 -1 0
1
end_operator
begin_operator
stack arm1 b2 b3
0
3
0 12 0 1
0 10 0 1
0 14 -1 0
1
end_operator
begin_operator
stack arm1 b3 b1
0
3
0 8 0 1
0 11 0 1
0 13 -1 0
1
end_operator
begin_operator
stack arm1 b3 b2
0
3
0 9 0 1
0 11 0 1
0 0 -1 0
1
end_operator
begin_operator
stack arm1 b3 b3
0
3
0 12 0 1
0 11 0 1
0 1 -1 0
1
end_operator
begin_operator
unstack arm1 b1 b1
0
3
0 8 -1 0
0 7 -1 0
0 6 0 1
1
end_operator
begin_operator
unstack arm1 b1 b2
0
3
0 9 -1 0
0 7 -1 0
0 5 0 1
1
end_operator
begin_operator
unstack arm1 b1 b3
0
3
0 12 -1 0
0 7 -1 0
0 2 0 1
1
end_operator
begin_operator
unstack arm1 b2 b1
0
3
0 8 -1 0
0 10 -1 0
0 3 0 1
1
end_operator
begin_operator
unstack arm1 b2 b2
0
3
0 9 -1 0
0 10 -1 0
0 4 0 1
1
end_operator
begin_operator
unstack arm1 b2 b3
0
3
0 12 -1 0
0 10 -1 0
0 14 0 1
1
end_operator
begin_operator
unstack arm1 b3 b1
0
3
0 8 -1 0
0 11 -1 0
0 13 0 1
1
end_operator
begin_operator
unstack arm1 b3 b2
0
3
0 9 -1 0
0 11 -1 0
0 0 0 1
1
end_operator
begin_operator
unstack arm1 b3 b3
0
3
0 12 -1 0
0 11 -1 0
0 1 0 1
1
end_operator
0
