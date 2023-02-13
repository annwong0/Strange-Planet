#
# CSCI3180 Principles of Programming Languages
#
# --- Declaration ---
#
# I declare that the assignment here submitted is original except for source
# material explicitly acknowledged. I also acknowledge that I am aware of
# University policy and regulations on honesty in academic work, and of the
# disciplinary guidelines and procedures applicable to breaches of such policy
# and regulations, as contained in the website
# http://www.cuhk.edu.hk/policy/academichonesty/
#
# Assignment 2
# Name : Wong Pui Yee
# Student ID : 1155127529
# Email Addr : pywong9@cse.cuhk.edu.hk
#

from Map import Map
from Cell import Plain, Mountain, Swamp, Cell
from GameCharacter import Player, Goblin

class Engine:
    def __init__(self, data_file):
        self._actors = []
        self._map = None 
        self._player = None 
        with open(data_file, 'r') as fp:
            line = fp.readline()
            if not line:
                return None 
            else:
                items = line.split()
                if len(items) != 5:
                    print('INVALID DATA FILE.')
                    return None 
                num_of_row = int(items[0])
                num_of_col = int(items[1])
                p_ox = int(items[2])
                p_hp = int(items[3])
                num_of_goblins = int(items[4])

            self._map = Map(num_of_row, num_of_col)
            
            # TODO: initialize each cell of the map object 
            #       using the build_cell method 
            for x in range(num_of_row):
                line = fp.readline()
                items = line.split()
                for y in range(num_of_col):
                    if items[y] == 'P':
                        self._map._cells[x][y] = Plain(x, y)
                        self._map.build_cell(x, y, self._map._cells[x][y])
                    elif items[y] == 'M':
                        self._map._cells[x][y] = Mountain(x, y)
                        self._map.build_cell(x, y, self._map._cells[x][y])
                    elif items[y] == 'S':
                        self._map._cells[x][y] = Swamp(x, y)
                        self._map.build_cell(x, y, self._map._cells[x][y])
                    else:
                        print('INVALID CELL TYPE!')

            # END TODO
           
            self._player = Player(num_of_row - 1, 0, p_hp, p_ox)
            
            # TODO: initilize the position of the player 
            #       using the set_occupant and occupying setter;
            #       add the player to _actors array 
            self._player.occupying = self._map.get_cell(num_of_row - 1, 0).set_occupant(self._player)
            self._actors.append(self._player)
            # END TODO 


            for gno in range(num_of_goblins):
                # TODO: initilize each Goblin on the map
                #       using the set_occupant and occupying setter;
                #       add each Goblin to _actors array 
                line = fp.readline()
                items = line.split()
                gno = Goblin(int(items[0]), int(items[1]), items[2:])
                gno.occupying = self._map.get_cell(int(items[0]), int(items[1])).set_occupant(gno)
                self._actors.append(gno)
                # END TODO

    def run(self):
        # main rountine of the game
        self.print_info()
        while not self.state():    
            for obj in self._actors:
                if obj.active: 
                    obj.act(self._map)
            self.print_info()
            self.clean_up()
        self.print_result()

    def clean_up(self):
        # TODO: remove all objects in _actors which is not active 
        i = 0
        for obj in self._actors:
            if obj.active == False:
                self._actors.pop(i)
            i += 1
        # END TODO

    # check if the game ends and return if the player win or not.
    def state(self):
        # TODO: check if the game ends and 
        #       return an integer for the game status 
        if self._player.row == 0 and self._player.col == self._map.cols - 1 and self._player.oxygen > 0 and self._player.hp > 0:
            return 1
        elif self._player.oxygen <= 0 or self._player.hp <= 0:
            return -1
        else:
            return 0
        # END TODO 
        
    def print_info(self):
        self._map.display()
        # TODO: display the remaining oxygen and HP 
        print('Oxygen: %d, HP: %d' %(self._player.oxygen, self._player.hp))
        # END TODO 

    def print_result(self):
        # TODO: print a string that shows the result of the game. 
        if self.state() == 1:
            print('\033[1;33;41mCongrats! You win!\033[0;0m')
        elif self.state() == -1:
            print('\033[1;33;41mBad Luck! You lose.\033[0;0m')
        else:
            print('ERROR.')
        # END TODO

        
