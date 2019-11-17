# PCGMM

## Image Generation
Please use the following code to generate your image map
* Be noted that you need to put the icons of tiles into "/data/pics/" folder

'''
import img_gen as ig

imgs_dic = ig.getAllTileImg("../data/pics")
ig.showRoom(m,imgs_dic) // m should be a nparray of the room, normally shape(16,9)
'''