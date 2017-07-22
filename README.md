# KivyRecordPlayer #

* clean UI
* each folder in the music directory is a "record" to be played by touch
* no playlists 
* no bleedin' shuffle mode

The actual playback is handled by a configurable backend, by default the excellent [Music Player Daemon](https://www.musicpd.org/).

Built using [Kivy](https://kivy.org).

Browsing - touch a record to select, then touch again to play...

![browsing](https://bytebucket.org/robagar/kivyrecordplayer/raw/164f3ec95368ce9f25a44022c644bb4b20c791fb/screenshots/browsing.png)

Playing...

![playing](https://bytebucket.org/robagar/kivyrecordplayer/raw/be94eb54d1e853946151b1932adade498eb8ce78/screenshots/playing.png)

## System Setup ##

This is my working setup for playing music.  See the *system_config* directory for full details of installed packages and configuration.

* [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [Arch Linux ARM](https://archlinuxarm.org/)
* Official Raspberry Pi [7" Touch Display](https://www.raspberrypi.org/products/raspberry-pi-touch-display/)
* Bang & Olufsen [BeoPlay S3](https://www.beoplay.com/products/beoplays3) bluetooth speaker (worth the money!)
* [Kivy](https://kivy.org) 1.9.1
* [MPD](https://www.musicpd.org/) 
* KivyRecordPlayer launched by [nodm](https://github.com/spanezz/nodm) as the sole GUI process on boot