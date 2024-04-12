import os
import sys
import shutil
import zipfile


jit_off_for_files = ["engine/http_manager.lua", "engine/profile.lua", "engine/save_manager.lua", "engine/sound_manager.lua", "main.lua"]


def copy_balatro_executable():
    if sys.platform == "win32":
        shutil.copy("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Balatro\\Balatro.exe", "balatro")
    elif sys.platform == "darwin":
        shutil.copy("/Users/" + os.getlogin() + "/Library/Application Support/Steam/steamapps/common/Balatro/Balatro.app/Contents/Resources/Balatro.love", "balatro")
    elif sys.platform == "linux":
        shutil.copy("/home/" + os.getlogin() + "/.steam/steam/steamapps/common/Balatro/Balatro.love", "balatro")


def extract_balatro_files():
    os.mkdir(os.path.join(os.getcwd(), "balatro_files"))
    with zipfile.ZipFile("balatro", 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd(), "balatro_files"))


def alter_code_for_ios():
    # append jit.off() to the beginning of each file
    for file in jit_off_for_files:
        with open(os.path.join("balatro_files", file), "r") as f:
            contents = f.readlines()
            contents.insert(0, "jit.off()\n")
        with open(os.path.join("balatro_files", file), "w") as f:
            f.writelines(contents)

    # comment out `loadstring(` in globals.lua
    with open(os.path.join("balatro_files", "globals.lua"), "r") as f:
        contents = f.readlines()
        for i, line in enumerate(contents):
            if "loadstring(" in line:
                contents[i] = "-- " + line
    with open(os.path.join("balatro_files", "globals.lua"), "w") as f:
        f.writelines(contents)

    # change FPS_CAP to 120 in main.lua
    with open(os.path.join("balatro_files", "main.lua"), "r") as f:
        contents = f.readlines()
        for i, line in enumerate(contents):
            if "G.FPS_CAP = G.FPS_CAP or 500" in line:
                contents[i] = line.replace("500", "120")
    with open(os.path.join("balatro_files", "main.lua"), "w") as f:
        f.writelines(contents)



def recompress_balatro_files():
    shutil.make_archive("balatro", "zip", "balatro_files")
    os.rename("balatro.zip", "balatro.love")
    shutil.rmtree("balatro_files")
    os.remove("balatro")


if __name__ == "__main__":
    copy_balatro_executable()
    extract_balatro_files()
    alter_code_for_ios()
    recompress_balatro_files()
