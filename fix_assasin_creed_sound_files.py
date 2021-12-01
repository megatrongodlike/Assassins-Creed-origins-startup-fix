import ctypes
import glob
import os
import shutil
import sys

# make sure you are *only* running this script in assasin's creed installation folder!!
# 在运行之前，确保这个文件在刺客信条的安装目录！！ 否则可能会破坏其他重要文件

dest_path = 'C:\\ac_sound_files\\'

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def find_all_pck(path):
    return map(lambda x: x.replace('\\\\', '\\'), (glob.iglob(path + '/**/*.pck', recursive=True)))


def move_and_link_all_folders_contain_soundfile(base_path: str, dest_path: str):
    kdll = ctypes.windll.LoadLibrary("kernel32.dll")

    sound_files = find_all_pck(base_path)
    for f in sound_files:
        if os.path.islink(f):
            print(f, 'is already moved')
            continue
        new_path = os.path.join(dest_path, os.path.relpath(f, base_path))
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        print("moving '{}' ---> '{}'".format(f, new_path))
        shutil.move(f, new_path)
        kdll.CreateSymbolicLinkW(f, new_path, 0)


if __name__ == '__main__':
    if is_admin():
        dest_path = os.path.join(dest_path, os.path.relpath(os.getcwd(), os.path.join(os.getcwd(), "..")))
        print("sound files will be in: '{}'".format(dest_path))
        print("在运行之前，确保这个文件在刺客信条的安装目录！！ 否则可能会破坏其他重要文件")
        print("按确认键继续，关闭窗口退出")

        print("make sure you are *only* running this script in assasin's creed installation folder!!")
        input("press enter to start, or close the program to stop")
        move_and_link_all_folders_contain_soundfile(os.getcwd(), dest_path)
        input("press enter to exit...")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.basename(__file__), None, 1)
