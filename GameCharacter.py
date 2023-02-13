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

from abc import ABCMeta
from abc import abstractmethod
from operator import truediv

class GameCharacter(metaclass=ABCMeta):
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._occupying = None
        self._name = None
        self._active = True
        self._character = None 
        self._color = '\033[1;31m'
    
    #TODO: name getter
    @property
    def name(self):
        return self._name
    
    #TODO: row getter
    @property
    def row(self):
        return self._row

    #TODO: col getter
    @property
    def col(self):
        return self._col
    
    #TODO: active getter and setter
    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    #TODO: occupying getter and setter
    @property
    def occupying(self):
        return self._occupying

    @occupying.setter
    def occupying(self, occupying):
        self._occupying = occupying

    def cmd_to_pos(self, char):
        next_pos = [self._row, self._col]
        if char == 'L':
            next_pos[1] -= 1
        elif char == 'R':
            next_pos[1] += 1
        elif char == 'U':
            next_pos[0] -= 1
        elif char == 'D':
            next_pos[0] += 1
        else:
            print('Invalid Move.')
        return next_pos

    @abstractmethod
    def act(self, map):
        pass

    @abstractmethod
    def interact_with(self, comer):
        pass
    
    def display(self):
        # TODO: return _color followed by _character for displaying 
        return self._color, self._character
        # END TODO 


class Player(GameCharacter):
    def __init__(self, row, col, h, o):
        GameCharacter.__init__(self, row, col)
        self._valid_actions = ['U', 'D', 'R', 'L']
        self._hp = h
        self._oxygen = o
        self._name = 'Player'
        self._character = 'A'

    #TODO: hp getter and setter
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, h):
        self._hp = h

    #TODO: oxygen getter and setter
    @property
    def oxygen(self):
        return self._oxygen

    @oxygen.setter
    def oxygen(self, ox):
        self._oxygen = ox

    def act(self, map):
        next_cell = None
        next_pos = [0, 0]
        while next_cell == None:
            action = input('Next move (U, D, R, L): ')
            # TODO: act method 
            if not (action == 'U' or action == 'D' or action == 'R' or action == 'L'):
                print('Invalid command. Please enter one of {U, D, R, L}.')
                continue

            next_pos = self.cmd_to_pos(action)
            next_cell = map.get_cell(next_pos[0], next_pos[1])
            if next_cell == None:
                continue

            if next_cell.set_occupant(self) == False:
                next_cell = None
                continue
            else:
                self._occupying = map.get_cell(self._row, self._col).remove_occupant()
                self._occupying = next_cell
                self._row = next_pos[0]
                self._col = next_pos[1]
                self._oxygen -= self._occupying.hours

            if self._active == False:
                self._occupying = map.get_cell(self._row, self._col).remove_occupant()
            # END TODO 

    # return whether comer entering the cell successfully or not
    def interact_with(self, comer):
        if comer.name == 'Goblin':
            print('\033[1;31;46mPlayer meets a Goblin! Player\'s HP - %d.\033[0m' %(comer.damage))
             # TODO: interact_with method 
            self._hp -= comer.damage
            comer.active = False
            return False
            # END TODO 


class Goblin(GameCharacter):
    def __init__(self, row, col, actions):
        GameCharacter.__init__(self, row, col)
        self._actions = actions
        self._cur_act = 0
        self._damage = 1
        self._name = 'Goblin'
        self._character = 'G'

    #TODO: damage getter
    @property
    def damage(self):
        return self._damage

    def act(self, map):
        # TODO: act method of a Goblin 
        # get the next cell according to _actions and _cur_act
        next_cell = None
        next_pos = [0, 0]
        action = self._actions[self._cur_act]
        next_pos = self.cmd_to_pos(action)
        next_cell = map.get_cell(next_pos[0], next_pos[1])
        self._cur_act += 1
        if self._cur_act == len(self._actions):
            self._cur_act = 0

        if next_cell != None: 
            if next_cell.set_occupant(self):
                self._occupying = map.get_cell(self._row, self._col).remove_occupant()
                self._occupying = next_cell
                self._row = next_pos[0]
                self._col = next_pos[1]
                print('\033[1;31;46mGoblin enters the cell (%d, %d).\033[0;0m' % (self._row, self._col))

            if not self._active:     
                self._occupying = map.get_cell(self._row, self._col).remove_occupant()

        # END TODO 

    # return whether comer entering the cell successfully or not
    def interact_with(self, comer):
        if comer.name == 'Player':
            print(
                '\033[1;31;46mA goblin at cell (%d, %d) meets Player. The goblin died. Player\'s HP - %d.\033[0;0m'
                % (self._row, self._col, self._damage)
            )
            # TODO: update properties of the player and the Goblin 
            #       return whether the Player successfully enter the cell 
            comer.hp -= self.damage
            self._active = False
            
            if comer.hp == 0:
                comer.active = False
            return True
            # END TODO
