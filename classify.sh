#just a side effect of how we process files.
# since we can process specific type of files at a time, like images or videos etc, we can use this python code to classify the files in a folder into categories.

DIRECTORY=$1
if [ -d "$DIRECTORY" ]; then

  if [ ! -d "temp_images_folder" ]; then
    python3 encode.py -f images $DIRECTORY temp_images_folder -sw
    python3 decode.py temp_images_folder Images_c
    if [ -d "temp_images_folder" ]; then
      rm -r temp_images_folder
    fi
  else
    echo -e "A directory named temp_images_folder already exists. The program cannot work as this temp directory is created\n"
    exit -1
  fi

  if [ ! -d "temp_videos_folder" ]; then
    python3 encode.py -f videos $DIRECTORY temp_videos_folder -sw
    python3 decode.py temp_videos_folder Videos_c
    if [ -d "temp_videos_folder" ]; then
      rm -r temp_videos_folder
    fi
  else
    echo -e "A directory named temp_videos_folder already exists. The program cannot work as this temp directory is created\n"
    exit -1
  fi

  if [ ! -d "temp_docs_folder" ]; then
    python3 encode.py -f docs $DIRECTORY temp_docs_folder -sw
    python3 decode.py temp_docs_folder Documents_c
    if [ -d "temp_docs_folder" ]; then
      rm -r temp_docs_folder
    fi
  else
    echo -e "A directory named temp_docs_folder already exists. The program cannot work as this temp directory is created\n"
    exit -1
  fi

  if [ ! -d "temp_prog_folder" ]; then
    python3 encode.py -f prog $DIRECTORY temp_prog_folder -sw
    python3 decode.py temp_prog_folder Programs_c
    if [ -d "temp_prog_folder" ]; then
      rm -r temp_prog_folder
    fi
  else
    echo -e "A directory named temp_prog_folder already exists. The program cannot work as this temp directory is created\n"
    exit -1
  fi
  
else
  echo "Please specify directory"
fi