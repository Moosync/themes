import os
import shutil
import zipfile
import json
import sys

# Directory path (current directory)
cwd = os.getcwd()

def consolidate_manifest():
    manifest = {}

    # Create 'dist' directory if it doesn't exist
    dist_dir = os.path.join(cwd, 'dist')
    os.makedirs(dist_dir, exist_ok=True)

    # Iterate through all .mstx files in the directory
    for file in os.listdir(cwd):
        if file.endswith(".mstx"):
            try:
                # Treat the .mstx file as a zip file
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    # Check if config.json exists in the zip file
                    if 'config.json' in zip_ref.namelist():
                        # Extract and parse config.json
                        with zip_ref.open('config.json') as config_file:
                            config_data = json.load(config_file)

                            # Remove 'customCSS' from 'theme' if it exists
                            if 'theme' in config_data and 'customCSS' in config_data['theme']:
                                del config_data['theme']['customCSS']

                            # Extract the id and check for conflicts
                            if 'id' in config_data:
                                id_value = config_data['id']
                                if id_value in manifest:
                                    print(f"Error: Conflict detected for ID '{id_value}' in {file}")
                                    sys.exit(1)
                                manifest[id_value] = {"data": config_data}

                                # Copy the .mstx file to the 'dist' directory with the new name
                                new_filename = f"{id_value}.mstx"
                                shutil.copy(file, os.path.join(dist_dir, new_filename))
                            else:
                                print(f"Warning: 'id' missing in {file}'s config.json")
            except zipfile.BadZipFile:
                print(f"Error: {file} is not a valid zip file.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Write the consolidated manifest to manifest.json in 'dist'
    manifest_path = os.path.join(dist_dir, 'manifest.json')
    with open(manifest_path, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=4)

    print(f"Manifest successfully written to {manifest_path}")

if __name__ == "__main__":
    consolidate_manifest()
