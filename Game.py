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

    def cycle(self):
        player1 = self.player1
        print("Turn:", player1)
        if player1: #--------->player 1
            if self.boot:
                _,in_pocket = minmax(self,self.mode,-50000,50000,True)         #------------------------------------->rg3y el Ai INPUT hena (1)
                print(in_pocket)
            else:
                user_in = input("choose a pocket (0:5) or q: ")
                if user_in == "q":
                    self.save_game['state_list']=self.game_list
                    self.save_game['player'] = self.player1
                    file = open("last.txt","a")
                    file.write(str(self.save_game))
                    file.close()
                    return 1 ,"game saved"
                elif int(user_in) < 13 :
                    in_pocket = int(user_in)#---------------------------------------------------->input player 1
                else:
                    return 1, "wrong input (not q or pocket)"
            pocket = in_pocket
            self.switch_player()
            if pocket <= 5:
                if self.game_list[pocket] != 0:
                    stones = self.game_list[pocket]
                    loop_counter = 1
                    next_pocket = 0
                    while(stones>0):
                        if next_pocket <13 and loop_counter<13:
                            next_pocket =  pocket+loop_counter
                            loop_counter+=1
                            if next_pocket != 13:
                                self.game_list[next_pocket] = self.game_list[next_pocket] + 1
                                stones-=1
                            
                        else:
                            next_pocket = 0
                            pocket = 0
                            loop_counter = 0
                        
                        if stones == 0 and next_pocket == 6:
                            if self.end(self.game_list)[0] == 0 :
                                self.switch_player()
                        #steeeeeeeeeeeealinggggggggggggggggggggggggggggg
                        if self.stealing:
                            if stones == 0 and next_pocket<6 and self.game_list[next_pocket] == 1:
                                self.steal(next_pocket)
                               
                                    
                    self.game_list[in_pocket] = 0
                    if self.end(self.game_list)[0] == 0:
                        self.printBoard(self.game_list)
                        return 0 ,"board printed"
                    else:
                        #print("22222")
                        self.last_score = self.end(self.game_list)[1]
                        self.printBoard(self.game_list)
                        print("game finished")
                        print("last score: ",self.last_score)
                        return   1,self.last_score,self.game_list
                        
                else:
                    self.switch_player()
                    state ="empty pocket pick another one"
                    print(state)
                    return 0, state
            else:
                self.switch_player()
                state = "wrong pocket input"
                print(state) # valid       7:12
                return 0,state
        
        elif not player1: #--------->player 2
            if not self.boot:
                _,in_pocket = minmax(self,self.mode,-50000,50000,True)  
                print(in_pocket)       #------------------------------------->rg3y el Ai INPUT hena (2)
            else:
                user_in = input("choose a pocket (7:12) or q: ")
                if user_in == "q":
                    self.save_game['state_list']=self.game_list
                    self.save_game['player'] = self.player1
                    file = open("last.txt","a")
                    file.write(self.save_game)
                    file.close()
                    return 1 ,"game saved"
                elif int(user_in) <13 :
                    in_pocket = int(user_in)
                else:
                    return 1, "wrong input (not q or pocket)"
            pocket = in_pocket
            self.switch_player()
            if pocket in range(7,13):
                if self.game_list[pocket] != 0:
                    stones = self.game_list[pocket]
                    loop_counter = 1
                    next_pocket = 0
                    while(stones>0):
                        if next_pocket <13 and loop_counter<13:
                            next_pocket =  pocket+loop_counter
                            loop_counter+=1
                            if next_pocket != 6:
                                self.game_list[next_pocket] = self.game_list[next_pocket] + 1
                                stones-=1
                        else:
                            next_pocket = 0
                            pocket = 0
                            loop_counter = 0
                            
                        
                        if stones==0 and next_pocket == 13:
                                if self.end(self.game_list)[0] == 0 :
                                    self.switch_player()
                        
                        #steeeeeeeeeeeealinggggggggggggggggggggggggggggg
                        if self.stealing:
                            if stones == 0 and next_pocket in range(7,13) and self.game_list[next_pocket] == 1:
                                self.steal(next_pocket)
                                
                    self.game_list[in_pocket] = 0
                    
                    if self.end(self.game_list)[0] == 0:
                        self.printBoard(self.game_list)
                        # return self.game_list
                        return 0 ,"board printed"
                    else:
                        #print("1111")
                        self.last_score = self.end(self.game_list)[1]
                        self.printBoard(self.game_list)
                        print("game finished")
                        print("last score: ",self.last_score)
                        return   1,self.last_score
                        
                else:
                    self.switch_player()
                    state ="empty pocket pick another one"
                    print(state)
                    return 0, state
            else:
                self.switch_player()
                state = "wrong pocket input"
                print(state) # valid       7:12
                return 0,state
    def cost(self,check_list):
            if self.end(check_list)[0]:
                if check_list[0]>check_list[6]:
                    return 50
                elif check_list[13]==check_list[6]:
                    return 0
                else :
                    return -50
            else:
                return check_list[13]- check_list[6]

    def steal(self,last_pocket):
        if last_pocket < 6:
            self.game_list[6] += self.game_list[12-last_pocket]+1
            self.game_list[12-last_pocket] = 0
            self.game_list[ last_pocket] = 0
        elif last_pocket > 6:
            self.game_list[13] += self.game_list[12-last_pocket]+1
            self.game_list[12-last_pocket] = 0
            self.game_list[ last_pocket] = 0

    def next_move(self, pocket):
        j=pocket
        againturn=False
        add=self.game_list[j]
        self.game_list[j] = 0
        if pocket>6:
            stones = add
            while(stones>0):
                pocket+=1
                pocket=pocket % 14
                if pocket==6 : continue
                else:
                    self.game_list[pocket%14]+=1
                stones-=1
            if pocket>6 and self.game_list[pocket]==1 and pocket!=13 and self.game_list[5-(pocket-7)]!=0:
                self.game_list[13]+=1+self.game_list[5-(pocket-7)]
                self.game_list[pocket]=0
                self.game_list[5-(pocket-7)]=0
            if pocket==13:
                againturn = True
        else:
            stones = add
            while (stones > 0):
                pocket += 1
                pocket = pocket % 14
                if pocket == 13:
                    continue
                else:
                    self.game_list[pocket%14] += 1
                stones -= 1
            if pocket < 6 and self.game_list[pocket] == 1 and pocket !=6 and self.game_list[-pocket + 12]!=0:
                self.game_list[6] += 1 + self.game_list[-pocket + 12]
                self.game_list[pocket] = 0
                self.game_list[-pocket + 12] = 0
            if pocket == 6:
                againturn = True
        return againturn
def minmax(state, depth, alpha, beta , Min_Max=True):
# recursion stop conditions
    if depth == 0 or state.end(state.game_list)[0]:
        return state.cost(state.game_list),-1
    #true -> max
    if Min_Max == True:
        old_alpa = -50000
        bowl = -1
        if state.player1:
            start=0
            end =6
        else:
            start=7
            end =13
        for i in range(start,end):
            if state.game_list[i]==0: 
                continue
            s=Game()
            s.game_list = state.game_list[:]
            Min_Max = s.next_move(i)
            new_alpha,_ =  minmax(s, depth-1, alpha, beta, Min_Max)
            if old_alpa< new_alpha:
                bowl=i
                old_alpa =new_alpha
            alpha = max(alpha, old_alpa)
            if alpha >= beta :
                break
        return old_alpa, bowl
    else:
        old_beta = 50000
        bowl = -1
        for i in range(0, 6):
            if state.game_list[i] == 0: 
                continue
            s = Game()
            s.game_list = state.game_list[:]
            Min_Max = s.next_move(i)
            new_beta,_ = minmax(s, depth - 1, alpha, beta, not  Min_Max)
            if old_beta > new_beta:
                bowl = i
                old_beta = new_beta
            beta = min(beta, old_beta)
            # cut off condition
            if alpha >= beta:
                break
        return old_beta, bowl

bot=int(input('1 for player2 , 0 for player1 : '))# boot 1(plyer1) -> player2 
stl =int(input('1 for stealing or 0 for without :'))
mode=input('enter 0 for easy mode or 1 for hard mode : ')
if mode =='1':
    mod= 3
else:
    mod=15
g1 = Game(stealing=stl,boot=bot,mode=mod)
cont_in = int(input("continue last game? (enter 1,0): "))
if cont_in ==1:
    f = open("last.txt", "r")
    read = ast.literal_eval(f.read())
    board_start = read['state_list']
    g1.player1 = read['player']
    
else:
    board_start = [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
g1.game_list = board_start
g1.printBoard(board_start) #draw first state 

while(1):
    x = g1.cycle()
    #print(x)
    if x[0] ==1 :
        print(x[1])
        break
