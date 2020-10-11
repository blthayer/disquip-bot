docker run --rm^
 --mount type=bind,source=%CD%/disquip.ini,target=/disquip-bot/disquip.ini^
 --mount type=bind,source=%CD%/audio_files,target=/disquip-bot/audio_files^
 blthayer/disquip-bot:latest