import os
import random
import numpy as np

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

def readMaps(tileTypes):
    maps_path = "../data/TheLegendofZelda/Processed"
    maps_lst = []

    for fileName in os.listdir(maps_path):
        if fileName == "README.txt":
            continue
        amap = []
        # Read this map
        map_f = open(maps_path+"/"+fileName, 'r')
        for row in map_f:
            row_chars = []
            for char in row.rstrip():
                if char not in tileTypes:
                    print(fileName,'Invalid char',char)
                row_chars.append(char)
            amap.append(row_chars)

        map_arr = np.asarray(amap, dtype=str)
        # print(fileName, map_arr.shape)
        maps_lst.append(map_arr)
    
    return maps_lst

def roomSplit(maps_lst):
    room_length = 16
    room_width = 11
    all_rooms = []
    for amap in maps_lst:
        num_a = amap.shape[0]//room_length
        num_b = amap.shape[1]//room_width
        rooms = np.empty((num_a*num_b, room_length,room_width),dtype=object)
        for i in range(num_a):
            for j in range(num_b):
                a_start,a_end = i*room_length, (i+1)*room_length
                b_start,b_end = j*room_width, (j+1)*room_width
                rooms[i*num_a+j] = amap[a_start:a_end,b_start:b_end]
        if type(all_rooms) == list:
            all_rooms = rooms
        else:
            all_rooms = np.append(all_rooms,rooms, axis=0)
        # print(all_rooms.shape)
    return all_rooms


def data_split(maps_data):
    # 80% training, 10% validation, 10% testing
    random.shuffle(maps_data)
    tr_idx = int(0.8*len(maps_data))
    va_length = int(0.1*len(maps_data))

    print(tr_idx,va_length)

    training_data = maps_data[:tr_idx]
    validation_data = maps_data[tr_idx:(tr_idx+va_length)]
    testing_data = maps_data[(tr_idx+va_length):]

    return training_data, validation_data, testing_data