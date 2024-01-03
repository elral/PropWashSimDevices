Import("env")
import os, zipfile, shutil
from pathlib import Path

# Get the version number from the build environment.
firmware_version = os.environ.get('VERSION', "")

# Get the ZIP filename from the build environment.
zip_file_name = env.GetProjectOption('custom_zip_filename', "")

# Get the custom folder from the build environment.
community_path = env.GetProjectOption('custom_device_folder', "")


if firmware_version == "":
  firmware_version = "0.0.1"
firmware_version = firmware_version.lstrip("v")
firmware_version = firmware_version.strip(".")


def copy_fw_files (source, target, env):
    if firmware_version == "0.0.1":
        return

    fw_file_name=str(target[0])

    if os.path.exists(community_path + "/Community/firmware") == False:
        os.mkdir(community_path + "/Community/firmware")
    
    if fw_file_name[-3:] == "bin":
        fw_file_name=fw_file_name[0:-3] + "uf2"

    shutil.copy(fw_file_name, community_path + "/Community/firmware")
    createZIP()


def createZIP():
    complete_ZIP_Filename = Path('./' + zip_file_name + '_' + firmware_version + '.zip')
    path_to_archive = Path("./" + community_path + "/Community")
    with zipfile.ZipFile(complete_ZIP_Filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fp in path_to_archive.glob("**/*"):
            zipf.write(fp, arcname=fp.relative_to(path_to_archive))


env.AddPostAction("$BUILD_DIR/${PROGNAME}.hex", copy_fw_files)
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", copy_fw_files)
