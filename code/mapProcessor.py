import os
import random
import numpy as np

'''
    In terms of functionality,
    'F' = 'O'
    'B' = 'I'
    'M' = 'P'
'''
tileTypes = {
    "F": "FLOOR",
    "B": "BLOCK",
    "M": "MONSTER",
    "P": "ELEMENT (LAVA, WATER)",
    "O": "ELEMENT + FLOOR (LAVA/BLOCK, WATER/BLOCK)",
    "I": "ELEMENT + BLOCK",
    "D": "DOOR",
    "S": "STAIR",
    "W": "WALL",
    "-": "VOID"
}

ROOMHEIGHT = 16
ROOMWIDTH = 11

def readMaps(maps_path):
    '''
    Reads all maps in the path
    '''
    maps_lst = []
    for fileName in os.listdir(maps_path):
        if fileName == "README.txt":
            continue
        map_arr = readOneMap(maps_path,fileName)
        maps_lst.append(map_arr)
    return maps_lst

def readOneMap(maps_path,fileName):
    amap = []
    map_f = open(maps_path+"/"+fileName, 'r')
    for row in map_f:
        row_chars = []
        for char in row.rstrip():
            if char not in tileTypes:
                print(fileName,'Invalid char',char)
            row_chars.append(char)
        amap.append(row_chars)
    return np.asarray(amap, dtype=str)

def roomSplit(maps_lst):
    '''
    returns a nparray of all valid rooms
    shape: (num_of_rooms, ROOMHEIGHT, ROOMWIDTH)
    '''
    all_rooms = []
    for amap in maps_lst:
        num_a = amap.shape[0]//ROOMHEIGHT
        num_b = amap.shape[1]//ROOMWIDTH
        rooms = list()
        # rooms = np.empty((num_a*num_b, ROOMHEIGHT,ROOMWIDTH),dtype=object)
        for i in range(num_a):
            for j in range(num_b):
                a_start,a_end = i*ROOMHEIGHT, (i+1)*ROOMHEIGHT
                b_start,b_end = j*ROOMWIDTH, (j+1)*ROOMWIDTH
                if amap[a_start,b_start] != "-":
                    room = amap[a_start:a_end,b_start:b_end]
                    room = room.reshape((1,room.shape[0],room.shape[1]))
                    if type(rooms) == list:
                        rooms = room
                    else:
                        rooms=np.append(rooms,room,axis=0)
        # print(rooms.shape)
        if type(all_rooms) == list:
            all_rooms = rooms
        else:
            all_rooms = np.append(all_rooms,rooms, axis=0)
    print(all_rooms.shape)
    return all_rooms

def data_split(maps_data):
    # 80% training, 10% validation, 10% testing
    random.shuffle(maps_data)
    tr_idx = int(0.8*len(maps_data))
    va_length = int(0.1*len(maps_data))

    # print(tr_idx,va_length)
    training_data = maps_data[:tr_idx]
    validation_data = maps_data[tr_idx:(tr_idx+va_length)]
    testing_data = maps_data[(tr_idx+va_length):]

    return training_data, validation_data, testing_data

def highLevelMapConv(ml,d,z,Th):
    for y in range(ml.shape[0]//ROOMHEIGHT):
        for x in range(ml.shape[1]//ROOMWIDTH):
            pass

# def 