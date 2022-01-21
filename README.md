# label-editor-v2

## Editor
![gui](images/gui.png)

## Data Viewer
![gui2](images/gui2.png)

# tesseract scripts
## change png to tif file extension
```
for f in *.png; do mv -- "$f" "${f%.png}.tif"; done
```



# TODO
* support other annotation
* seperate annotation and prediction
  * self improved system with more data
* backend decisions
  * tensorflow serving
  * tesseract service
  * django/flask backend
    * easier to do the postprocessing
    * the backend can be scaled up seperately
