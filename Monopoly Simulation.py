# Import statements
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

# User defined variables variables
DATA_DIR = 'C:/Users/Chris/Desktop'
NUM_TURNS = 500000

# Game variables
current_pos = 0
chance_stack = []
com_chest_stack = []
game_over = False
jail = 0
out_jail_card = [False, False]
turn_history = pd.DataFrame()

# Create monopoly game board dataframe
monopoly_spots = {'Position': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                               24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                  'Name': ['Go', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax',
                           'Reading Railroad', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue',
                           'In Jail (Just Visiting)', 'St. Charles Place', 'Electric Company', 'States Avenue',
                           'Virginia Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest',
                           'Tennessee Avenue', 'New York Avenue', 'Free Parking', 'Kentucky Avenue', 'Chance',
                           'Indiana Avenue', 'Illinois Avenue', 'B. & O. Railroad', 'Atlantic Avenue',
                           'Ventnor Avenue', 'Water Works', 'Marvin Gardens', 'Go To Jail', 'Pacific Avenue',
                           'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance',
                           'Park Place', 'Luxury Tax', 'Boardwalk'],
                  'Class': ['Go', 'Brown', 'Community Chest', 'Brown', 'Tax', 'Railroads', 'Light Blue', 'Chance',
                            'Light Blue', 'Light Blue', 'In Jail (Just Visiting)', 'Pink', 'Utilities', 'Pink', 'Pink',
                            'Railroads', 'Orange', 'Community Chest', 'Orange', 'Orange', 'Free Parking', 'Red',
                            'Chance', 'Red', 'Red', 'Railroads', 'Yellow', 'Yellow', 'Utilities', 'Yellow',
                            'Go To Jail', 'Green', 'Green', 'Community Chest', 'Green', 'Railroads', 'Chance',
                            'Dark Blue', 'Tax', 'Dark Blue'],
                  'RGB': [(0.749, 0.859, 0.682), (0.525, 0.298, 0.220), (0.749, 0.859, 0.682), (0.525, 0.298, 0.220),
                          (0.749, 0.859, 0.682), (0, 0, 0), (0.675, 0.863, 0.941), (0.749, 0.859, 0.682),
                          (0.675, 0.863, 0.941), (0.675, 0.863, 0.941), (0.749, 0.859, 0.682), (0.773, 0.220, 0.518),
                          (0.749, 0.859, 0.682), (0.773, 0.220, 0.518), (0.773, 0.220, 0.518), (0, 0, 0),
                          (0.925, 0.545, 0.172), (0.749, 0.859, 0.682), (0.925, 0.545, 0.172), (0.925, 0.545, 0.172),
                          (0.749, 0.859, 0.682), (1, 0, 0), (0.749, 0.859, 0.682), (1, 0, 0), (1, 0, 0), (0, 0, 0),
                          (1, 0.941, 0.016), (1, 0.941, 0.016), (0.749, 0.859, 0.682), (1, 0.941, 0.016),
                          (0.749, 0.859, 0.682), (0, 0.588, 0), (0, 0.588, 0), (0.749, 0.859, 0.682), (0, 0.588, 0),
                          (0, 0, 0), (0.749, 0.859, 0.682), (0, 0.4, 0.706), (0.749, 0.859, 0.682), (0, 0.4, 0.706)]}
game_board = pd.DataFrame(monopoly_spots, columns=['Position', 'Name', 'Class', 'RGB'])

# Functions
# Addresses Chance card picked up by player
def chance(card_num, pos, jail):
    if card_num == 0:
        desc = 'Advance to Go (Collect $200)'
        move = 40 - pos
        pos = 0
        jail = 0
    elif card_num == 1:
        desc = 'Advance to Illinois Ave.  If you pass Go, collect $200'
        if pos > 24: # If player needs to pass Go
            move = 40 - pos + 24
        else:
            move = 24 - pos
        pos = 24
        jail = 0
    elif card_num == 2:
        desc = 'Advance to St. Charles Place. If you pass Go, collect $200'
        if pos > 11: # If player needs to pass Go
            move = 40 - pos + 11
        else:
            move = 11 - pos
        pos = 11
        jail = 0
    elif card_num == 3:
        desc = 'Advance token to nearest Utility. If UNOWNED, you may buy it from the Bank. If OWNED, throw dice and ' \
               'pay owner a total 10 times the amount thrown.'
        if (pos > 28) or (pos < 12): # Go to Electric Company
            if pos > 28:
                move = 40 - pos + 12
            else:
                move = 12 - pos
            pos = 12
        else: # Go to Water Works
            move = 28 - pos
            pos = 28
        jail = 0
    elif card_num in [4, 5]:
        desc = 'Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise ' \
               'entitled. If Railroad is UNOWNED, you may buy it from the Bank.'
        if (pos > 35) or (pos < 5): # Go to Reading Railroad
            if pos > 35:
                move = 40 - pos + 5
            else:
                move = 5 - pos
            pos = 5
        elif (pos > 5) and (pos < 15): # Go to Pennsylvania Railroad
            move = 15 - pos
            pos = 15
        elif (pos > 15) and (pos < 25): # Go to B. & O. Railroad
            move = 25 - pos
            pos = 25
        else: # Go to Short Line
            move = 35 - pos
            pos = 35
        jail = 0
    elif card_num == 6:
        desc = 'Bank pays you dividend of $50'
        move = 0
        jail = 0
    elif card_num == 7:
        desc = 'Get out of Jail Free. This card may be kept until needed, or traded/sold'
        move = 0
        jail = 0
    elif card_num == 8:
        desc = 'Go back 3 spaces'
        move = -3 # Don't need to account for cross Go backwards as it's not possible from Chance positions
        pos -= 3
        jail = 0
    elif card_num == 9:
        desc = 'Go directly to Jail. Do not pass GO, do not collect $200'
        move = -99
        pos = 10
        jail = 1
    elif card_num == 10:
        desc = 'Make general repairs on all your property: For each house pay $25, For each hotel $100'
        move = 0
        jail = 0
    elif card_num == 11:
        desc = 'Pay poor tax of $15'
        move = 0
        jail = 0
    elif card_num == 12:
        desc = 'Take a ride on the Reading. If you pass Go, collect $200'
        move = 40 - pos + 5
        pos = 5
        jail = 0
    elif card_num == 13:
        desc = 'Take a walk on the Boardwalk. Advance token to Boardwalk'
        move = 39 - pos
        pos = 39
        jail = 0
    elif card_num == 14:
        desc = 'You have been elected Chairman of the Board. Pay each player $50'
        move = 0
        jail = 0
    else:
        desc = 'Your building and loan matures. Collect $150'
        move = 0
        jail = 0

    return pos, move, jail, desc, card_num

# Addresses Community Chest card picked up by player
def community_chest(card_num, pos, jail):
    if card_num == 0:
        desc = 'Advance to Go (Collect $200)'
        move = 40 - pos
        pos = 0
        jail = 0
    elif card_num == 1:
        desc = 'Bank error in your favor. Collect $200'
        move = 0
        jail = 0
    elif card_num == 2:
        desc = "Doctor's fees. Pay $50"
        move = 0
        jail = 0
    elif card_num == 3:
        desc = 'From sale of stock you get $45'
        move = 0
        jail = 0
    elif card_num == 4:
        desc = 'Get Out of Jail Free. This card may be kept until needed or sold'
        move = 0
        jail = 0
    elif card_num == 5:
        desc = 'Go to Jail. Go directly to jail. Do not pass Go, Do not collect $200'
        move = -99
        pos = 10
        jail = 1
    elif card_num == 6:
        desc = 'Grand Opera Night. Collect $50 from every player for opening night seats'
        move = 0
        jail = 0
    elif card_num == 7:
        desc = 'Xmas fund matures. Collect $100'
        move = 0
        jail = 0
    elif card_num == 8:
        desc = 'Income tax refund. Collect $20'
        move = 0
        jail = 0
    elif card_num == 9:
        desc = 'Life insurance matures. Collect $100'
        move = 0
        jail = 0
    elif card_num == 10:
        desc = 'Pay hospital $100'
        move = 0
        jail = 0
    elif card_num == 11:
        desc = 'Pay school tax of $150'
        move = 0
        jail = 0
    elif card_num == 12:
        desc = 'Receive for services $25'
        move = 0
        jail = 0
    elif card_num == 13:
        desc = 'You are assessed for street repairs: Pay $40 per house and $115 per hotel you own'
        move = 0
        jail = 0
    elif card_num == 14:
        desc = 'You have won second prize in a beauty contest. Collect $10'
        move = 0
        jail = 0
    else:
        desc = 'You inherit $100'
        move = 0
        jail = 0

    return pos, move, jail, desc, card_num

# Decides which pile to pick a card from
def card_pickup(pos, jail, out_jail_card, chance_stack, com_chest_stack):
    if pos in [7, 22, 36]: # Chance spot
        if len(chance_stack) == 0: # Rescrambles Chances cards if there are none left
            chance_stack = shuffle(chance_stack, out_jail_card, 1, 0)

        pos, move, jail, desc, chance_num = chance(chance_stack[0], pos, jail)
        chance_stack.pop(0) # Remove card drawn from the Chance pile

        if chance_num == 7: # 7 is card_num for Get Out of Jail card for Chance
            out_jail_card[0] = True

    elif pos in [2, 17, 33]: # Community Chest spot
        if len(com_chest_stack) == 0: # Rescrambles Community Chest cards if there are none left
            com_chest_stack = shuffle(com_chest_stack, out_jail_card, 0 , 1)

        pos, move, jail, desc, chest_num = community_chest(com_chest_stack[0], pos, jail)
        com_chest_stack.pop(0) # Remove card drawn from the Community Chest pile

        if chest_num == 4:  # 4 is card_num for Get Out of Jail card for Community Chest
            out_jail_card[1] = True

    return pos, move, jail, desc, out_jail_card, chance_stack, com_chest_stack

# Gives from random numbers from 1 - 6 mimicking rolling of 2 dies
def roll_dies():
    return [random.randint(1, 6), random.randint(1, 6)]

def shuffle(stack, out_jail_card, chance_ind, chest_ind):
    stack = random.sample(range(0, 15), 15) # Randomly shuffle the cards

    # Remove Get out of Jail card from Chance pile if player is holding it
    if (out_jail_card[0] == True) and (chance_ind == 1):
        stack.pop(stack.index(7)) # 7 is card_num for Get Out of Jail card for Chance

    # Remove Get out of Jail card from Community Chest pile if player is holding it
    elif (out_jail_card[1] == True) and (chest_ind == 1):
        stack.pop(stack.index(4)) # 4 is card_num for Get Out of Jail card for Community Chest

    return stack

# Moves the player based on die roll and cards picked up
def turn(roll, current_pos, jail, out_jail_card, chance_stack, com_chest_stack, turn_history):
    # Addresses running to the end of the board first loop
    if (current_pos + sum(roll) > 39):
        pos = current_pos + sum(roll) - 40
    else:
        pos = current_pos + sum(roll)
    turn_history = log_turns(i, sum(roll), roll, pos, '', turn_history)

    # Landed on Go To Jail spot
    if pos == 30:
        turn_history = log_turns(i, -20, '', 10, 'Landed on Go To Jail', turn_history)
        pos = 10
        jail += 1

    # Landed on Chance and Community Chest spots
    if pos in [2, 7, 17, 22, 33, 36]:
        pos, move, jail, desc, out_jail_card, chance_stack, com_chest_stack = card_pickup(pos, jail, out_jail_card, chance_stack,
                                                                                    com_chest_stack)
        turn_history = log_turns(i, move, '', pos, desc, turn_history)

        # For if player landed on Chance and then got shifted back to Community Chest
        if pos == 33:
            pos, move, jail, desc, out_jail_card, chance_stack, com_chest_stack = card_pickup(pos, jail, out_jail_card,
                                                                                              chance_stack,
                                                                                              com_chest_stack)
            turn_history = log_turns(i, move, '', pos, desc, turn_history)

    return pos, jail, out_jail_card, chance_stack, com_chest_stack, turn_history

# Records every action done in the game by player
def log_turns(i, move, roll, current_pos, desc, turn_history):
    if desc == '':
        text = 'Rolled a {}'.format(sum(roll))
    else:
        text = desc
    turn_history = turn_history.append({'Turn': i + 1, 'Advance': move, 'Dies': roll, 'Position': current_pos,
                          'Description': text}, ignore_index=True)

    return turn_history

# Main game loop
for i in range(NUM_TURNS):
    # If not in jail loop
    if jail == 0:
        doubles = 0
        # While player has not rolled 3 consecutive doubles
        while True:
            # Player turn roll
            roll = roll_dies()
            if roll[0] == roll[1]:
                current_pos, roll_jail, out_jail_card, chance_stack, com_chest_stack, turn_history = turn(roll,
                                                                                                          current_pos,
                                                                                                          jail,
                                                                                                          out_jail_card,
                                                                                                          chance_stack,
                                                                                                          com_chest_stack,
                                                                                                          turn_history)
                if roll_jail == 1:
                    break
                else:
                    doubles += 1
            else:
                current_pos, roll_jail, out_jail_card, chance_stack, com_chest_stack, turn_history = turn(roll,
                                                                                                          current_pos,
                                                                                                          jail,
                                                                                                          out_jail_card,
                                                                                                          chance_stack,
                                                                                                          com_chest_stack,
                                                                                                          turn_history)
                break
            if doubles == 2:
                # Go to jail if rolled doubles for 3rd consecutive time
                if roll[0] == roll[1]:
                    current_pos = 10
                    roll_jail += 1
                    turn_history = log_turns(i, -99, roll, current_pos,
                                             'Rolled doubles for the 3rd consecutive time, go directly to Jail',
                                             turn_history)
                else:
                    current_pos, roll_jail, out_jail_card, chance_stack, com_chest_stack, turn_history = turn(roll,
                                                                                                              current_pos,
                                                                                                              jail,
                                                                                                              out_jail_card,
                                                                                                              chance_stack,
                                                                                                              com_chest_stack,
                                                                                                              turn_history)
                break
        jail = roll_jail

    # If in jail loop
    elif 0 < jail < 3:
        # Check if player has Get out of Jail Free card
        if (out_jail_card[0] == True) or (out_jail_card[1] == True):
            use_card = random.sample(range(0, 2), 1)[0] # Randomly decide if want to use Get out of Jail Free card
            if use_card == 1:
                # If have both Get out of Jail Free cards randomly decide which to use
                if out_jail_card.count(True) == 2:
                    which_card = random.sample(range(0, 2), 1)[0]
                    out_jail_card[which_card] = False
                else:
                    if out_jail_card[0] == True:
                        out_jail_card[0] = False
                        turn_history = log_turns(i, 0, '', current_pos,
                                                 'Jail turn {}. Used Chance Get out of Jail Free card'.format(jail),
                                                 turn_history)
                    else:
                        out_jail_card[1] = False
                        turn_history = log_turns(i, 0, '', current_pos,
                                                 'Jail turn {}. Used Community Chest Get out of Jail Free card'.format(
                                                     jail), turn_history)
                jail = 0
            # If player doesn't want to use Get out of Jail Free card, the player still needs to roll
            else:
                roll = roll_dies()
                if roll[0] == roll[1]:
                    turn_history = log_turns(i, 0, roll, current_pos,
                                             'Jail turn {}. Rolled doubles out next turn'.format(jail),
                                             turn_history)
                    jail = 0
                else:
                    turn_history = log_turns(i, 0, roll, current_pos,
                                             "Jail turn {}. Didn't roll doubles, still in Jail next turn".format(
                                                 jail),
                                             turn_history)
                    jail += 1
        # Player rolls dies to for chance to leave jail
        else:
            roll = roll_dies()
            if roll[0] == roll[1]:
                turn_history = log_turns(i, 0, roll, current_pos,
                                         'Jail turn {}. Rolled doubles out next turn'.format(jail), turn_history)
                jail = 0
            else:
                turn_history = log_turns(i, 0, roll, current_pos,
                                         "Jail turn {}. Didn't roll doubles, still in Jail next turn".format(jail),
                                         turn_history)
                jail += 1
    # 3rd turn in jail so leave next turn regardless
    else:
        turn_history = log_turns(i, 0, roll, current_pos,
                                 'Jail turn {}. Rolled {}, but 3rd turn in Jail, so out next turn anyways'.format(
                                     jail, roll), turn_history)
        jail = 0
    print('Completed turn {:,}'.format(i + 1))

# Merge turn history with game board to find description of which location player is on
turn_history = turn_history.merge(game_board, on=['Position'], how='left')

# Filter dataframe for when player moved positions
player_moves = turn_history[turn_history['Advance'] != 0]
player_moves = player_moves.copy()
player_moves['Percentage'] = 100 / len(player_moves)

# Setup data for 1st graph
a_data = player_moves.groupby(['Position', 'RGB', 'Name'])['Percentage'].sum().reset_index()
a_xlabels = [i for i in a_data['Name']]
a_colour_list = [i for i in a_data['RGB']]

# Create 1st graph
plt.figure(figsize=(5, 4), dpi=300)
player_moves.groupby('Position')['Percentage'].sum().plot(kind='bar', color=a_colour_list)
plt.title('Probability of Landing on Each Location ({:,} Turns)'.format(NUM_TURNS), fontdict={'fontsize': 10, 'fontweight': 'bold'})
plt.xlabel('Location', fontsize=8)
plt.ylabel('Percentage (%)', fontsize=8)
plt.xticks(np.arange(len(a_xlabels)), labels=a_xlabels, rotation='vertical', fontsize=5)
plt.yticks(fontsize=7)
plt.tight_layout()
plt.savefig('{}/Probability of Landing on Each Location.png'.format(DATA_DIR))
plt.show()

# Setup data for 2nd graph
b_data = player_moves.groupby(['Class', 'RGB'])['Percentage'].sum().reset_index()
b_data = b_data.sort_values(by=['Percentage'], ascending=False)
b_data['Order'] = range(1, len(b_data) + 1)
b_xlabels = [i for i in b_data['Class']]
b_colour_list = [i for i in b_data['RGB']]

# Create 2nd graph
plt.figure(figsize=(5, 4), dpi=300)
b_data.groupby('Order')['Percentage'].sum().plot(kind='bar', color=b_colour_list)
plt.title('Probability of Landing on Each Type of Property ({:,} Turns)'.format(NUM_TURNS), fontdict={'fontsize': 8.5, 'fontweight': 'bold'})
plt.xlabel('Type', fontsize=8)
plt.ylabel('Percentage (%)', fontsize=8)
plt.xticks(np.arange(len(b_xlabels)), labels=b_xlabels, rotation='vertical', fontsize=5)
plt.yticks(fontsize=7)
plt.tight_layout()
plt.savefig('{}/Probability of Landing on Each Type of Property.png'.format(DATA_DIR))
plt.show()

# Save to CSV
del turn_history['RGB']
turn_history.to_csv('{}/Turn History.csv'.format(DATA_DIR), index=False)
game_board.to_csv('{}/Game Board.csv'.format(DATA_DIR), index=False)
