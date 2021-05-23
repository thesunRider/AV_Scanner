#!/bin/bash

declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypp
osInfo[/etc/debian_version]=apt-get

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
    	echo "Package mngr: ${osInfo[$f]}"

        if [ $(which ${osInfo[$f]}|grep "apt-get") ];then
        	sudo apt-get install cron anacron
        	sudo service cron start
        fi
        if [  $(which ${osInfo[$f]}|grep "yum") ];then
        	sudo yum install cronie cronie-anacron
        	systemctl enable cronie.service
        	systemctl start cronie.service
        fi
        if [  $(which ${osInfo[$f]}|grep "pacman") ];then
        	sudo pacman -S cronie
        	systemctl enable --now cronie.service
        	systemctl start cronie.service
        fi
        sudo ${osInfo[$f]} install anacron
    fi
done

if [[ $(which gnome-shell) ]]; then
	sudo echo -ne '[Desktop Entry]
Name=JVSOFT Malware Detector
Exec='$PWD'/av_scanner
StartupNotify=true
Terminal=false
Type=Application
Icon='$PWD'/icon.ico'>/usr/share/applications/jvsoft.desktop
fi


sudo chmod +x av_scanner
sudo echo -ne '#!/bin/sh \n.'$PWD'/av_scanner -a' >/etc/cron.daily/launchjvsoft
sudo chmod +x /etc/cron.daily/launchjvsoft