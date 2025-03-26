import h5py
import os
import tempfile

path = os.path.join("..","data", "saved_files")
extension = ".h5"

def create_hdf5_file(filename="tile_data"):
    filepath = os.path.join(path, filename + extension)
    try:
        with h5py.File(filepath, 'w-') as h5file:
            pass
        
        print(f"Empty HDF5 file '{filename}' created !")
    except OSError:
        print(f"File '{filename}' already exists. No changes made.")

def save_to_file(new_tiles, filename="tile_data"):
    filepath = os.path.join(path, filename + extension)
    
    temp_fd, temp_file_path = tempfile.mkstemp(suffix='.h5')
    
    try:
        os.close(temp_fd) 
        
        with h5py.File(temp_file_path, 'w') as temp_hf:
            for group in new_tiles:
                print(f"Saving group: {group}")
                
                group_node = temp_hf.create_group(group)

                for idx, tile in enumerate(new_tiles[group]):
                    _recursively_save_dict(temp_hf, f"{group_node.name}/{idx}", tile)
        
        os.remove(temp_file_path)

        with h5py.File(filepath, 'a') as original_hf:
            for group in new_tiles:
                print(f"Appending group: {group}")
                
                if group not in original_hf:
                    group_node = original_hf.create_group(group)
                else:
                    group_node = original_hf[group]

                for idx, tile in enumerate(new_tiles[group]):
                    _recursively_save_dict(original_hf, f"{group_node.name}/{idx}", tile)

        print(f"Data successfully appended to '{filename}'")

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
        else:
            h5file.create_dataset(f"{path}/{key}", data=item)


def load_dict(filename="tile_data"):
    filepath = os.path.join(path, filename + extension)
    try:
        with h5py.File(filepath, 'r') as h5file:
            
            print("\nNow loading full data...\n")
            loaded_dict = _recursively_load_dict(h5file, '/')
        
        print("\nLoaded data:")
        print(loaded_dict)
    except Exception as e:
        print(f"Error while loading {path}: {e}")


def load_tiles_by_id(tile_id: str, filename="tile_data"):
    filepath = os.path.join(path, filename + extension)
    try:
        with h5py.File(filepath, 'r') as h5file:
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

def save_fetched_item(item_id, item_metadata, filename="split_tiles"):
    filepath = os.path.join(path, filename + extension)

    with h5py.File(filepath, "a") as hf:
        if item_id in hf:
            print(f"Group '{item_id}' already exists. Replacing it...")
            del hf[item_id]

        item_group = hf.create_group(item_id)

        metadata_group_path = f"{item_group.name}/item_metadata"
        _recursively_save_dict(hf, metadata_group_path, item_metadata)

        print(f"Structure for '{item_id}' with item_metadata saved in {filename}.\n")
    
def add_tile_to_item(item_id, tile_metadata, tile_id, filename="split_tiles"):
    filepath = os.path.join(path, filename + extension)

    with h5py.File(filepath, "a") as hf:
        if item_id not in hf:
            print(f"Item '{item_id}' not found in {filepath}. Cannot add tile.")
            return

        item_group = hf[item_id]

        tile_group_name = f"tile_{tile_id}"
        if tile_group_name in item_group:
            del item_group[tile_group_name]

        tile_group = item_group.create_group(tile_group_name)

        _recursively_save_dict(hf, tile_group.name, tile_metadata)

def load_item_by_id(item_id, filename="split_tiles"):
    filepath = os.path.join(path, filename + extension)

    with h5py.File(filepath, "r") as hf:
        if item_id not in hf:
            print(f"Item '{item_id}' not found in {filename}.")
            return None

        item_group_path = hf[item_id].name

        return _recursively_load_dict(hf, item_group_path)