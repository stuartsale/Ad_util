import numpy as np
import json
import math
import glob

def sorted_dict_make(dirname=""):

    map_list=glob.glob("*_map.json")
    map_list.sort()

    for map_name in map_list:

        sorted_dict={}

     	with (open('{0:s}{1:s}_map.json'.format(dirname, map_name)) 
              as f):
            map_dict = json.load(f)

        for filename in map_dict:

            for x in range(map_dict[filename]["x_min"], 
                           map_dict[filename]["x_max"]+1):
                for y in range(map_dict[filename]["y_min"], 
                               map_dict[filename]["y_max"]+1):

                    sorted_dict[(x,y)] = filename

     	with (open('{0:s}{1:s}_map_sorted.json'.format(dirname, 
              map_name)) as f):
            json.dump(sorted_dict, f)        
            
