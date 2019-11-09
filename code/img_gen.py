from PIL import Image
import numpy as np
import os
import mapProcessor as mp 

name_dict = {   'block.png':'B',
                'door.png':'D',
                'floor.png':'F',
                'monstor.png':'M',
                'void.png':'-',
                'wall.png':'W',
                'water.png':'P'
            }

def getAllTileImg(path):
    imgs_dic = dict()
    for fileName in os.listdir(path):
        map_arr = readOneTileImg(path,fileName)
        imgs_dic[name_dict[fileName]] = map_arr
    return imgs_dic

def readOneTileImg(path,fileName):
    pic = np.asarray(Image.open(path + "/" + fileName))
    return pic

def showRoom(room,imgs_dic):
    room_img = list()
    for i in range(room.shape[0]):
        line_img = list()
        for j in range(room.shape[1]):
            tile = imgs_dic[room[i][j]]
            if room[i][j] == 'O':
                tile = imgs_dic['F']
            elif room[i][j] == 'I':
                tile = imgs_dic['B']
                
            if type(line_img) == list:
                line_img = tile
            else:
                line_img = np.append(line_img,tile, axis=0)
        if type(room_img) == list:
            room_img = line_img
        else:
            room_img = np.append(room_img,line_img, axis=1)
    img = Image.fromarray(room_img, 'RGB')
    img.show()
    return