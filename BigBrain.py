"""
Some Heuristics to consider:
 - Total Unit Value Ratio (Axis vs Allies) compared to the start to determine who is winning
 - Same thing but just sea power
 - Same thing but just air power
 - Same thing but just land power
 - Might be worth literally checking every unit to see if there is a correlation but this might be crazy
 - Percent of unit value in range of the front line
 - Total income compared to start
 - Number of 'combat important territories' you control / have ranged jurisdiction over
 - Number of your vs. their factories that are in danger
 - Create some sort of "Similarity distance' function to compare current board with known 'winning' boards
 - Overall 'luck' value. Do battle calculator before every battle and add up the difference between expected ipc_swing for your side and actual
 - Could do a similar luck value based on percentages, where an actual win is 1 and a loss 0.
 - Obviously number of controlled capitals.
 - Number of factories taken from enemy
 - which team controls suez
 
"""
