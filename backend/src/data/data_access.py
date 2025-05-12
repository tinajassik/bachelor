import h5py
import os
import tempfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DIR_PATH = os.path.join(BASE_DIR, "data")

def create_hdf5_file(save_dir=DIR_PATH, filename="tile_data"):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir, exist_ok=True) # exist_ok=True is good practice
            print(f"data_access.py: Directory '{save_dir}' ensured/created.")
        except Exception as e:
            print(f"data_access.py: Error creating directory '{save_dir}': {e}")
            return # Cannot proceed if directory creation fails
    else:
        print(f"data_access.py: Directory '{save_dir}' already exists.")

    file_path = os.path.join(save_dir, filename + ".h5")
    print(f"data_access.py: Checking for HDF5 file at: {file_path}")

    if not os.path.exists(file_path):
        print(f"data_access.py: File '{file_path}' does not exist. Attempting to create.")
        try:
            with h5py.File(file_path, 'w') as hf: # 'w' creates or truncates
                # Create an empty group or dataset if needed, or just leave it empty
                hf.create_group("stac_ids") # Example: create a root group
            print(f"data_access.py: HDF5 file '{file_path}' created successfully with a 'stac_ids' group.")
        except Exception as e:
            print(f"data_access.py: Error creating HDF5 file '{file_path}': {e}")
    else:
        print(f"data_access.py: File '{file_path}' reported as existing by os.path.exists().")
        print(f"data_access.py: Is it a file? {os.path.isfile(file_path)}")
        print(f"data_access.py: Is it a directory? {os.path.isdir(file_path)}")
        try:
            # Try to open in append mode to see if it's a valid HDF5 file we can access
            with h5py.File(file_path, 'a') as hf:
                if "stac_ids" not in hf:
                    hf.create_group("stac_ids")
                    print(f"data_access.py: Opened existing file '{file_path}' and ensured 'stac_ids' group exists.")
                else:
                    print(f"data_access.py: Successfully opened existing file '{file_path}' in append mode. 'stac_ids' group found.")
        except Exception as e:
            print(f"data_access.py: Error opening/validating existing HDF5 file '{file_path}' in append mode: {e}")
            print(f"data_access.py: This could mean it's not a valid HDF5 file, a directory, or a permissions issue despite os.path.exists() being true.")


def save_to_file(new_tiles, save_dir=DIR_PATH,filename="tile_data"):
    file_path = os.path.join(save_dir, filename + ".h5")
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

        with h5py.File(file_path, 'a') as original_hf:
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


def load_dict(save_dir=DIR_PATH,filename="tile_data"):
    file_path = os.path.join(save_dir, filename + ".h5")
    try:
        with h5py.File(file_path, 'r') as h5file:

            print("\nNow loading full data...\n")
            loaded_dict = _recursively_load_dict(h5file, '/')

        print("\nLoaded data:")
        print(loaded_dict)
        return loaded_dict
    except Exception as e:
        print(f"Error while loading {file_path}: {e}")


def load_tiles_by_id(tile_id: str, save_dir=DIR_PATH,filename="tile_data"):
    file_path = os.path.join(save_dir, filename + ".h5")
    try:
        with h5py.File(file_path, 'r') as h5file:
            if tile_id not in h5file:
                raise ValueError(f"ID '{tile_id}' not found in the HDF5 file.")

            tile_group = h5file[tile_id]

            tiles_data = []
            for tile_key in tile_group.keys():
                tile_data = _recursively_load_dict(h5file, f'/{tile_id}/{tile_key}')
                tiles_data.append(tile_data)
    except Exception as e:
        print(f"Error while loading {file_path}: {e}")
    return tiles_data

def get_all_stac_ids(save_dir=DIR_PATH,filename="tile_data"):
    file_path = os.path.join(save_dir, filename + ".h5")
    try:
        with h5py.File(file_path, 'r') as h5file:
            ids = list(h5file.keys())
            print(f"Found IDs: {ids}")
            return ids
    except Exception as e:
        print(f"Error while reading IDs from '{file_path}': {e}")
        return []

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
