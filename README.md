# Monopoly-Move-Simulation
A program to analyze the probability of landing on each tile in the Monopoly board given the normal game settings.

Landing on a location is defined as during the turn, if you rolled the die causing you to move to said location or a Chance/Community Chest card causes you to move to said location. In the case if you land on the 'Go To Jail' location, a count will be added for the 'Go To Jail' location as well as the 'In Jail (Just Visiting)' location. A count will not be added for if the player is in Jail and they proceed to stay in Jail for the turn and if a player is on Chance/Community Chest and draw a card that doesn't move them from the location.

Assumptions made regarding the Chance and Community Chest piles are all drawn cards from their respective piles are placed into a separate pile until their respective piles are empty. It is at this point when all Chance or Community Chest cards (whichever pile is empty) not held by the player (Get Out of Jail Free cards) are reshuffled.

If a player is in jail and they hold either one or both (Get Out of Jail Free cards), they will choose with 50% to use one to get out of jail for the next turn. This is done because there are no incentives to stay in or leave jail.
