#!/bin/bash
MY_ENVS=("$@")
for MY_ENV_SET in "${MY_ENVS[@]}";do
    CMD+="export $MY_ENV_SET "
done

CMD+="env"
exec "$CMD"
# docker compose -p rosyain_blog up