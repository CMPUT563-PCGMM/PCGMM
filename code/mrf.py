import mapProcessor as mp 
import img_gen as ig
import numpy as np
import random
import math 

class MRF:
    def __init__(self, _b=999999):
        self.height = mp.ROOMHEIGHT
        self.width = mp.ROOMWIDTH
        self.thick = mp.ROOMBORDER
        self.IT = mp.indoor_tileTypes
        self.BT = mp.border_tileTypes
        self.BorderProbCount = [dict(),dict(),dict(),dict()]
        self.BorderProb = [dict(),dict(),dict(),dict()]
        self.b = _b
        # network structure P(Sx,y |Sx−1,y, Sx+1,y, Sx,y−1, Sx,y+1)
        self.S = dict()
        self.P = dict()
        self.S_pos = dict()
        self.P_pos = dict()

    def getConfig(self,i,j,room):
        sleft = room[i-1][j]
        sright = room[i+1][j]
        stop = room[i][j-1]
        sbtm = room[i][j+1]
        config = str(i)+"_"+str(j)+sleft+sright+stop+sbtm
        # config = sleft+sright+stop+sbtm
        return config

    def train(self, training_data):
        # find border probabilities
        num_rooms=len(training_data)
        for room in training_data:
            doors = list()
            doors= [room[1,5],room[-2,5],room[7,1],room[7,-2]]
            for i in range(len(doors)):
                if doors[i] not in self.BorderProbCount[i].keys():
                    self.BorderProbCount[i][doors[i]]=1
                else:
                    self.BorderProbCount[i][doors[i]]+=1

        for i in range(len(self.BorderProbCount)):
            for tile in self.BorderProbCount[i].keys():
                self.BorderProb[i][tile]=self.BorderProbCount[i][tile]/num_rooms
        
        # find indoor probabilities
        for room in training_data:
            for i in range(self.thick,self.height-self.thick):
                for j in range(self.thick,self.width-self.thick):
                    t = room[i][j]
                    config = self.getConfig(i,j,room)
                    pos = str(i)+"_"+str(j)
                    if config not in self.S.keys():
                        self.S[config] = {t:1}
                    elif t not in self.S[config].keys():
                        self.S[config][t] = 1
                    else:
                        self.S[config][t] += 1
                    
                    if pos not in self.S_pos.keys():
                        self.S_pos[pos] = {t:1}
                    elif t not in self.S_pos[pos].keys():
                        self.S_pos[pos][t] = 1
                    else:
                        self.S_pos[pos][t] += 1
        # print(self.S)

        for c in self.S.keys():
            _sum = sum(self.S[c].values())
            for t in self.S[c].keys():
                self.P[t+c] = self.S[c][t]/_sum
        # print(len(self.P))

        for pos in self.S_pos.keys():
            _sum = sum(self.S_pos[pos].values())
            pos_t = dict()
            for t in self.S_pos[pos].keys():
                pos_t[t] = self.S_pos[pos][t]/_sum
            self.P_pos[pos] = pos_t
        # print(self.P_pos)
        return

    # Future work: can also bulid a Markov model for the border
    def sampleBorder(self):
        m = np.empty([self.height, self.width], dtype = str)
        m[:] = 'W'
        for i in range(4):
            # door = random.choice(list(self.BT.keys()))
            from numpy.random import choice
            door = choice(list(self.BorderProb[i].keys()), 1,
              p=list(self.BorderProb[i].values()))
            m[mp.door_loc[i]]=door
        return m

    def sample(self,imgs_dic): 
        m = self.sampleBorder()

        for i in range(self.thick,self.height-self.thick):
            for j in range(self.thick,self.width-self.thick):
                # m[i][j] = random.choice(list(self.IT.keys()))
                pos = str(i)+"_"+str(j)
                pos_t = self.P_pos[pos]
                pos_t_new = list()
                sorted_pos_t = sorted(pos_t, key=pos_t.get,reverse=True)
                sorted_values = sorted(pos_t.values(),reverse=True)

                randpick = random.random()
                for idx in range(len(sorted_pos_t)):
                    if randpick < sum(sorted_values[:idx+1]):
                        # print(randpick,sum(sorted_values[:idx+1]),sorted_pos_t[idx])
                        m[i,j] = sorted_pos_t[idx]
                        break

        ig.showRoom(m,imgs_dic)

        bool_pos_select = np.zeros((self.height,self.width))
        j = 0
        BORDER_COUNT = 92
        while j <=self.b:
            while np.count_nonzero(bool_pos_select==0)>=BORDER_COUNT+2:
                # print(np.count_nonzero(bool_pos_select==0))
                h1,w1 = random.randint(self.thick,self.height-self.thick-1),random.randint(self.thick,self.width-self.thick-1)
                h2,w2 = random.randint(self.thick,self.height-self.thick-1),random.randint(self.thick,self.width-self.thick-1)
                bool_pos_select[h1,w1]=1
                bool_pos_select[h2,w2]=1
                # print(h1,w1,h2,w2)

                t1,t2 = m[h1,w1],m[h2,w2]
                if t1 != t2:
                    # ig.showRoom(m,imgs_dic)
                    L_pre = self.getLogLike(h1,w1,h2,w2,m)
                    m = self.swapTile(h1,w1,h2,w2,m)
                    L_post = self.getLogLike(h2,w2,h1,w1,m)
                    prob = min(1,math.exp(L_post-L_pre))
                    do_swap = (random.random() <= prob)
                    # print(do_swap)
                    # print(prob,L_pre,L_post)
                    # ig.showRoom(m,imgs_dic)
                    # input()
                    if not do_swap:
                        m = self.swapTile(h1,w1,h2,w2,m)
            j+=1
        # print(m)
        return m

    def getLogLike(self,h1,w1,h2,w2,m):
        # tile1 and tile2
        t1,t2 = m[h1,w1],m[h2,w2]
        c1,c2 = self.getConfig(h1,w1,m),self.getConfig(h2,w2,m)
        L_1 = 0.001
        if t1+c1 in self.P.keys():
            L_1 = self.P[t1+c1]
            # print('L1',t1+c1,L_1)
        L_2 = 0.001 
        if t2+c2 in self.P.keys():
            L_2 = self.P[t2+c2]
            # print('L2',t2+c2,L_2)
            
        L = math.log(L_1)+math.log(L_2)
        # print('L',L_1*L_2, L)
        return L

    def swapTile(self,h1,w1,h2,w2,m):
        t1,t2 = m[h1,w1],m[h2,w2]
        # print(t1,t2)
        # print(h1,w1,h2,w2)
        m_new = m.copy()
        m_new[h2,w2] = t1
        m_new[h1,w1] = t2

        return m_new

    def getRoomLogLike(self,m):
        room_ll_dict = dict()
        for i in range(self.thick,self.height-self.thick):
            for j in range(self.thick,self.width-self.thick):
                pos = str(i)+"_"+str(j)
                t = m[i][j]
                c = self.getConfig(i,j,m)
                L = 0.00001
                if t+c in self.P.keys():
                    L = self.P[t+c]
                room_ll_dict[pos]=math.log(L)
        return room_ll_dict

    def getTrainAvgLogLike(self,rooms):
        import pandas as pd

        dicts = list()
        for m in rooms:
            room_ll_dict = self.getRoomLogLike(m)
            dicts.append(room_ll_dict)
        
        df = pd.DataFrame(dicts)
        return dict(df.mean())