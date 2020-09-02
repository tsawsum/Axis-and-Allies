# Axis-and-Allies
Basic Axis and Allies AI

Todo list:
- If a sub enters combat, it needs to use up all remaining movement. But the program can't differentiate between a sub attacking vs staying submerged when it ends its combat turn in enemy territories. It currently assumes that if a sub ends in enemy units on a combat turn, then it attacks (and that it would move during non-combat otherwise)
- Multiple fighters can plan a return path to the same carrier, potentially going over its capacity and forcing a fighter to die. This is basically unfixable, and the same bug exists in the game's source code. Also, carriers must move before fighters during non-combat turns, because the program assumes this in order to simplify calculations
- Currently factories are considered enemy units, which needs to be fixed