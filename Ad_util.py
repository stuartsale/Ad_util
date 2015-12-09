import numpy as np
import json
import math
import glob
import itertools
from os import path

def sorted_dict_make(dirname="data/"):

    map_list=glob.glob("{0:s}*_map.json".format(dirname))
    map_list.sort()

    for map_fullname in map_list:
        map_dir, map_name = path.split(map_fullname)
        print map_name, map_dir

        sorted_names=[ [ [] for c in range(60) ] for r in range(60) ]

     	with open(map_fullname) as f:
            map_dict = json.load(f)

        for filename in map_dict:

            for x in range(map_dict[filename]["x_min"], 
                           map_dict[filename]["x_max"]+1):
                for y in range(map_dict[filename]["y_min"], 
                               map_dict[filename]["y_max"]+1):

                    sorted_names[x][y] = filename

     	with open(path.join(map_dir, '{0:s}_map_sorted.json'.format(
                  map_name.split("_")[0])), "w") as f:
            json.dump(sorted_names, f)   

class map_regions:

    """ class for querying which map file is associated with
        a certain position on the sky.
    """

    def __init__(self, dirname="data/"):

        base_dir = _dir = path.dirname(__file__)

        self.dirname = path.join(base_dir,dirname)
        self.map_dicts = {}

    def query(self, l, b):

        # check we just have single floats for l&b
        if isinstance(l, float) and isinstance(b, float):

            # get the block
            if l<215 and l>=30:
                l_block = int(l/5.+0.5)*5
            else:
                raise ValueError("l out of range covered by map")

            if b<0 and b>-5:
                b_block = "a"
            elif b>=0 and b<5:
                b_block = "b"
            else:
                raise ValueError("b out of range covered by map")

            blockname = "{0:d}{1:s}".format(l_block, b_block)

            # if block's dict hasn't been loaded, load it
            if blockname not in self.map_dicts:

            	with open(path.join(self.dirname, 
                     '{0:s}_map_sorted.json'.format(blockname))) as f:
    	            self.map_dicts[blockname] = json.load(f) 

            x = int((l%5)*12+0.5)
            y = int((b%5)*12+0.5)

            return self.map_dicts[blockname][x][y]
            
