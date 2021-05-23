declare -A osInfo;
osInfo[/etc/redhat-release]=yum
osInfo[/etc/arch-release]=pacman
osInfo[/etc/gentoo-release]=emerge
osInfo[/etc/SuSE-release]=zypp
osInfo[/etc/debian_version]=apt-get

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        if [${osInfo[$f]} == 'apt-get'];then
        	sudo apt-get install cron anacron
        	service cron start
        fi
        if [${osInfo[$f]} == 'yum'];then
        	yum install cronie cronie-anacron
        	systemctl enable cronie.service
        	systemctl start cronie.service
        fi
        if [${osInfo[$f]} == 'pacman'];then
        	pacman -S cronie
        	systemctl enable --now cronie.service
        	systemctl start cronie.service
        fi
        ${osInfo[$f]} install anacron
    fi
done