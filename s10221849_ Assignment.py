#This program is a city-building strategy game; Simp City. 
#Author: Chew Shi Wei
#Last modified: 8/9/2021
'''This city-building strategy game is played over 16 turns. In each turn, you will build one of two randomly-selected buildings in 
your 4x4 city. In the first turn, you can build anywhere in the city. In subsequent turns, you can only build on squares that are 
connected to existing buildings. The other building that you did not build is discarded.

Each building scores in a different way. The objective of the game is to build a city that scores as many points as possible.

There are 5 types of buildings, with 8 copies of each:
•	Beach (BCH): Scores 3 points if it is built on the left or right side of the city, or 1 point otherwise
•	Factory (FAC): Scores 1 point per factory (FAC) in the city, up to a maximum of 4 points for the first 4 factories. 
    All subsequent factories only score 1 point each.
•	House (HSE): If it is next to a factory (FAC), then it scores 1 point only. Otherwise, it scores 1 point for each adjacent house (HSE) 
    or shop (SHP), and 2 points for each adjacent beach (BCH).
•	Shop (SHP): Scores 1 point per different type of building adjacent to it.
•	Highway (HWY): Scores 1 point per connected highway (HWY) in the same row. '''

#for loading of game and score
import csv

#creating empty file 
import os 
f = open('Simp_City.csv','w')
f.close()

#setting up lists: ---
letter = ['a','b','c','d'] 

number = ['1','2','3','4']

    #this list mainly stores the remaining number of each building 
building = [[8, 'BCH'],[8, 'FAC'],[8, 'HSE'],[8, 'SHP'],[8, 'HWY']]

    #this list will store the buildings built on each coordinate
    #if no buildings built -> coordinates[i][1] = '   ' (empty)
coordinates = []
for i in range(1, 5):
    for z in range(0,len(letter)):
        coordinates.append([letter[z]+str(i), '   '])
        #[['a1', '   '], ['b1', '   '], ['c1', '   '],...]
        

#end of setting up lists ---

#Function 1 prints the main menu of game ---
def display_main_menu():
    print('''Welcome, mayor of Simp City!
----------------------------
1. Start new game
2. Load saved game
3. Show high scores

0. Exit''')

#end of display_main_menu() function ---

#Function 2 prints the number of turns, the board with the buildings built ---
def print_board_buildings(letter, coordinates):

    #turn number is determined by how many buildings are built 
    turn = 1 
    for x in range(0, len(coordinates)):
        if coordinates[x][1] != '   ':
            turn += 1 

    #printing of turn number should stop when it rches turn 16 
    if turn <= 16:
        print('Turn {}'.format(turn))

    #printing of map 
    print('''    A     B     C     D
 +-----+-----+-----+-----+''')
    t = 0
    for i in range(1,5):
        print(i, end='')
        for z in range(0, len(letter)):
            print('| ' + str(coordinates[t][1]) + ' ', end='') #printing of buildings
            t += 1
        print('|\n +-----+-----+-----+-----+')

    return turn #returns turn number for another function 
   #end of print_board_building(letter, coordinates) function ---

#Function 3 prints the game menu ---
def print_game_menu():
    option = [] #to list the buildings that were randomly imported 
    import random
    count = 1
    for i in building:
        if count <= 2: #so only print two times
            random_choice = random.choice(building)[1]
            print('{:d}. Build a {}'.format(count, random_choice))
            option.append(random_choice)
            count += 1
            
    print('''3. See remaining buildings
4. See current score

5. Save game
0. Exit to main menu''')

    return option #returns function for another function 

#end of print_game_menu() function ---

#Function 4 finds the adjacent building based on the location entered ---
def find_adjacent(location):

    #letter = ['a','b','c','d'] 
    #number = ['1','2','3','4']
    adjacent = []
    left = ''
    right = ''
    top = ''
    bottom = ''

    #for finding coordinates of left n right
    for i in range(0, len(letter)):
        if location[0] == letter[i]:

            #if location's letter is 'a'
            if location[0] == letter[0]:
                right = letter[1] + location[1]
                #for eg. location = 'a1', right='b1 
                

            #if location's letter is 'd'
            elif location[0] == letter[len(letter)-1]:
                left = letter[len(letter)-2] + location[1]
                #for eg. location = 'd1', left='c1
                

            else:
                left = letter[i-1] + location[1]
                right = letter[i+1] + location[1]

            break

    #for finding coordinates of top n bottom 
    for i in range(0, len(number)):
        if location[1] == number[i]:

            #if location's number is '1'
            if location[1] == number[0]:
                bottom = location[0] + number[1] 
                #for e.g. location = b1, bottom = b2 
                break

            #if location's number is '4'
            elif location[1] == number[len(number)-1]:
                top = location[0] + number[len(number)-2]
                #for e.g. location = c4, top = c3
                break
            else:
                top = location[0] + number[i-1]
                bottom = location[0] + number[i+1]
                break

    adjacent.append(left)
    adjacent.append(right)
    adjacent.append(top)
    adjacent.append(bottom)

    return adjacent #for eg, location = 'b2' -> adjacent = ['a2', 'c2', 'b1', 'b3']

#end of find_adjacent(location) function ---

#Function 5  prompts user for placement of building, and validates their input 
def validation_of_building(option,game_choice,coordinates,building,turn):
    location = input('Build where?')
    location = location.lower() #in case user enter A1 instead of a1
    #letter = ['a','b','c','d'] 
    #number = ['1','2','3','4']
    location_should_be = []
    
    #['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'd1', 'd2', 'd3', 'd4']
    for i in range(len(letter)):
        for j in range(len(number)): 
            location_should_be.append(letter[i]+number[j]) 
    
    if location not in location_should_be:
        print('Invalid input.')

    else:
        #so can append to the remaining building
        for i in range(0, len(building)): 
            if option[game_choice-1] == building[i][1]:
                
                for j in range(0, len(coordinates)):
                    if coordinates[j][0] == location:    
                        if coordinates[j][1] != '   ': #means there's already a building at that location 
                            print('This area has already been built! Try again.')
                            break 

                        else:      
                            #turn 2 onwards only can build at spaces that are 
                            #built orthogonally adjacent to existing buildings
                            if turn > 1:
                                value = 0 
                                adjacent = find_adjacent(location) #finds the adjacent of the location 
                                for k in range(0, len(adjacent)):
                                    for a in range(0, len(coordinates)):
                                        if adjacent[k] == coordinates[a][0] and coordinates[a][1] != '   ': #if the adjacents are not empty
                                                                                                                    # = valid to build        
                                            coordinates[j][1] = option[game_choice-1] #alter coordinates list so new building will be printed
                                            building[i][0] -= 1 #append remaining number of building
                                            value = 1
                                            break

                                if value == 0: #means no adjacent has buildings = invalid to build 
                                    print('You must build next to an existing building.')
                                        
                            #for turn 1, building can build anywhere 
                            else:
                                coordinates[j][1] = option[game_choice-1] #alter coordinates list so new building will be printed
                                building[i][0] -= 1 #append remaining number of building 

#end of validation_of_building(option,game_choice,coordinates,building,turn) ---

#Function 6 save the coordinates 
def save_game(coordinates):
    save_game = open('Simp_City.csv','w')

    #coordinates, building
    #a1,BCH
    #b1,HSE...
    for i in range(0, len(coordinates)): 
        save_string = '' 
        save_string += str(coordinates[i][0]) #coordinates
        save_string += ',' + str(coordinates[i][1]) + '\n' #,building 
        save_game.write(save_string)    #coordinates, building
                                        #a1,BCH
    save_game.close()                   #b1,HSE...
    
#end of save_game(coordinates) function ---

#Function 7 makes the data store back into coordinates list ---
def load_game():
    
    load_game = open('Simp_City.csv','r')
    data = csv.reader(load_game)

    coordinates = []
    for line in data:
            coordinates.append(line)
    load_game.close()

    return coordinates  
#end of load_game() function ---

#Function 8 calculates and display the current scores for each building type ---
def see_current_scores(coordinates):

    #'setting' variables
    BCHtotal = 0
    BCHprint = '0'

    FACcount = 0 
    FACtotal = 0 
    FACprint = '0'

    HSEtotal = 0
    HSEprint = '0' 

    SHPtotal = 0 
    SHPprint = '0'

    HWYlist = [[],[],[],[]]
    HWYpoints = [] 
    
    #iterate thru coordinates 
    #example of coordinates - [['a1', '   '], ['b1', 'BCH'], ['c1', '   '],...]
    for i in range (0, len(coordinates)):

        #beach points 
        if coordinates[i][1] == 'BCH': 
            #if first letter is 'a' or 'd' 
            if coordinates[i][0][0] == letter[0] or coordinates[i][0][0] == letter[-1]:
                BCHtotal += 3
                if BCHprint == '0': 
                    BCHprint = '3'
                else:
                    BCHprint += ' + 3'
            else:   #if first letter is 'b' or 'c'
                BCHtotal += 1 
                if BCHprint == '0':
                    BCHprint = '1'
                else:
                    BCHprint += ' + 1'

        #factory points 
        elif coordinates[i][1] == 'FAC':
            FACcount += 1 
            #to be continued: another loop is needed outside of the current loop 
    
        #house points 
        elif coordinates[i][1] == 'HSE':
            HSEscore = 0
            fac = False
            adjacent = find_adjacent(coordinates[i][0])
            for t in range(0, len(coordinates)):
                for y in range(0, len(adjacent)):
                    if coordinates[t][0] == adjacent[y]: 
                        if coordinates[t][1] == 'FAC': #if adjacent contains factory
                            HSEscore = 1 #HSescore will be 1 regardless 
                            fac = True 
                            break #break thru 2nd loop
                        
                        #if adjacent contains 'hse' or 'shp'
                        elif coordinates[t][1] == 'HSE' or coordinates[t][1] == 'SHP': 
                            HSEscore += 1 
                        
                        elif coordinates[t][1] == "BCH": #if adjacent contains beach 
                            HSEscore += 2

                if fac == True:
                    break #to break thru 1st loop 

            HSEtotal += HSEscore
            if HSEprint == '0':
                HSEprint = str(HSEscore)
            else:
                HSEprint += ' + ' + str(HSEscore)

        #shop points 
        elif coordinates[i][1] == 'SHP': #scores based on number of diff types og building in adjacent 
            adjacent = find_adjacent(coordinates[i][0])
            type_of_buildings = [] 
            for j in range(0,len(coordinates)):
                for k in range(0,len(adjacent)):
                    if coordinates[j][0] == adjacent[k]:
                        type_of_buildings.append(coordinates[j][1])
                        
                        #number of unique buildings 
                        number_of_diff = len(set(type_of_buildings))

            SHPtotal += number_of_diff
            if SHPprint == '0':
                SHPprint = str(number_of_diff)
            else:
                SHPprint += ' + ' + str(number_of_diff)

        #highway points
        elif coordinates[i][1] == "HWY":
            #HWYlist = [[],[],[],[]]
            #first element is for row 1, second is for row 2...
            for j in range(0, len(number)): #one row max 4 buildings
                if coordinates[i][0][1] == number[j]:
                    for k in range(0, len(letter)):
                                
                        # coordinates[i][0][0] is letter e.g. a b c d
                        if coordinates[i][0][0] == letter[k]:
                            HWYlist[j].append(int(letter.index(letter[k]))+1)
                            #converts a to 1, b to 2, c to 3, d to 4 

            #example: hwy built at a2,b2,c1
            #HWYlist = [[],[1,2],[3],[]]
            
    for a in range(0, len(HWYlist)):         
        #count how many highways are in each row
        HWYcount = len(HWYlist[a])
        if HWYcount >= 1: #if more than 1 hwy in that row 
            diff = HWYlist[a][-1] - HWYlist[a][0] #last element - first element
            if diff == HWYcount - 1: #all the hwy in that row is connected
                for i in range(HWYcount):
                    HWYpoints.append(HWYcount)
            elif diff > HWYcount - 1: #if not
                if HWYcount == 2: #if only 2hwy but diff is not 1 = not side by side
                    for i in range(HWYcount):
                        HWYpoints.append(1) #1 pt each 
                                
                elif HWYcount == 3: #if 3 hwy in that row 
                    diffs = HWYlist[a][-2] - HWYlist[a][0] #second element - first element 
                    if diffs == 1: #two side by side, one not 
                        for i in range(2):
                            HWYpoints.append(HWYcount - 1)
                        HWYpoints.append(1)
                    else:
                        HWYpoints.append(1)
                        for i in range(2):
                            HWYpoints.append(HWYcount - 1)

        elif HWYcount == 1: #if only 1 hwy in that row 
            HWYpoints.append(1) #only 1 pt

    if FACcount <= 4: #if thr's less than 4 factories
        for i in range(0, FACcount):
            if FACprint == "0":
                FACprint = ''
                FACprint += str(FACcount)
            else:
                FACprint += " + " + str(FACcount)

            FACtotal = FACcount * FACcount 
                                
    else:
        more_than_four = FACcount - 4
        FACtotal = 16 + more_than_four
        FACprint = '4 + 4 + 4 + 4'
        for i in range (0,more_than_four):
            FACprint += ' + 1'

    #printing of scores
    print("BCH: " + BCHprint + " = " + str(BCHtotal))
    print("FAC: " + FACprint + " = " + str(FACtotal))
    print("HSE: " + HSEprint + " = " + str(HSEtotal))
    print("SHP: " + SHPprint + " = " + str(SHPtotal))
    HWYtotal = 0
    if len(HWYpoints) == 0:
        print('HWY: 0 = {}'.format(HWYtotal))
    else:
        print("HWY: ", end='')

        for i in range(0, len(HWYpoints)):
            if i <= len(HWYpoints) - 2:
                print(HWYpoints[i], end=' + ')
                HWYtotal += HWYpoints[i]
            else:
                HWYtotal += HWYpoints[i]
                print(str(HWYpoints[i]) + " = " + str(HWYtotal))  
                #print('HWY: ' + HWYpoints.split(',', ' + ') + ' = ' + str(HWYtotal))

    total = BCHtotal + FACtotal + HSEtotal + SHPtotal + HWYtotal
    print("Total score: " + str(total))
    return total #for high score function 

#end of see_current_score(coordinates, letter)---

#Function 9 saves highscores into file 
def save_highscores(highscore_list):
    save_hs = open('Highscores.csv', 'w')

    for i in range(0,len(highscore_list)):
        save_string = ''
        save_string += str(highscore_list[i][0]) #scores
        save_string += ',' + str(highscore_list[i][1]) + '\n' #playername
        save_hs.write(save_string)  #score, player's name
                                    #47, try n beat me
    save_hs.close()

#end of save_highscores(highscore_list) function ---  

#Function 10 checks if the player beats the 10th place in leaderboard ---
def beat_highscores(total,highscore_list,highscore_score):
    highscore_name_score = []

    #if leaderboard has less than 10 scores
    if len(highscore_list) != 10: 
        #find position: 
        highscore_score.append(total)
        highscore_score = sorted(highscore_score,reverse=True) #this will sort highest to lowest  
        position = (highscore_score.index(total)+1) #to find position 
        print('Congratulations! You made the high score board at position {}'.format(position))
        player = input('Please enter your name (max 20 chars): ')

        #highscore_name_score = [total,'name']
        highscore_name_score.append(str(total))
        highscore_name_score.append(player)
        highscore_list.append(highscore_name_score) #append highscore_name_score as an element in highscore_list

        save_highscores(highscore_list) #call function to save new scores
        leaderboard(highscore_list) #display leaderboard since player made it in 

    else:
        if total >= (highscore_score[-1]+1): #if total is more than the 10th place in leaderboard  
            highscore_score.append(total) #add new highscore
            highscore_score = sorted(highscore_score,reverse=True) #sort list with new highscore 
            highscore_score.pop(-1) #remove lowest score
            #print(highscore_score)
            position = (highscore_score.index(total)+1) #find position of new highscore
            print('Congratulations! You made the high score board at position {}'.format(position))
            player = input('Please enter your name (max 20 chars): ')

            #highscore_name_score = [total,'name']
            highscore_name_score.append(str(total))
            highscore_name_score.append(player)

            highscore_list.append(highscore_name_score) #add new high score into list
            highscore_list.sort() #sort list based on total (player's score)
            highscore_list.pop(0) #remove the one with lowest score 

            save_highscores(highscore_list)  #call function to save new scores
            leaderboard(highscore_list) #display leaderboard since player made it in 

#end of beat_highscores(total,highscore_list,highscore_score function --- 

#Function 11 loads the data back into the lists ---
def load_highscores():
    load_hs = open('Highscores.csv', 'r')
    hs = csv.reader(load_hs)

    highscore_list = []
    for line in hs:
        highscore_list.append(line)
    load_hs.close()

    highscore_score = [] #list needed to check position of player on leaderboard
    for i in range(0, len(highscore_list)):
        highscore_score.append(int(highscore_list[i][0]))

    return [highscore_list,highscore_score] 

#end of load_highscores() function ---

#Function 12 prints the leaderboard 
def leaderboard(highscore_list):
    #printing of leaderboard
    print('--------- HIGH SCORES ---------')
    print('{:4}{:22}{:5}'.format('POS','Player','Score'))
    print('{:4}{:22}{:5}'.format('---','------','-----'))

    highscore_list.sort()
    highscore_list.reverse() #so scores arranged in descending order
    for i in range(len(highscore_list)):
        print('{:>2}{:2}{:<22}{:<5}'.format(i+1,'.',highscore_list[i][1],highscore_list[i][0]))
    print('-------------------------------')

#end of leaderboard(highscore_list) function --- 

result = load_highscores()
highscore_list = result[0]
highscore_score = result[1]

#Main Game ---
#This part of the program takes in the players' input
game_state = 'main'
game_over = False 

while game_state != 'exit':
    if game_state == 'main':
        display_main_menu()
        main_choice = input('Your choice?')
        
        if main_choice == '1': #start new game 
            #resets board
            coordinates = [] 
            for i in range(1, 5):
                for z in range(0,len(letter)):
                    coordinates.append([letter[z]+str(i), '   '])

            game_state = 'game'
            game_over = False 
            

        elif main_choice == '2': #load saved game 
            saved_file = 'Simp_City.csv'
            if os.stat(saved_file).st_size == 0: #if file = empty means no previous data 
                print('No saved game.')
                continue

            else: 
                coordinates = load_game()
                game_state = 'game'
                game_over = False 
            
        elif main_choice == '3': #show high scores 
            leaderboard(highscore_list)

        elif main_choice == '0': #exit 
            game_state = 'exit'
            print('Thanks for playing! We hope to see you again :)')

        else: #[validation]
            print('Invalid choice.')

    elif game_state == 'game':
        while not game_over:
            turn = print_board_buildings(letter,coordinates)
            option = print_game_menu()

            #input needs to be integer [validation]
            try:
                game_choice = int(input('Your choice?'))
            except:
                print('Invalid choice.')
                break 
        
            if game_choice == 1 or game_choice == 2:
                validation_of_building(option,game_choice,coordinates,building,turn)
                
                if turn==16:
                    print('Final layout of Simp City:')
                    print_board_buildings(letter, coordinates)
                    total = see_current_scores(coordinates)
                    beat_highscores(total,highscore_list,highscore_score) #see if player makes it in leaderboard
                    game_over = True
                    game_state = 'main' #prints main menu
                 

            elif game_choice == 3: #see remaining building 
                print("Building\tRemaining")
                print("--------\t---------")
                for i in building:
                    print(i[1] + "\t\t" + str(i[0]))
                

            elif game_choice == 4: #see current score 
                see_current_scores(coordinates)
                
            elif game_choice == 5: #save game 
                save_game(coordinates)
                print('Game saved!')
                
            elif game_choice == 0: #exit to main menu 
                game_state = 'main' 
                game_over = True
                
            else: #if input is integer but not '1' '2' '3' '4' '5' '0' [validation]
                print('Invalid choice.')
