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

# Duck Typing
class Trap:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._occupying = None
        self._name = 'Trap'

    # TODO: _occupying get and setter
    @property
    def occupying(self):
        return self._occupying
    
    @occupying.setter
    def occupying(self, occupying):
        self._occupying = occupying

    # TODO: _name getter
    @property
    def name(self):
        return self._name

    def interact_with(self, comer):
        # TODO: Add game logic.
        self._occupying = None
        if comer.name == 'Goblin':
            print('\033[1;31;43mA goblin entered a trap at (%d, %d)and died.\033[0;0m' % (self._row, self._col))
            # TODO: Add game logic.
            comer.active = False
            return False
        elif comer.name == 'Player':
            print('\033[1;31;43mYou entered a trap at (%d, %d)! HP - 1.\033[0;0m' % (self._row, self._col))
            # TODO: Add game logic.
            comer.oxygen -= 1
            comer.hp -= 1
            return True


    def display(self):
        # TODO: Add display logic.
        return ' '
