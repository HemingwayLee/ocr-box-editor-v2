# tesseract-box-editor-v2

## Editor
![gui](images/gui.png)

## Data Viewer
![gui2](images/gui2.png)

# tesseract scripts
## change png to tif file extension
```
for f in *.png; do mv -- "$f" "${f%.png}.tif"; done
```
