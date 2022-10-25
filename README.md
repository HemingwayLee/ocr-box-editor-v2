# ocr-box-editor-v2
## prerequisite
* install `tesseract`
* install `python3` and `virtualenv`

## How to install
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt 
```

## How to run
```
python3 manage.py migrate
python3 manage.py runserver
```

And then, we can access `http://127.0.0.1:8000`

## Editor
![gui](images/gui.png)

## Data Viewer
![gui2](images/gui2.png)

# tesseract scripts
## change png to tif file extension
```
for f in *.png; do mv -- "$f" "${f%.png}.tif"; done
```

