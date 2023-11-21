from io import TextIOWrapper
import os
import json

from jams.jam import Jam


def select_jam(args):
    jams = get_available_jams(args.jamspath)
    if len(jams) == 0:
        print(
            "No jams available! Please add some to the jam_library folder with an appropriate manifest file for loading."
        )
        return None

    jam_index = select_jam_index(jams)
    manifest = jams[jam_index]

    return Jam(manifest["name"], manifest["audio_files"])


def select_jam_index(jams):
    while True:
        print("\nAvailable jams (or just press ENTER to quit):")
        for i, jam in enumerate(jams):
            print(f"  {i+1}. {jam['name']}")

        inputValue = input("Select your jam: ")

        if inputValue == "":
            print("Quitting...")
            return None

        if not inputValue.isdigit():
            print("Invalid input - please enter a number.")
            continue

        jam_index = int(inputValue) - 1
        if jam_index < 0 or jam_index >= len(jams):
            print("Invalid input - please make a valid selection.")
            continue

        return jam_index


def get_available_jams(jam_library_path):
    jam_manifests = []
    for root, _, files in os.walk(jam_library_path):
        for file in files:
            if file == "manifest.json":
                manifest_path = os.path.join(root, file)
                with open(manifest_path, "r") as f:
                    manifest = prepare_manifest(root, f)
                    if len(manifest["audio_files"]) > 1:
                        jam_manifests.append(manifest)
                    else:
                        print(f"Skipping {manifest['name']} - not enough levels.")
    return sorted(jam_manifests, key=lambda x: x["name"])


def prepare_manifest(root: str, f: TextIOWrapper):
    manifest = json.load(f)
    manifest["path"] = root
    manifest["audio_files"] = [
        f"{manifest['path']}/{level['file']}"
        for level in manifest["levels"]
        if level["file"].strip()
    ]
    return manifest
