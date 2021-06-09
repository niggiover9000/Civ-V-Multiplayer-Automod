import os
from os.path import expanduser, isdir
from distutils.dir_util import copy_tree
from shutil import copyfile
from time import sleep

mods_path = os.path.join(expanduser("~"), "Documents\My Games\Sid Meier's Civilization 5\MODS")


def gen_xml():
    """
    Creates the XML File used for the multiplayer mods
    :return: XML formatted string containing the downloaded mods
    """
    ret_xml = "\n\t<!-- MULTIPLAYER MOD FILES -->\n\n"

    for _, _, files in os.walk(mods_path):
        for file in files:
            if file.endswith(".xml"):
                ret_xml += "\t<GameData>" + file + "</GameData>\n"
                ret_xml += "\t<TextData>" + file + "</TextData>\n\n"

    ret_xml += "\t<!-- END MULTIPLAYER MOD FILES -->\n\n"
    return ret_xml


def remove_mods(data):
    """
    :return:
    """
    mod_begin = 0
    mod_end = 0

    for i in range(len(data)):
        if "\t<!-- MULTIPLAYER MOD FILES -->\n" in data[i]:
            mod_begin = i
        elif "\t<!-- END MULTIPLAYER MOD FILES -->\n" in data[i]:
            mod_end = i
            break

    del (data[mod_begin - 1:mod_end + 2])


def get_game_path():
    steam_path = "\steam\steamapps\common\Sid Meier's Civilization V\Assets\DLC\Expansion2"
    if isdir(f"C:\Program Files (x86){steam_path}"):
        return f"C:\Program Files (x86){steam_path}"
    else:
        for i in range(65, 91):
            if isdir(f"{chr(i)}:\{steam_path}"):
                return f"{chr(i)}:\{steam_path}"
        return False


def get_mod_folder():
    if isdir(mods_path):
        print("Mods folder found.\n")
    else:
        print(f"Mods folder not present at: {mods_path}. Did you download the mods from the Steam Workshop?")
        print("Program will terminate now.")
        sleep(5)
        exit(-1)


def list_mods():
    mods = os.listdir(mods_path)
    print("Installing Mods:")
    print('\n Installing '.join(mods))
    return mods


def copy_mods(mods):
    for mod in mods:
        src = os.path.join(mods_path, mod)
        target = os.path.join(steam_path, "[MOD] " + mod)
        copy_tree(src, target)


def backup_pkg_file():
    print("\n Backing up Expansion2.Civ5Pkg File...")
    pkg = os.path.join(steam_path, "Expansion2.Civ5Pkg")
    copyfile(pkg, pkg + ".old")
    del pkg


def write_pkg_file():
    with open(os.path.join(steam_path, "Expansion2.Civ5Pkg")) as f:
        data = f.readlines()

        remove_mods(data)

        for i in range(len(data)):
            if "<Gameplay>\n" in data[i]:
                xml = gen_xml()
                data.insert(i + 1, xml)
                break
    with open(os.path.join(steam_path, "Expansion2.Civ5Pkg"), "w") as f:
        f.writelines(data)
        f.flush()

if __name__ == '__main__':
    # check for mods folder
    get_mod_folder()

    # get steam install drive
    game_path = get_game_path()
    if game_path is not False:
        steam_path = game_path
        print(f"Civ_Folder automatically detected: {steam_path}")
    else:
        print("Civilization V folder couldn't be detected automatically.")
        while True:
            steam_drive = input("Please enter your install path. i.e. C:/Program Files (x86)/Steam, E:/Steam ...: ")
            steam_path = os.path.join(steam_drive, "steamapps\common\Sid Meier's Civilization V\Assets\DLC\Expansion2")
            # check for civ install folder
            if steam_drive == "/exit":
                print("Program will terminate now.")
                sleep(5)
                exit(-1)
            if isdir(steam_path):
                print("The Civilization V folder was found.\n")
                break
            else:
                print(f"The Civilization V folder was not fould at {steam_path}. Please retry or exit with '/exit'")

    # list subscribed mods
    mods = list_mods()

    # copy mods
    copy_mods(mods)

    # saving pkg file
    backup_pkg_file()

    # writing to pkg file
    write_pkg_file()

    print("Install successful")
    sleep(5)
