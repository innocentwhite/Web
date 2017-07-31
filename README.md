# My First Website: Used for displaying prediction result produced by a CNN model in Caffe
### Written with django:version 1.10.5       [restframework](http://www.django-rest-framework.org/):version 3
#### To get your django-version:
##### (in python shell)
``` python
>>> import jango
>>> print django.VERSION
```
### index
![Index Page](https://github.com/innocentwhite/website-for-prediction-result/blob/master/website_view/index.png)
## How to run this website?
download all the packages included in this project,here are some packages i remember:
 + **django**
 + **restframework**
 + **numpy**
 + **cv2**
 + **skimage**
 + **PIL**


 in your cmd typing(__NOT__ your python shell):  
 ``` sh
 >>> git clone https://github.com/innocentwhite/website-for-prediction-result/ (you need to install git first)  
 >>> cd website-for-prediction-result   
 >>> python manage.py runserver    
 ```
 
 If you have installed all the packages needed, It will display as follows:
 ```
 Performing system checks...

 System check identified no issues (0 silenced).   
 July ××, 2017 - ××:××:××    
 Django version 1. 10. 5, using settings '''displayWeb.settings'''   
 Start development server at http://127.0.0.1:8000/    
 Quit the server with CTRL-BREAK   
```
 If you got the same message: congratulations,you have succeeded in setting up your website!
 You can visit your website in your browser at http://127.0.0.1:8000/ now.

 If you failed: Sorry, I don't know what's the problems with your code.You can google with your error messages.    
 But if you don't mind, you can also contact me at liucl14@mails.tsinghua.edu.cn
## How to display prediction result?
__Only Caffe__ is supported!
besides,the path must be:
``` sh
Home\website-for-prediction-result\display
Home\files\caffe\
```
The connection part(connects to CNN model) is defined in :  
```
website-for-prediction-result\display\upload\caffemodel.py
```
in your project, you should modify lines 35-47 as follows:
```python
caffe_root = '/workov/home1/liucl/files/caffe/'
sys.path.insert(0, caffe_root + 'python')

import caffe

MODEL_FILE = '../../files/caffe/examples/diabetic/model/deploy.prototxt'

PRETRAINED = '../../files/caffe/examples/diabetic/model/VGG19ft_iter_3500.caffemodel'

IMAGE_FILE = '../../files/caffe/examples/images'

IMAGE_NAME = 'preprocessed.jpeg'
```
__caffe_root__ defines as named   
__MODEL_FILE__ requires your model layer definition, so modify it with your \*\*\*.prototxt   
__PRETRAINED__ is your model parameters saved as \*\*\*.caffemodel, please modify it with your \*\*\*.caffemodel   
__IMAGE_FILE__ is the dir that saves your images to be predicted  
__IMAGE_NAME__ defines as named

__IMAGE_FILE__ and __IMAGE_NAME__ is connected in:
```
website-for-prediction-result\display\upload\views.py
```
lines 29-33:
```python
os.system("cp "+os.path.join("storage", new_img.Image.name)+" ../../files/caffe/examples/images/again.jpeg")
preprocessing(IMAGE_FILE, "again.jpeg")
if not os.path.exists("upload/static/img"):
    os.system("mkdir upload/static/img/")
os.system("cp "+"../../files/caffe/examples/images/preprocessed.jpeg "+"upload/static/img/")
```
I think you can understand that

After this, you can predict with your model.   
Click the \"select file\" button and then \"Submit\" button.    
I hope this website can hlep.
## Unfinished Part
In profile page, \"save\" button directs to \"#\", url is not defined now, so this website don't support change profile now.   
But you can change your password in profile page.
  
This website still usesd django's template, restful API version will be updated soon.
## Function unit
 ### Admin Part
 ![Admin Page](https://github.com/innocentwhite/website-for-prediction-result/blob/master/website_view/admin.png)
 ### Login Part
 ![Login Page](https://github.com/innocentwhite/website-for-prediction-result/blob/master/website_view/login.png)
 ### Profile Part
 ![Profile Page](https://github.com/innocentwhite/website-for-prediction-result/blob/master/website_view/profile.png)
 ### Registe Part
 ![Registe Page](https://github.com/innocentwhite/website-for-prediction-result/blob/master/website_view/registe.png)
