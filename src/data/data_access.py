import h5py
import numpy as np
import os
import tempfile
import shutil

path = '../data/saved_files/'

def create_hdf5_file(filename: str):
    try:
        with h5py.File(path+filename, 'w-') as h5file:
            pass
        
        print(f"Empty HDF5 file '{filename}' created !")
    except OSError:
        print(f"File '{filename}' already exists. No changes made.")

    
def save_to_file(new_tiles, filename: str):
    final_path = path + filename
    
    temp_fd, temp_file_path = tempfile.mkstemp(suffix='.h5')
    
    try:
        os.close(temp_fd)  

        with h5py.File(temp_file_path, 'w') as hf:
            for group in new_tiles:
                print(f"Saving group: {group}")
                
                group_node = hf.create_group(group)
                
                for idx, tile in enumerate(new_tiles[group]):
                    _recursively_save_dict(hf, f"{group_node.name}/{idx}", tile)

    
        shutil.move(temp_file_path, final_path)
        
        print(f"Data successfully saved to '{filename}'")

    except Exception as e:
        print(f"Error while saving '{filename}': {e}")

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file '{temp_file_path}' removed.")

                                            
def _recursively_save_dict(h5file, path, dic):
    
    if not isinstance(dic, dict): 
        dic = dic.to_dict()
    for key, item in dic.items():
        if isinstance(item, dict):
            group = h5file.require_group(f"{path}/{key}")
            _recursively_save_dict(h5file, group.name, item)
        elif isinstance(item, np.ndarray):
            h5file.create_dataset(f"{path}/{key}", data=item)
        else:
            raise TypeError(f"Unsupported type {type(item)} at {path}")


def load_dict(filename: str):
    try:
        with h5py.File(path+filename, 'r') as h5file:
            
            print("\nNow loading full data...\n")
            loaded_dict = _recursively_load_dict(h5file, '/')
        
        print("\nLoaded data:")
        print(loaded_dict)
    except Exception as e:
        print(f"Error while loading {path}: {e}")


def load_tiles_by_id(filename: str, tile_id: str):
    try:
        with h5py.File(path+filename, 'r') as h5file:
            if tile_id not in h5file:
                raise ValueError(f"ID '{tile_id}' not found in the HDF5 file.")
            
            tile_group = h5file[tile_id]
            
            tiles_data = []
            for tile_key in tile_group.keys():
                tile_data = _recursively_load_dict(h5file, f'/{tile_id}/{tile_key}')
                tiles_data.append(tile_data)
    except Exception as e:
        print(f"Error while loading {path}: {e}")
    return tiles_data


def _recursively_load_dict(h5file, path):
    result = {}

    try:
        group = h5file[path]
        
        for key, item in group.items():
            if isinstance(item, h5py.Group):
                result[key] = _recursively_load_dict(h5file, f"{path}/{key}")
            
            elif isinstance(item, h5py.Dataset):
                data = item[()]
                
                if isinstance(data, bytes):
                    data = data.decode()
                
                result[key] = data

    except Exception as e:
        print(f"Error while loading path '{path}': {e}")
            
    return result


        
