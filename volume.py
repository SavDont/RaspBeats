def set_volumes(volumes):
    '''
    set_volumes(volumes) - set volumes dictionary to 127 (max volume) for all keys [1, 2, ..., 7]
    '''
    for i in range(7):
        volumes[i+1] = 127
