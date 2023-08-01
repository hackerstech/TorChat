#!/bin/bash



if [ -z "$1" ]
then
echo -e "\033[1;32m Tor_Chat is encrypted chat over Tor service \n for more visit :\033[0m https://github.com/hackerstech"
echo -e "\033[1;33musage: 	sudo tor_chat -s : For server side \n	sudo tor_chat -c : For client side \033[0m \n 	tor_chat -u: uninstall"
exit
fi




if [ "$EUID" -ne 0 ]
then
echo "run with sudo"
exit
elif [ "$1" == "-s" ]

then

sudo cat torrc > /etc/tor/torrc
trap 'cat Normal_Torrc >/etc/tor/torrc' 1 2/3 9
service tor start 2>/dev/null
echo "link to join-:"
cat /var/lib/tor/hidden_service/hostname
echo -e "server should be host on same port 8080 and join port = 80\n"
torsocks python3 chat_server.py

elif [ "$1" == "-c" ]
then 

service tor start 2>/dev/null
torsocks python3 chat_client.py

elif [ "$1" == "-u" ] || [ "$1" == "--uninstall" ]
then
cat Normal_Torrc >/etc/tor/torrc




echo "uninstalled"
cd ..
rm -rf TorChat

elif [ "$1" == "-r" ]

then 

echo "reversed"

cat Normal_Torrc >/etc/tor/torrc



else
echo "\033[1;31mERROR"
exit

fi
