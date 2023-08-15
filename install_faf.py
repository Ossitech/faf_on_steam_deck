import os
import json

HOME_PATH = os.path.join("/home", os.environ["USER"])

RUN_FILE_PATH = os.path.join(HOME_PATH, ".faforever/run")
CLIENT_PREFS_PATH = os.path.join(HOME_PATH, ".faforever/client.prefs")

LAUNCH_PARAMETERS = "PROTON_NO_ESYNC=1 PROTON_NO_FSYNC=1 PROTON_DUMP_DEBUG_COMMANDS=1 %command%"

def run(command, ignore_failure = False):
    if os.system(command):
        if not ignore_failure:
            print("An error occurred during this command: " + command)
            exit()

def update_pacman_conf():
    print("Updating /etc/pacman.conf...")

    with open("/etc/pacman.conf", "r") as f:
        text = f.read()
    
    with open("pacman.conf", "w") as f:
        f.write(text)
    
    run("cp pacman.conf pacman.conf.backup")
    
    text = text.replace("[jupiter]", "[jupiter-rel]")
    text = text.replace("[holo]", "[holo-rel]")
    text = text.replace("[core]", "[core-rel]")
    text = text.replace("[extra]", "[extra-rel]")
    text = text.replace("[community]", "[community-rel]")
    text = text.replace("[multilib]", "[multilib-rel]")

    with open("pacman.conf", "w") as f:
        f.write(text)
    
    run("sudo mv pacman.conf /etc/pacman.conf")

    print("Finished!")


def init_pacman_keyring():
    print("Initializing pacman keyring...")

    run("sudo pacman-key --init")
    run("sudo pacman-key -u")
    run("sudo pacman-key --populate")
    run("sudo pacman-key --populate archlinux")
    run("sudo pacman-key --populate holo")

    print("Finished!")


def install_aur_package(name):
    print(f'Installing AUR-Package "{name}"...')
    run(f'git clone "https://aur.archlinux.org/{name}.git"')

    # Save current directory.
    cwd = os.getcwd()

    # Move into cloned repository.
    os.chdir(name)
    run("makepkg -si --noconfirm")

    # Move back to the current working directory.
    os.chdir(cwd)

    # Clean up
    run(f'rm -rf "{name}"')

    print("Finished!")



def install_dgVoodoo():
    print("Installing dgVoodoo...")

    cwd = os.getcwd()
    run("mkdir voodooStuff", True)
    os.chdir("voodooStuff")

    run("curl -L -O http://dege.freeweb.hu/dgVoodoo2/bin/dgVoodoo2_79_1.zip")
    run("unzip dgVoodoo2_79_1.zip")
    run("cp MS/x64/D3D9.dll /home/$USER/.faforever/bin/")
    run("cp dgVoodoo.conf /home/$USER/.faforever/bin/")

    os.chdir(cwd)

    # Remove watermark.
    with open(".faforever/bin/dgVoodoo.conf", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("dgVoodooWatermark"):
            lines[i] = line.replace("true", "false")
            break
    
    text = "".join(lines)

    with open(".faforever/bin/dgVoodoo.conf", "w") as f:
        f.write(text)

    # Clean up
    run("rm -rf voodooStuff")

    print("Finished!")


def copy_faf_run_script():
    print("Copy steam run script to faf...")

    found = False
    while not found:
        # Find run dump path in /tmp
        for file_name in os.listdir("/tmp"):
            if "proton_" in file_name:
                full_path = os.path.join("/tmp", file_name, "run")

                if not os.path.exists(full_path):
                    break

                run(f'sudo cp "{full_path}" "{RUN_FILE_PATH}"')
                found = True
        
        if not found:
            input(f"The run file could not be found! Please make sure to launch SupCom FA at least once with the following launch parameters:\n{LAUNCH_PARAMETERS}\nPress Enter if you want to try again.")

    print("Finished!")


def set_faf_run_script():
    print("Setting run script in faf...")

    with open(CLIENT_PREFS_PATH) as f:
        text = f.read()

    json_object = json.loads(text)
    json_object["forgedAlliance"]["executableDecorator"] = RUN_FILE_PATH + ' "%s"'

    text = json.dumps(json_object, indent=4)

    with open(CLIENT_PREFS_PATH, "w") as f:
        f.write(text)

    print("Finished!")


def main():
    os.chdir(HOME_PATH)

    # make steamos writable
    run("sudo steamos-readonly disable")

    update_pacman_conf()

    init_pacman_keyring()

    # install packages for AUR
    run("sudo pacman -S --needed --noconfirm base-devel git")
    run("sudo pacman -S --noconfirm holo-rel/linux-headers linux-neptune-headers holo-rel/linux-lts-headers glibc gcc gcc-libs fakeroot linux-api-headers libarchive")

    install_aur_package("yay")
    run("yay -S --noconfirm downlords-faf-client")

    install_dgVoodoo()

    copy_faf_run_script()
    set_faf_run_script()

    print("Installation successful!")


if __name__ == "__main__":
    main()
