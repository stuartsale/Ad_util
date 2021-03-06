from __future__ import print_function, division
import glob
import itertools
import json
import math
import numpy as np
from os import path


def sorted_dict_make(dirname="data/"):

    """ sorted_dict_make(dirname="data/")


        Parameters
        ----------
        dirname : string, optional
            the location of the directory containing the data
            files.

    """

    map_list = glob.glob("{0:s}*_map.json".format(dirname))
    map_list.sort()

    for map_fullname in map_list:
        map_dir, map_name = path.split(map_fullname)
        print(map_name, map_dir)

        sorted_names = [[[] for c in range(60)] for r in range(60)]

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

    """ Class map_regions

        A class for querying which map file is associated with
        a certain position on the sky.

        Each object stores the data containing dictionaries
        it needs.
    """

    def __init__(self, dirname="data/"):
        """ __init__(dirname="data/")

            Initialise a map_regions object.

            Parameters
            ----------
            dirname : string, optional
                the location of the directory containing the
                data files.
        """

        base_dir = _dir = path.dirname(__file__)

        self.dirname = path.join(base_dir, dirname)
        self.map_dicts = {}

    def query(self, gal_l, gal_b):
        """ query(gal_l, gal_b)

            Find the filename(s) which contain the extinction
            distance relationships for some galactic
            coordinate(s).

            Parameters
            ----------
            gal_l : float, ndarray(float)
                    The galactic longitude(s)
            gal_b : float, ndarray(float)
                    The galactic latitude(s)

            Returns
            -------
            filenames : ndarray(string)
                The filename(s) where the extinction-distance
                relationships for the relevant coordinates
                can be found.
        """

        # check we just have single floats for l&b
        if isinstance(gal_l, float) and isinstance(gal_b, float):

            # get the block
            if gal_l < 215 and gal_l >= 30:
                l_block = int(l/5.)*5
            else:
                raise ValueError("gal_l out of range covered by map")

            if gal_b < 0 and gal_b > -5:
                b_block = "a"
            elif gal_b >= 0 and gal_b < 5:
                b_block = "b"
            else:
                raise ValueError("gal_b out of range covered by map")

            blockname = "{0:0>3d}{1:s}".format(l_block, b_block)

            # if block's dict hasn't been loaded, load it
            if blockname not in self.map_dicts:

                with open(path.join(self.dirname,
                          '{0:s}_map_sorted.json'.format(blockname))) as f:
                    self.map_dicts[blockname] = np.array(json.load(f))

            x = int((gal_l % 5) * 12)
            y = int((gal_b % 5) * 12)

            return self.map_dicts[blockname][x][y]

        if isinstance(l, np.ndarray) and isinstance(b, np.ndarray):

            # get the blocks
            if np.min(gal_l) >= 30 and np.max(gal_l) < 215:
                l_block = np.floor(gal_l/5.).astype(int)*5
            else:
                raise ValueError("gal_l out of range covered by map")

            if np.min(gal_b) >= -5 and np.max(gal_b) < 5:
                b_block = np.empty(gal_b.shape, dtype=str)
                b_block[gal_b < 0] = "a"
                b_block[gal_b >= 0] = "b"
            else:
                raise ValueError("gal_b out of range covered by map")

            blocknames = np.core.defchararray.add(l_block.astype(str),
                                                  b_block)

            for i in range(blocknames.size):
                blocknames[i] = "{0:0>4s}".format(blocknames[i])

            x = np.floor((gal_l % 5) * 12).astype("int")
            y = np.floor((gal_b % 5) * 12).astype("int")

            filenames = np.empty(b.shape, dtype=object)

            done_blocks = []

            # check to see if required dict(s) have been loaded
            for blockname in blocknames:
                if blockname not in self.map_dicts:
                    # if not load it
                    with open(path.join(self.dirname,
                              '{0:s}_map_sorted.json'.format(blockname))) as f:
                        self.map_dicts[blockname] = np.array(json.load(f))

                if blockname not in done_blocks:
                    rows = (blocknames == blockname)
                    filenames[rows] = (
                        self.map_dicts[blockname][x[rows], y[rows]])

                done_blocks.append(blockname)

            return filenames
