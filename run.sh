mkdir raw text clean fixed
python scrape.py 
python extract.py 
python cleanup.py $1
python fix.py 
python gather.py
