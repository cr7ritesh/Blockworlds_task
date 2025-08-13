Here is an optimal plan to solve the given block-stacking problem: 

1. pickup b7
2. pickup b8
3. putdown b7
4. stack b8 on b7
5. pickup b1
6. stack b1 on b8
7. pickup b6
8. stack b6 on b1
9. pickup b4
10. putdown b4
11. stack b6 on b4
12. pickup b7
13. stack b7 on b6
14. pickup b5
15. stack b5 on b6
16. pickup b2
17. stack b2 on b5
18. pickup b3
19. stack b3 on b2

In this plan, the robot first creates a stack of blocks b7, b8, b1, and b6, following the current arrangement. Then, it places b4 on the table and builds a new stack on top of it, with b6, b7, b1, and b5. Finally, it creates the desired stack of b2 and b3 on top of b5, fulfilling the goal configuration. 

The plan ensures that the blocks are moved optimally, with no unnecessary moves, and achieves the desired configuration.