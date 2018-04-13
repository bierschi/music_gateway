#!/usr/bin/env bash

echo -e "\nconfiguration for the music gateway starts: \n"

read -p "please enter the host address for the broker: " host
read -p "please enter the port: " port
read -p "please enter the username: " username
read -p "please enter the password: " password
read -p "please enter the topic: " topic

mkdir configs #TODO check if configs is already existing

cat <<EOF > configs/configuration.json
{
    "TOPIC_NAME": {
        "topic": "$topic"
    },
    "MQTT": {
        "host": "$host",
        "port": "$port",
        "username": "$username",
        "password": "$password"
    }
}
EOF




