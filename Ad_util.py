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


            
