#~/bin/bash

USER=rob

set -x

pacman -Qe > arch_packages.txt
pip freeze > python_packages.txt
cp /etc/mpd.conf ./etc
cp /etc/nodm.conf ./etc
cp /etc/locale.conf ./etc
rsync -a /etc/systemd/ ./etc/systemd
rsync -a /etc/X11/ ./etc/X11
rsync -a /etc/bluetooth/ ./etc/bluetooth
rsync -a /etc/pulse/ ./etc/pulse

mkdir -p ./home/$USER/.kivy
cp /home/$USER/.kivy/config.ini ./home/$USER/.kivy
cp /home/$USER/.xinitrc ./home/$USER/.xinitirc

