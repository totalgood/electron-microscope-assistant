# Electron Microscope Assistant

Ben Weintraub, Ph.D.

<a href="https://www.linkedin.com/in/benweintraub-phd/">LinkedIn profile</a>


## Table of Contents

- <a href="https://github.com/b-weintraub/electron-microscope-assistant#background">Background</a>  
- <a href="https://github.com/b-weintraub/electron-microscope-assistant#Dataset">Dataset</a> 
- <a href="https://github.com/b-weintraub/electron-microscope-assistant#Exploratory-Data-Analysis">Exploratory Data Analysis</a>  
- <a href="https://github.com/b-weintraub/electron-microscope-assistant#Models">Models</a> 
- <a href="https://github.com/b-weintraub/electron-microscope-assistant#DiscussionNext-steps">Discussion/Next steps</a>

## Summary

## Background

Electron microscopes (EMs) such as transmission electron microscopes (TEMs) and scanning electron microscopes (SEMs) are useful for probing matter at magnifications beyond what’s possible using light microscopes, whose resolution is limited by the abbe diffraction limit. EMs can achieve sub-nanometer resolutions and are useful for characterizing nano-materials, or materials with dimensions on the order of billionths of a meter.  However, EMs are complex instruments requiring ultra-high vacuum systems and are thus expensive to operate.  It would be useful to develop methods to reduce the length of time required to analyze samples and increase sample analysis throughput.  Electron microscopists spend much of their time searching for target samples on the substrate as this process can be likened to “finding a needle in a haystack”.

This project looks for ways to automate parts of the electron microscopy process by using neural networks to identify nano-materials from scanning electron microscope images.


## Dataset

The dataset contains 21,283 scanning electron microscope (SEM) images produced at Institute of Materials, CNR (https://b2share.eudat.eu/records/80df8606fcdb4b2bae1656f0dc6db8ba).  The images were broken up into 10 categories as shown in the below table.

## Exploratory Data Analysis

| category     | Number of images |
| ------------- |:-------------:| 
| Biological | 973    |
| Fibres | 163    |   
| Films_Coated_Surface      |327     |
| MEMS_devices_and_electrodes  | 4591     |
| Nanowires  | 3821     |
| Particles  | 3926     |
| Patterned_surface  | 4756     |
| Porous_Sponge  | 182     |
| Powder  | 918     |
| Tips  | 1625     |


Here are some representative images of each of the 10 categories.

<img src='img/example_categories_plot.png' align='center' style='width: 800px;'>

Although the images are grayscale, they are encoded in 3 RGB channels. Each image contains a color metadata tag including magnification, stage tilt angle, working distance, etc.  The tag was not removed. 

# Data preprocessing

The data was split into 70% training, 20% validation and 10% holdout and uploaded to an AWS S3 bucket for later processing on an EC2 instance.

Training image data were augmented by transformations including rotation, width/height shift, shearing and zoom.



## Models

A convolution neural network (CNN) was the best choice for this dataset because they are uniquely suited to finding features in images. Generally, images are represented as tensors, or multi-dimensional arrays. Convolution, Rectified Linear Unit, and Max Pooling are three types of transformations commonly chained together in CNNs. Convolution is an operation that identifies which regions of an image have a feature by combining an image and a filter to create a new image.  The rectified linear unit (ReLU),an activation function, highlights only the region where the feature exists. Lastly, max pooling downsamples the resulting information to lower resolution to save space and computation. 



## Training
To handle the heavy processing, all computing was performed on an AWS EC2 instance (32 vCPU, 128 GiB memory). The model was training for 20 epochs.  Tensorboard was used to monitor the progress of the models. The model was trained by minimizing a cross entropy loss function. Accuracy and loss was tabulated for each epoch and saved to a log file using tensorboard.  

Here is sample code for the simple CNN.

<details open="">
    
    nb_filters = 32
    kernel_size = (3, 3)
    pool_size = (2, 2)
    model = Sequential()
    # 2 convolutional layers followed by a pooling layer followed by dropout
    model.add(Convolution2D(nb_filters, kernel_size,
                            padding='valid',
                            input_shape=input_size))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, kernel_size))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))
    # transition to an mlp
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(n_categories))
    model.add(Activation('softmax'))

</details>

<details open="">
    <summary>Xception transfer Model Summary</summary>
    
</details>


## Discussion/Next steps

<table>
    <tbody><tr><th><img src='img/accuracy_xc_model-20.png' align='center' style='width: 200px;'></th>
    <th><img src='img/accuracy_simple_cnn_model-20.png' align='center' style='width: 200px;'></td></th>
    </tr><tr>
        <td><img src='img/loss_xc_model-20.png' align='center' style='width: 200px;'></td>
        <td><img src='img/loss_simple_cnn_model-20.png' align='center' style='width: 200px;'></td>
    </tr>
</tbody></table>


<img src='img/confusion_xc_model.png' align='center' style='width: 800px;'>

Commonly confused categories

| category     | confused for | % |
| ------------- |:-------------:|:-------: |
| Patterned_surface | MEMS_devices_and_electrodes    | 2.26%|
| Particles | Nanowires    |  0.55% |
|   Particles    |Films_Coated_Surface     | 0.43%|
|  Nanowires | Biological    | 0.37%|
|  Nanowires | Films_Coated_Surface     |0.30%|


## Flask web app

<p align='middle'>
<td><img src='img/web-app-screen-shot.png'  width="400" height=""></td>
</p>

App demonstration

<p align='middle'>
<img src="https://github.com/b-weintraub/electron-microscope-assistant/blob/master/img/flask-demo3.gif" width="" height="" />
</p>
  
Tech stack used:

<p align='middle'>
<td><img src='img/tech-stack.png'  width="" height=""></td>
</p>



## References

Aversa, R., Modarres, M., Cozzini, S. et al. The first annotated set of scanning electron microscopy images for nanoscience. Sci Data 5, 180172 (2018). 
https://www.nature.com/articles/sdata2018172

F. Chollet, "Xception: Deep Learning with Depthwise Separable Convolutions," 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), Honolulu, HI, 2017, pp. 1800-1807, doi: 10.1109/CVPR.2017.195.
https://arxiv.org/pdf/1610.02357.pdf


