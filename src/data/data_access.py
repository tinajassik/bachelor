from model import TileData
import h5py
from dataclasses import asdict
from typing import Optional
import numpy as np

path = '../data/saved_files/'

def create_hdf5_file(filename: str):
    try:
        with h5py.File(path+filename, 'w-') as h5file:
            pass
        
        print(f"Empty HDF5 file '{filename}' created !")
    except OSError:
        print(f"File '{filename}' already exists. No changes made.")

    

def save_to_file(new_tiles, filename: str):
    with h5py.File(path+filename, 'a') as hf:
        for group in new_tiles:
            group_node = hf.create_group(group)
            for idx, tile in enumerate(new_tiles[f'{group}']):
                _recursively_save_dict(hf, f"{group_node.name}/{idx}", tile)

        
        
def _recursively_save_dict(h5file, path, dic):
    print(f"path: {path}")
    if not isinstance(dic, dict): 
        dic = dic.to_dict()
    for key, item in dic.items():
        if isinstance(item, dict):
            group = h5file.require_group(f"{path}/{key}")
            _recursively_save_dict(h5file, group.name, item)
        elif isinstance(item, np.ndarray):
            h5file.create_dataset(f"{path}/{key}", data=item)
        else:
            h5file.create_dataset(f"{path}/{key}", data=item)

def load_dict(filename: str):
    with h5py.File(path+filename, 'r') as h5file:
        
        print("\nNow loading full data...\n")
        loaded_dict = _recursively_load_dict(h5file, '/')
    
    print("\nLoaded data:")
    print(loaded_dict)


def load_tiles_by_id(filename: str, tile_id: str):
    with h5py.File(path+filename, 'r') as h5file:
        if tile_id not in h5file:
            raise ValueError(f"ID '{tile_id}' not found in the HDF5 file.")
        
        tile_group = h5file[tile_id]
        
        tiles_data = []
        for tile_key in tile_group.keys():
            tile_data = _recursively_load_dict(h5file, f'/{tile_id}/{tile_key}')
            tiles_data.append(tile_data)
    
    return tiles_data


def _recursively_load_dict(h5file, path):
    result = {}
    
    group = h5file[path]
    
    for key, item in group.items():
        if isinstance(item, h5py.Group):
            result[key] = _recursively_load_dict(h5file, f"{path}/{key}")
        
        elif isinstance(item, h5py.Dataset):
            data = item[()]
            
            if isinstance(data, bytes):
                data = data.decode()
            
            result[key] = data
            
    return result


        
