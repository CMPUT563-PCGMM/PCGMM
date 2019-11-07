import mapProcessor as mp 



if __name__ == "__main__":
    maps_data = mp.readMaps(mp.tileTypes)
    rooms = mp.roomSplit(maps_data)
    training_data, validation_data, testing_data = mp.data_split(rooms)