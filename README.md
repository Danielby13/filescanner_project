#File Scanner program - automatic crop and convert image color 
The following options allowed in the program: 
```
1) crop and convert to black & white 
2) crop and convert to grayscale color 
3) crop and keep the original colors
after choosing the convert type - click on button "save" to save new image by the name: "output.jpg".
```

The scanner will assume that:
```
1) The document to be scanned is the main focus of the image.
2) The document is rectangular, meaning it can be represented by four points.
```

The program was written in python 3.8 on windows 10.
Required libraries: ```opencv-python, numpy, scipy, matplotlib, pillow, imutils, tkinter```

Files required on the same folder:
```
"Scanner.py", "background_image1.png", "background_image2.png"
Output image will be saved to the same folder "scanner.py" is located.
```

To run "Scanner.py" script:
```
terminal:   .../[folder path]/python Scanner.py
```

##Authors
Daniel Ben Yair - 204469118
Inbal Altan - 201643459
