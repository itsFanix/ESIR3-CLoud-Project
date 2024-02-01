
## Error encounter while doing the project


### 'PIL.Image' has no attribute 'ANTIALIAS'
to solve this bug, install openCV.
Moviepy  use openCV as resizer first and if openCV is not install, it will use  PIL wich leads  to the error
pip install opencv-python