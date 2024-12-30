import os
import zipfile
import json

# Directory path (current directory)
cwd = os.getcwd()

# Consolidated manifest
def consolidate_manifest():
    manifest = {}

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
                            del config_data["customCSS"]

                            # Extract the id and use the entire config.json as value
                            if 'id' in config_data:
                                manifest[config_data['id']] = config_data
                            else:
                                print(f"Warning: 'id' missing in {file}'s config.json")
            except zipfile.BadZipFile:
                print(f"Error: {file} is not a valid zip file.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Write the consolidated manifest to manifest.json
    manifest_path = os.path.join(cwd, 'manifest.json')
    with open(manifest_path, 'w') as manifest_file:
        json.dump(manifest, manifest_file, indent=4)

    print(f"Manifest successfully written to {manifest_path}")

if __name__ == "__main__":
    consolidate_manifest()
