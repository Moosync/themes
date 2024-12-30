import os
import zipfile
import json
import uuid

# Directory path (current directory)
cwd = os.getcwd()

def resolve_and_repack():
    ids_seen = set()

    for file in os.listdir(cwd):
        if file.endswith(".mstx"):
            temp_dir = os.path.join(cwd, "temp_extract")
            os.makedirs(temp_dir, exist_ok=True)

            try:
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                config_path = os.path.join(temp_dir, "config.json")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as config_file:
                        config_data = json.load(config_file)

                    if 'id' in config_data:
                        original_id = config_data['id']

                        if original_id in ids_seen:
                            # Generate a new UUID for the conflicting ID
                            new_id = str(uuid.uuid4())
                            print(f"Conflict detected for ID '{original_id}' in {file}. Replacing with new ID: {new_id}")
                            config_data['id'] = new_id

                            # Update config.json with new ID
                            with open(config_path, 'w') as config_file:
                                json.dump(config_data, config_file, indent=4)

                        ids_seen.add(config_data['id'])
                    else:
                        print(f"Warning: 'id' not found in config.json of {file}")

                # Repack the zip file with updated config.json
                new_zip_path = os.path.join(cwd, file)
                with zipfile.ZipFile(new_zip_path, 'w') as new_zip:
                    for root, _, files in os.walk(temp_dir):
                        for fname in files:
                            file_path = os.path.join(root, fname)
                            arcname = os.path.relpath(file_path, start=temp_dir)
                            new_zip.write(file_path, arcname)

                print(f"Repacked and updated {file} successfully.")

            except zipfile.BadZipFile:
                print(f"Error: {file} is not a valid zip file.")
            except Exception as e:
                print(f"Error processing {file}: {e}")
            finally:
                # Clean up temporary directory
                for root, _, files in os.walk(temp_dir):
                    for fname in files:
                        os.remove(os.path.join(root, fname))
                os.rmdir(temp_dir)

if __name__ == "__main__":
    resolve_and_repack()
