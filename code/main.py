import mapProcessor as mp 
import img_gen as ig
import numpy as np
from mrf import MRF

if __name__ == "__main__":
    maps_data = mp.readMaps("../data/CMPUT563_Change_tile/Processed_changed_tiles_reduced_OI")
    rooms = mp.roomSplit(maps_data)
    training_data, validation_data, testing_data = mp.data_split(rooms)
    imgs_dic = ig.getAllTileImg("../data/pics")

    # swap each location _b times
    mrf = MRF(_b = 9999)
    mrf.train(training_data)
    m = mrf.sample(imgs_dic)
    ig.showRoom(m,imgs_dic)

    # for style
    sampling_param_dict = mrf.getRoomLogLike(m)
    training_param_dict = mrf.getTrainAvgLogLike(training_data)