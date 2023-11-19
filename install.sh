#!/bin/bash
# MY_ENVS=("$@")
# for MY_ENV_SET in "${MY_ENVS[@]}";do
#     ENV_CMD+="export $MY_ENV_SET "
# done

SLOGAN=$(
cat << "EOF"
_____________________________________________________________________
|       ___                         _        ___  __                |
|      / _ \___  ___ __ _________ _(_)__    / _ )/ /__  ___ _       |
|     / , _/ _ \(_-</ // / __/ _ `/ / _ \  / _  / / _ \/ _ `/       |
|    /_/|_|\___/___/\_, /_/  \_,_/_/_//_/ /____/_/\___/\_, /        |
|                  /___/                              /___/         |
_____________________________________________________________________
EOF
)
GIT_INFO=$(
cat << "EOF"
       [Github] https://github.com/Rosyrain/Rosyrain-blog.git
EOF
)
echo -e "\e[34m$SLOGAN\e[0m"
echo -e "\n\e[34m$GIT_INFO\e[0m\n"
if [ ! -d "$DB_NAME" ];then
    read -p "数据库名称：" DB_NAME
    ENV_CMD+="export DB_NAME=$DB_NAME "
fi

if [ ! -d "$DB_PASSWD" ];then
    PASSWD_NOT_OK=true
    while $PASSWD_NOT_OK
    do
        read -s -p "数据库密码：" TEMP_PASSWD
        echo
        read -s -p "请重复输入密码：" TEMP_PASSWD_VERIFY
        echo
        if [ "$TEMP_PASSWD" = "$TEMP_PASSWD_VERIFY" ];then
            PASSWD_NOT_OK=false
            ENV_CMD+="export DB_PASSWD=$TEMP_PASSWD "
        else
            echo -e "\e[31m两次密码不一致，请重新输入！\e[0m"
        fi
    done
    
fi
exec bash -c "$ENV_CMD && docker compose -p rosyain_blog up"