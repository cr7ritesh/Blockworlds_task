Here is an optimal plan to solve the new planning problem: 

- unstack b2 from b5
- unstack b5 from b4
- putdown b5
- unstack b9 from b6
- putdown b9
- unstack b3 from b4
- putdown b3
- unstack b6 from b9
- putdown b6
- unstack b7 from b10
- putdown b7
- unstack b10 from b7
- putdown b10
- pickup b2
- stack b2 on b7
- pickup b5
- stack b5 on b4
- pickup b6
- stack b6 on b10
- pickup b7
- stack b7 on b3
- pickup b9
- stack b9 on b5
- pickup b10
- stack b10 on b9
- pickup b11
- stack b11 on b1

This plan ensures that the blocks are arranged in the desired configuration, with each block stacked on top of the specified other block. The plan also takes into account the initial state of the blocks and the arm, and ensures that the arm is empty and the blocks are on the table or stacked as needed after each action.