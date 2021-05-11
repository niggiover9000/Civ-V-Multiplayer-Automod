import os
from os.path import expanduser, isdir
from distutils.dir_util import copy_tree
from shutil import copyfile

mods_path = os.path.join(expanduser("~"), "Documents\My Games\Sid Meier's Civilization 5\MODS")


def gen_xml():
    ret_xml = "\n\t<!-- MULTIPLAYER MOD FILES -->\n\n"

    for _, _, files in os.walk(mods_path):
        for file in files:
            if file.endswith(".xml"):
                ret_xml += "\t<GameData>" + file + "</GameData>\n"
                ret_xml += "\t<TextData>" + file + "</TextData>\n\n"

    ret_xml += "\t<!-- END MULTIPLAYER MOD FILES -->\n\n"
    return ret_xml


def remove_mods():
    mod_begin = 0
    mod_end = 0

    for i in range(len(data)):
        if "\t<!-- MULTIPLAYER MOD FILES -->\n" in data[i]:
            mod_begin = i
        elif "\t<!-- END MULTIPLAYER MOD FILES -->\n" in data[i]:
            mod_end = i
            break

    del (data[mod_begin - 1:mod_end + 2])


if __name__ == '__main__':

    # check for mods folder
    if isdir(mods_path):
        print("mods folder found.\n")
    else:
        print("mods folder not present at: " + mods_path)
        exit(-1)

    # get steam install drive
    # steam_drive = input("steam install path? i.e. C:/Program Files (x86)/Steam, E:/Steam ...\n\n")
    steam_drive = "d:/faststeam"
    steam_path = os.path.join(steam_drive, "steamapps\common\Sid Meier's Civilization V\Assets\DLC\Expansion2")

    # check for civ install folder
    if isdir(steam_path):
        print("civ folder found.\n")
    else:
        print("civ folder not present at: " + steam_path)
        exit(-1)

    # list subscribed mods
    mods = os.listdir(mods_path)
    print("installing mods:")
    print('\n'.join(mods))

    # copy mods
    for mod in mods:
        src = os.path.join(mods_path, mod)
        target = os.path.join(steam_path, "[MOD] " + mod)
        copy_tree(src, target)

    # saving pkg file
    print()
    print("backing up pkg file")
    pkg = os.path.join(steam_path, "Expansion2.Civ5Pkg")
    copyfile(pkg, pkg + ".old")
    del pkg

    data = str()

    # writing to pkg file
    with open(os.path.join(steam_path, "Expansion2.Civ5Pkg")) as f:
        data = f.readlines()

        remove_mods()

        for i in range(len(data)):
            if "<Gameplay>\n" in data[i]:
                xml = gen_xml()
                data.insert(i + 1, xml)
                break

    with open(os.path.join(steam_path, "Expansion2.Civ5Pkg"), "w") as f:
        f.writelines(data)
        f.flush()

    print("install successful")
