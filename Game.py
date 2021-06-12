import ast

class Game:
# ---------------------------------------------------------------------------------
# |            |  (12)  |  (11)  |  (10)  |  (9)   |  (8)   |  (7)   |            |
# |            |   1    |   2    |   3    |   4    |   5    |   6    |            |
# |            |        |        |        |        |        |        |            |
# |    (13)    |-----------------------------------------------------|    (6)     |
# |            |-----------------------------------------------------|            |
# |            |        |        |        |        |        |        |            |
# |            |   6    |   5    |   4    |   3    |   2    |   1    |            |
# |            |  (0)   |  (1)   |  (2)   |  (3)   |  (4)   |  (5)   |            |
# ---------------------------------------------------------------------------------
    def __init__(self, mode=10, player1=True, stealing=False, boot=False):
        '''
        @boot = True ------------> boot is player 1, False ---------------> boot is player 2
        '''
        self.game_list = []
        self.start_state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.game_list = self.start_state
        self.player1 = player1
        self.stealing = stealing
        self.last_score = (0, 0)
        self.boot = boot
        self.save_game = {}
        self.mode = mode

    def end(self, check_list):
        if sum(check_list[0:6]) == 0:
            score = (check_list[6], check_list[13] + sum(check_list[7:13]))
            return 1, score
        if sum(check_list[7:13]) == 0:
            score = (check_list[6] + sum(check_list[0:6]), check_list[13])
            return 1, score
        else:
            return 0, (0, 0)

    def switch_player(self):
        if self.player1 == True:
            self.player1 = False
        else:
            self.player1 = True
    def printBoard(self,state):
        print("---------------------------------------------------------------------------------")
        print("|            |        |        |        |        |        |        |            |")
        print("|            |   "+str(state[12])+"    |   "+str(state[11])+"    |   "+str(state[10])+"    |   "+str(state[9])+"    |   "+str(state[8])+"    |   "+str(state[7])+"    |            |")
        print("|            |        |        |        |        |        |        |            |")
        print("|     "+str(state[13])+"      |-----------------------------------------------------|     "+str(state[6])+"      |")
        print("|            |-----------------------------------------------------|            |")
        print("|            |        |        |        |        |        |        |            |")
        print("|            |   "+str(state[0])+"    |   "+str(state[1])+"    |   "+str(state[2])+"    |   "+str(state[3])+"    |   "+str(state[4])+"    |   "+str(state[5])+"    |            |")
        print("|            |        |        |        |        |        |        |            |")
        print("---------------------------------------------------------------------------------")
