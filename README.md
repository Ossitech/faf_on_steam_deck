# FAF on the Steam Deck
## Introduction
This tutorial will show you how to set up Downlords FAF Client on the Steam Deck.
You will be able to play the game and use all the features of Downlords FAF Client but there are some compromises to remember.

## Automatic installation via my python script
The steps of this tutorial have to be repeated every time your Steam Deck receives an update for Steam OS! This can get very annoying soon so I encourage you to use my script that automates all these steps.
To use the script simply use these commands:
```
git clone https://github.com/Ossitech/faf_on_steam_deck
cd faf_on_steam_deck
python install_faf.py
```
Before running the script you will need to set a user password first, in case you didn't already do that.
Use the following command to set a password:
`passwd`
### Missing visual effects ingame
Some visual ingame effects are missing with the current setup.
The game is still completly playable and I am very sure that many linux players play the game without even noticing there are effects missing.

For example the projectile of the main gun of the Aeon ACU looks much more simple and has basically no visual effects except a small grey trace. This is also true for some other Aeon units like the T1 Tank and T2 Blaze.
There are many more effects missing but most of the time it only affects projectiles and you will only notice it when playing zoomed in for long periods of time.

This is a known issue on Arch Linux and normally you would fix this by not using Proton 5.0-10, which is quite old. Unfortunatly I only got the FAF Client to launch Supreme Commander with this Proton Version.
Instead using a custom proton version called ProtonGE will restore all effects but I was not able to make it work with the FAF Client on the Steam Deck. You can find more information about that here: https://github.com/GloriousEggroll/proton-ge-custom#installation
On my Arch Desktop ProtonGE and the FAF Client work just fine and noe visual effects are missing at all.

I noticed that most of the missing effects, but not all of them, can be restored by using the Proton Experimental Option in Steam. However, on the Steam Deck this, again, only seems to work with the Steam version of the game. FAF won't currently launch the game with Proton Experimental (Aug 2023) but this may be fixed in the future as Proton will be developed further.

## Manual installation
#### Steam Client
* Install Supreme Commander Forged Alliance on Steam.
* Select Proton 5.0-10 as compatibility option.
* Set these run parameters:
`PROTON_NO_ESYNC=1 PROTON_NO_FSYNC=1 PROTON_DUMP_DEBUG_COMMANDS=1 %command%`
Now start Supreme Commander Forged Alliance and close it when you get to the main menu. Maybe the game asks you to set up a local userprofile for the game before you get to the main menu.
Launching the Steam version of Supreme Commander with the provided settings has created a new file called run in this location:

```
/tmp/proton_deck/run
```

We need to copy this file to our home directory so that FAF can use it to start Supreme Commander Forged Alliance like Steam launches it.
For this we need a terminal. Switch into the desktop mode of your steam deck and open a terminal.
The terminal can be found by typing "terminal" or "console" in the start menu.
Use this command to copy the file:

```
cp /tmp/proton_deck/run /home/deck/run
```

The default username of the Steam Deck is `"deck"`. This name is NOT your steam user name but a local name for the operating system.
If you have changed your linux username before replace every `"deck"` with your username.
For instance if my name is `"name"` the command would look like this:

```
cp /tmp/proton_name/run /home/name/run
```
#### Downlords FAF Client
##### pacman

Pacman is needed for installing the FAF Client.
It's the default package manger for arch based linux distributions and is used to install software and dependencies.
For pacman to work on the Steam Deck the system write protection has to be disabled with the following commands:

To set up a root password for the deck user:

```
passwd
```

To disable the write protection:

```
sudo steamos-readonly disable
```
This will ask for the password you did just set up.

There is an issue with pacman that needs to be fixed in order to use it proberly.
Some changes to the pacman configuration have to be made.
To edit the pacman configuration file enter this command:

```
sudo nano /etc/pacman.conf
```

Navigate through the file with the arrow keys. Go down in the file until you find a section that looks like this:
```
[jupiter]
Include = /etc/pacman.d/mirrorlist
SigLevel = Never

[holo]
Include = /etc/pacman.d/mirrorlist
SigLevel = Never

[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

[community]
Include = /etc/pacman.d/mirrorlist

[multilib]
Include = /etc/pacman.d/mirrorlist
```
These headings have to be renamed so pacman can find packages. To do this simply add a "-rel" to the name.
For example, change `[holo]` to `[holo-rel]`.
Do this with: 
	`holo`
	`jupiter`
	 `core`
	 `extra`
	 `community`
	 `multilib`

To safe your changes to the file press `Ctrl + S` and to exit the editor press `Ctrl + X`.

To initialize pacman run these commands:

```
sudo pacman-key --init
sudo pacman-key -u
sudo pacman-key --populate
sudo pacman-key --populate archlinux
sudo pacman-key --populate holo
```

For the next steps we need some basic dependencies.
We install with pacman using the following command:
```
sudo pacman -S --noconfirm --needed --noconfirm base-devel git holo-rel/linux-headers linux-neptune-headers holo-rel/linux-lts-headers glibc gcc gcc-libs fakeroot linux-api-headers libarchive
```
This command may take few minutes to complete.
##### yay
yay is an so called "AUR helper". It works much like pacman and is used to install software. The difference is that you can install packages with yay, that are not found in the default repositories that pacman uses, but instead are part of the Arch User Repository (AUR).



Running the last command may require you to type in your root password.

#### Downlord's FAF Client
The FAF Client is part of the AUR (Arch User Repository) and is not an official package. That's why we need to install it differently.
Run these commands to install it:

Download:
```
git clone https://aur.archlinux.org/downlords-faf-client.git
```

Navigate into the downloaded folder:
```
cd downlords-faf-client
```

Install yay:
```
makepkg -si --noconfirm
```
You may be asked for your root password.

Now you should be able to find Downlords FAF Client under the "Games" category in the start menu or by typing FAF.
Launch the FAF Client and log in.
Now go to the top left menu and open "settings".
Navigate to the "Forged Alliance Forever" section and scroll down.
Find the entry with the title "Command Line Format for Executable" and insert the path to the "run" file we copied in the beginning.
It should look like this:

`/home/deck/run "%s"`
It is importand that the line ends with `"%s"`!
Again change the `"deck"` to your username in case you changed it.

You can now close the settings menu and play FAF!

You can use the Steam client to add FAF to your games library so you can run launch the FAF Client from the handheld mode.
