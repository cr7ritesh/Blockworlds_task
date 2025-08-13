Here is an optimal plan to solve the new planning problem: 

1. pickup b1
2. stack b1 on b5
3. unstack b5 from b4
4. putdown b5
5. unstack b4 from b2
6. stack b4 on b7
7. pickup b7
8. stack b7 on b8
9. unstack b2 from b3
10. putdown b2
11. pickup b5
12. stack b5 on b3
13. pickup b2
14. stack b2 on b10
15. unstack b10 from b9
16. putdown b10
17. pickup b9
18. stack b9 on b2
19. pickup b8
20. stack b8 on b10

This plan ensures that the blocks are arranged in the desired configuration, with b1 on top of b5, b2 on top of b10, and so on. The plan also takes into account the current state of the blocks and the arm, and ensures that the arm is empty at the end of each step, ready for the next action.