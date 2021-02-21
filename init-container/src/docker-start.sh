cd /$DATA_FOLDER;kaggle datasets download -d rounakbanik/the-movies-dataset -p /data
cd /$DATA_FOLDER;unzip the-movies-dataset.zip
cd /$DATA_FOLDER;wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
cd /$DATA_FOLDER;gzip -d enwiki-latest-abstract.xml.gz
echo "Done"