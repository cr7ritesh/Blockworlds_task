Here is an optimal plan to achieve the described goal: 

- **unstack b4 from b1**
   - Precondition: b4 is clear, the arm is empty
   - Postcondition: the arm is holding b4, b1 is no longer on top of b4

- **putdown b4**
   - Precondition: the arm is holding b4
   - Postcondition: b4 is on the table, the arm is now empty

- **pickup b4**
   - Precondition: b4 is on the table, the arm is empty
   - Postcondition: the arm is now holding b4

- **unstack b1 from b2**
   - Precondition: b1 is clear, the arm is empty
   - Postcondition: the arm is holding b1, b1 is no longer on top of b2

- **stack b1 on b4**
   - Precondition: the arm is holding b1, b4 is clear
   - Postcondition: b1 is now on top of b4, the arm is empty

- **pickup b2**
   - Precondition: b2 is on the table, the arm is empty
   - Postcondition: the arm is now holding b2

- **unstack b3 from b2**
   - Precondition: b2 is clear, the arm is empty
   - Postcondition: the arm is holding b3, b3 is no longer on top of b2

- **stack b3 on b5**
   - Precondition: the arm is holding b3, b5 is clear
   - Postcondition: b3 is now on top of b5, the arm is empty

- **pickup b1**
   - Precondition: b1 is on the table, the arm is empty
   - Postcondition: the arm is now holding b1

- **stack b1 on b3**
   - Precondition: the arm is holding b1, b3 is clear
   - Postcondition: the goal is achieved, b1 is on top of b3

So, the final sequence of actions or plan is: **unstack b4, putdown b4, pickup b4, unstack b1, stack b1 on b4, pickup b2, unstack b3, stack b3 on b5, pickup b1, and stack b1 on b3**.

This plan achieves the goal of having b1 on top of b3 and b3 on top of b5, with the given initial configuration of blocks.