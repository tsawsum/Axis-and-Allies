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

List of things AI needs to do:
- Needs to decide if we are winning
 * use above stuff
- Needs to decide risk tolerance
 * Used in is_vulnerable and everywhere that it is used.
 * What is the minimum threshold ratio of the Hawkes formula that the AI will tolerate
 * < 1 - risk tolerance is vulnerable
 * Look at past battles and decide if they won in the end and what the 'risk tolerance' was
 * I have a higher risk tolerance if I am losing
- Needs to make an 'importance' value of each territory:
 * Informed by webcrawled games.
- Factory builder
 * each territory from other games has a average factory value (how many were there and whose).
 * if you are the player, you will build a factory there according to those values and if you can hold it
 * Make sure we impliment both purchase and placement (place the factory at the end so it doesnt think it can build in it)
- Calculate build average for each teritory
 * build importance determine max build in unthreateneed territories
- AI organize placements list
 * WHAT THE FUCK WERE WE THINKING WHYYYYYYY
- Needs to decide build priority values.
"""
