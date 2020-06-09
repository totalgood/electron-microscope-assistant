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

## Training
To handle the heavy processing, all computing was performed on an AWS EC2 instance (32 vCPU, 128 GiB memory). The model was training for 20 epochs.  Tensorboard was used to monitor the progress of the models.

<details open="">
    <summary>Xception transfer Model Summary</summary>
    
    Model: "model"
__________________________________________________________________________________________________
Layer (type)                    Output Shape         Param #     Connected to                     
==================================================================================================
input_1 (InputLayer)            [(None, 170, 170, 3) 0                                            
__________________________________________________________________________________________________
block1_conv1 (Conv2D)           (None, 84, 84, 32)   864         input_1[0][0]                    
__________________________________________________________________________________________________
block1_conv1_bn (BatchNormaliza (None, 84, 84, 32)   128         block1_conv1[0][0]               
__________________________________________________________________________________________________
block1_conv1_act (Activation)   (None, 84, 84, 32)   0           block1_conv1_bn[0][0]            
__________________________________________________________________________________________________
block1_conv2 (Conv2D)           (None, 82, 82, 64)   18432       block1_conv1_act[0][0]           
__________________________________________________________________________________________________
block1_conv2_bn (BatchNormaliza (None, 82, 82, 64)   256         block1_conv2[0][0]               
__________________________________________________________________________________________________
block1_conv2_act (Activation)   (None, 82, 82, 64)   0           block1_conv2_bn[0][0]            
__________________________________________________________________________________________________
block2_sepconv1 (SeparableConv2 (None, 82, 82, 128)  8768        block1_conv2_act[0][0]           
__________________________________________________________________________________________________
block2_sepconv1_bn (BatchNormal (None, 82, 82, 128)  512         block2_sepconv1[0][0]            
__________________________________________________________________________________________________
block2_sepconv2_act (Activation (None, 82, 82, 128)  0           block2_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block2_sepconv2 (SeparableConv2 (None, 82, 82, 128)  17536       block2_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block2_sepconv2_bn (BatchNormal (None, 82, 82, 128)  512         block2_sepconv2[0][0]            
__________________________________________________________________________________________________
conv2d_2 (Conv2D)               (None, 41, 41, 128)  8192        block1_conv2_act[0][0]           
__________________________________________________________________________________________________
block2_pool (MaxPooling2D)      (None, 41, 41, 128)  0           block2_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
batch_normalization (BatchNorma (None, 41, 41, 128)  512         conv2d_2[0][0]                   
__________________________________________________________________________________________________
add (Add)                       (None, 41, 41, 128)  0           block2_pool[0][0]                
                                                                 batch_normalization[0][0]        
__________________________________________________________________________________________________
block3_sepconv1_act (Activation (None, 41, 41, 128)  0           add[0][0]                        
__________________________________________________________________________________________________
block3_sepconv1 (SeparableConv2 (None, 41, 41, 256)  33920       block3_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block3_sepconv1_bn (BatchNormal (None, 41, 41, 256)  1024        block3_sepconv1[0][0]            
__________________________________________________________________________________________________
block3_sepconv2_act (Activation (None, 41, 41, 256)  0           block3_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block3_sepconv2 (SeparableConv2 (None, 41, 41, 256)  67840       block3_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block3_sepconv2_bn (BatchNormal (None, 41, 41, 256)  1024        block3_sepconv2[0][0]            
__________________________________________________________________________________________________
conv2d_3 (Conv2D)               (None, 21, 21, 256)  32768       add[0][0]                        
__________________________________________________________________________________________________
block3_pool (MaxPooling2D)      (None, 21, 21, 256)  0           block3_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
batch_normalization_1 (BatchNor (None, 21, 21, 256)  1024        conv2d_3[0][0]                   
__________________________________________________________________________________________________
add_1 (Add)                     (None, 21, 21, 256)  0           block3_pool[0][0]                
                                                                 batch_normalization_1[0][0]      
__________________________________________________________________________________________________
block4_sepconv1_act (Activation (None, 21, 21, 256)  0           add_1[0][0]                      
__________________________________________________________________________________________________
block4_sepconv1 (SeparableConv2 (None, 21, 21, 728)  188672      block4_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block4_sepconv1_bn (BatchNormal (None, 21, 21, 728)  2912        block4_sepconv1[0][0]            
__________________________________________________________________________________________________
block4_sepconv2_act (Activation (None, 21, 21, 728)  0           block4_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block4_sepconv2 (SeparableConv2 (None, 21, 21, 728)  536536      block4_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block4_sepconv2_bn (BatchNormal (None, 21, 21, 728)  2912        block4_sepconv2[0][0]            
__________________________________________________________________________________________________
conv2d_4 (Conv2D)               (None, 11, 11, 728)  186368      add_1[0][0]                      
__________________________________________________________________________________________________
block4_pool (MaxPooling2D)      (None, 11, 11, 728)  0           block4_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
batch_normalization_2 (BatchNor (None, 11, 11, 728)  2912        conv2d_4[0][0]                   
__________________________________________________________________________________________________
add_2 (Add)                     (None, 11, 11, 728)  0           block4_pool[0][0]                
                                                                 batch_normalization_2[0][0]      
__________________________________________________________________________________________________
block5_sepconv1_act (Activation (None, 11, 11, 728)  0           add_2[0][0]                      
__________________________________________________________________________________________________
block5_sepconv1 (SeparableConv2 (None, 11, 11, 728)  536536      block5_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block5_sepconv1_bn (BatchNormal (None, 11, 11, 728)  2912        block5_sepconv1[0][0]            
__________________________________________________________________________________________________
block5_sepconv2_act (Activation (None, 11, 11, 728)  0           block5_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block5_sepconv2 (SeparableConv2 (None, 11, 11, 728)  536536      block5_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block5_sepconv2_bn (BatchNormal (None, 11, 11, 728)  2912        block5_sepconv2[0][0]            
__________________________________________________________________________________________________
block5_sepconv3_act (Activation (None, 11, 11, 728)  0           block5_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
block5_sepconv3 (SeparableConv2 (None, 11, 11, 728)  536536      block5_sepconv3_act[0][0]        
__________________________________________________________________________________________________
block5_sepconv3_bn (BatchNormal (None, 11, 11, 728)  2912        block5_sepconv3[0][0]            
__________________________________________________________________________________________________
add_3 (Add)                     (None, 11, 11, 728)  0           block5_sepconv3_bn[0][0]         
                                                                 add_2[0][0]                      
__________________________________________________________________________________________________
block6_sepconv1_act (Activation (None, 11, 11, 728)  0           add_3[0][0]                      
__________________________________________________________________________________________________
block6_sepconv1 (SeparableConv2 (None, 11, 11, 728)  536536      block6_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block6_sepconv1_bn (BatchNormal (None, 11, 11, 728)  2912        block6_sepconv1[0][0]            
__________________________________________________________________________________________________
block6_sepconv2_act (Activation (None, 11, 11, 728)  0           block6_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block6_sepconv2 (SeparableConv2 (None, 11, 11, 728)  536536      block6_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block6_sepconv2_bn (BatchNormal (None, 11, 11, 728)  2912        block6_sepconv2[0][0]            
__________________________________________________________________________________________________
block6_sepconv3_act (Activation (None, 11, 11, 728)  0           block6_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
block6_sepconv3 (SeparableConv2 (None, 11, 11, 728)  536536      block6_sepconv3_act[0][0]        
__________________________________________________________________________________________________
block6_sepconv3_bn (BatchNormal (None, 11, 11, 728)  2912        block6_sepconv3[0][0]            
__________________________________________________________________________________________________
add_4 (Add)                     (None, 11, 11, 728)  0           block6_sepconv3_bn[0][0]         
                                                                 add_3[0][0]                      
__________________________________________________________________________________________________
block7_sepconv1_act (Activation (None, 11, 11, 728)  0           add_4[0][0]                      
__________________________________________________________________________________________________
block7_sepconv1 (SeparableConv2 (None, 11, 11, 728)  536536      block7_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block7_sepconv1_bn (BatchNormal (None, 11, 11, 728)  2912        block7_sepconv1[0][0]            
__________________________________________________________________________________________________
block7_sepconv2_act (Activation (None, 11, 11, 728)  0           block7_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block7_sepconv2 (SeparableConv2 (None, 11, 11, 728)  536536      block7_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block7_sepconv2_bn (BatchNormal (None, 11, 11, 728)  2912        block7_sepconv2[0][0]            
__________________________________________________________________________________________________
block7_sepconv3_act (Activation (None, 11, 11, 728)  0           block7_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
block7_sepconv3 (SeparableConv2 (None, 11, 11, 728)  536536      block7_sepconv3_act[0][0]        
__________________________________________________________________________________________________
block7_sepconv3_bn (BatchNormal (None, 11, 11, 728)  2912        block7_sepconv3[0][0]            
__________________________________________________________________________________________________
add_5 (Add)                     (None, 11, 11, 728)  0           block7_sepconv3_bn[0][0]         
                                                                 add_4[0][0]                      
__________________________________________________________________________________________________
block8_sepconv1_act (Activation (None, 11, 11, 728)  0           add_5[0][0]                      
__________________________________________________________________________________________________
block8_sepconv1 (SeparableConv2 (None, 11, 11, 728)  536536      block8_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block8_sepconv1_bn (BatchNormal (None, 11, 11, 728)  2912        block8_sepconv1[0][0]            
__________________________________________________________________________________________________
block8_sepconv2_act (Activation (None, 11, 11, 728)  0           block8_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block8_sepconv2 (SeparableConv2 (None, 11, 11, 728)  536536      block8_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block8_sepconv2_bn (BatchNormal (None, 11, 11, 728)  2912        block8_sepconv2[0][0]            
__________________________________________________________________________________________________
block8_sepconv3_act (Activation (None, 11, 11, 728)  0           block8_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
block8_sepconv3 (SeparableConv2 (None, 11, 11, 728)  536536      block8_sepconv3_act[0][0]        
__________________________________________________________________________________________________
block8_sepconv3_bn (BatchNormal (None, 11, 11, 728)  2912        block8_sepconv3[0][0]            
__________________________________________________________________________________________________
add_6 (Add)                     (None, 11, 11, 728)  0           block8_sepconv3_bn[0][0]         
                                                                 add_5[0][0]                      
__________________________________________________________________________________________________
block9_sepconv1_act (Activation (None, 11, 11, 728)  0           add_6[0][0]                      
__________________________________________________________________________________________________
block9_sepconv1 (SeparableConv2 (None, 11, 11, 728)  536536      block9_sepconv1_act[0][0]        
__________________________________________________________________________________________________
block9_sepconv1_bn (BatchNormal (None, 11, 11, 728)  2912        block9_sepconv1[0][0]            
__________________________________________________________________________________________________
block9_sepconv2_act (Activation (None, 11, 11, 728)  0           block9_sepconv1_bn[0][0]         
__________________________________________________________________________________________________
block9_sepconv2 (SeparableConv2 (None, 11, 11, 728)  536536      block9_sepconv2_act[0][0]        
__________________________________________________________________________________________________
block9_sepconv2_bn (BatchNormal (None, 11, 11, 728)  2912        block9_sepconv2[0][0]            
__________________________________________________________________________________________________
block9_sepconv3_act (Activation (None, 11, 11, 728)  0           block9_sepconv2_bn[0][0]         
__________________________________________________________________________________________________
block9_sepconv3 (SeparableConv2 (None, 11, 11, 728)  536536      block9_sepconv3_act[0][0]        
__________________________________________________________________________________________________
block9_sepconv3_bn (BatchNormal (None, 11, 11, 728)  2912        block9_sepconv3[0][0]            
__________________________________________________________________________________________________
add_7 (Add)                     (None, 11, 11, 728)  0           block9_sepconv3_bn[0][0]         
                                                                 add_6[0][0]                      
__________________________________________________________________________________________________
block10_sepconv1_act (Activatio (None, 11, 11, 728)  0           add_7[0][0]                      
__________________________________________________________________________________________________
block10_sepconv1 (SeparableConv (None, 11, 11, 728)  536536      block10_sepconv1_act[0][0]       
__________________________________________________________________________________________________
block10_sepconv1_bn (BatchNorma (None, 11, 11, 728)  2912        block10_sepconv1[0][0]           
__________________________________________________________________________________________________
block10_sepconv2_act (Activatio (None, 11, 11, 728)  0           block10_sepconv1_bn[0][0]        
__________________________________________________________________________________________________
block10_sepconv2 (SeparableConv (None, 11, 11, 728)  536536      block10_sepconv2_act[0][0]       
__________________________________________________________________________________________________
block10_sepconv2_bn (BatchNorma (None, 11, 11, 728)  2912        block10_sepconv2[0][0]           
__________________________________________________________________________________________________
block10_sepconv3_act (Activatio (None, 11, 11, 728)  0           block10_sepconv2_bn[0][0]        
__________________________________________________________________________________________________
block10_sepconv3 (SeparableConv (None, 11, 11, 728)  536536      block10_sepconv3_act[0][0]       
__________________________________________________________________________________________________
block10_sepconv3_bn (BatchNorma (None, 11, 11, 728)  2912        block10_sepconv3[0][0]           
__________________________________________________________________________________________________
add_8 (Add)                     (None, 11, 11, 728)  0           block10_sepconv3_bn[0][0]        
                                                                 add_7[0][0]                      
__________________________________________________________________________________________________
block11_sepconv1_act (Activatio (None, 11, 11, 728)  0           add_8[0][0]                      
__________________________________________________________________________________________________
block11_sepconv1 (SeparableConv (None, 11, 11, 728)  536536      block11_sepconv1_act[0][0]       
__________________________________________________________________________________________________
block11_sepconv1_bn (BatchNorma (None, 11, 11, 728)  2912        block11_sepconv1[0][0]           
__________________________________________________________________________________________________
block11_sepconv2_act (Activatio (None, 11, 11, 728)  0           block11_sepconv1_bn[0][0]        
__________________________________________________________________________________________________
block11_sepconv2 (SeparableConv (None, 11, 11, 728)  536536      block11_sepconv2_act[0][0]       
__________________________________________________________________________________________________
block11_sepconv2_bn (BatchNorma (None, 11, 11, 728)  2912        block11_sepconv2[0][0]           
__________________________________________________________________________________________________
block11_sepconv3_act (Activatio (None, 11, 11, 728)  0           block11_sepconv2_bn[0][0]        
__________________________________________________________________________________________________
block11_sepconv3 (SeparableConv (None, 11, 11, 728)  536536      block11_sepconv3_act[0][0]       
__________________________________________________________________________________________________
block11_sepconv3_bn (BatchNorma (None, 11, 11, 728)  2912        block11_sepconv3[0][0]           
__________________________________________________________________________________________________
add_9 (Add)                     (None, 11, 11, 728)  0           block11_sepconv3_bn[0][0]        
                                                                 add_8[0][0]                      
__________________________________________________________________________________________________
block12_sepconv1_act (Activatio (None, 11, 11, 728)  0           add_9[0][0]                      
__________________________________________________________________________________________________
block12_sepconv1 (SeparableConv (None, 11, 11, 728)  536536      block12_sepconv1_act[0][0]       
__________________________________________________________________________________________________
block12_sepconv1_bn (BatchNorma (None, 11, 11, 728)  2912        block12_sepconv1[0][0]           
__________________________________________________________________________________________________
block12_sepconv2_act (Activatio (None, 11, 11, 728)  0           block12_sepconv1_bn[0][0]        
__________________________________________________________________________________________________
block12_sepconv2 (SeparableConv (None, 11, 11, 728)  536536      block12_sepconv2_act[0][0]       
__________________________________________________________________________________________________
block12_sepconv2_bn (BatchNorma (None, 11, 11, 728)  2912        block12_sepconv2[0][0]           
__________________________________________________________________________________________________
block12_sepconv3_act (Activatio (None, 11, 11, 728)  0           block12_sepconv2_bn[0][0]        
__________________________________________________________________________________________________
block12_sepconv3 (SeparableConv (None, 11, 11, 728)  536536      block12_sepconv3_act[0][0]       
__________________________________________________________________________________________________
block12_sepconv3_bn (BatchNorma (None, 11, 11, 728)  2912        block12_sepconv3[0][0]           
__________________________________________________________________________________________________
add_10 (Add)                    (None, 11, 11, 728)  0           block12_sepconv3_bn[0][0]        
                                                                 add_9[0][0]                      
__________________________________________________________________________________________________
block13_sepconv1_act (Activatio (None, 11, 11, 728)  0           add_10[0][0]                     
__________________________________________________________________________________________________
block13_sepconv1 (SeparableConv (None, 11, 11, 728)  536536      block13_sepconv1_act[0][0]       
__________________________________________________________________________________________________
block13_sepconv1_bn (BatchNorma (None, 11, 11, 728)  2912        block13_sepconv1[0][0]           
__________________________________________________________________________________________________
block13_sepconv2_act (Activatio (None, 11, 11, 728)  0           block13_sepconv1_bn[0][0]        
__________________________________________________________________________________________________
block13_sepconv2 (SeparableConv (None, 11, 11, 1024) 752024      block13_sepconv2_act[0][0]       
__________________________________________________________________________________________________
block13_sepconv2_bn (BatchNorma (None, 11, 11, 1024) 4096        block13_sepconv2[0][0]           
__________________________________________________________________________________________________
conv2d_5 (Conv2D)               (None, 6, 6, 1024)   745472      add_10[0][0]                     
__________________________________________________________________________________________________
block13_pool (MaxPooling2D)     (None, 6, 6, 1024)   0           block13_sepconv2_bn[0][0]        
__________________________________________________________________________________________________
batch_normalization_3 (BatchNor (None, 6, 6, 1024)   4096        conv2d_5[0][0]                   
__________________________________________________________________________________________________
add_11 (Add)                    (None, 6, 6, 1024)   0           block13_pool[0][0]               
                                                                 batch_normalization_3[0][0]      
__________________________________________________________________________________________________
block14_sepconv1 (SeparableConv (None, 6, 6, 1536)   1582080     add_11[0][0]                     
__________________________________________________________________________________________________
block14_sepconv1_bn (BatchNorma (None, 6, 6, 1536)   6144        block14_sepconv1[0][0]           
__________________________________________________________________________________________________
block14_sepconv1_act (Activatio (None, 6, 6, 1536)   0           block14_sepconv1_bn[0][0]        
__________________________________________________________________________________________________
block14_sepconv2 (SeparableConv (None, 6, 6, 2048)   3159552     block14_sepconv1_act[0][0]       
__________________________________________________________________________________________________
block14_sepconv2_bn (BatchNorma (None, 6, 6, 2048)   8192        block14_sepconv2[0][0]           
__________________________________________________________________________________________________
block14_sepconv2_act (Activatio (None, 6, 6, 2048)   0           block14_sepconv2_bn[0][0]        
__________________________________________________________________________________________________
global_average_pooling2d (Globa (None, 2048)         0           block14_sepconv2_act[0][0]       
__________________________________________________________________________________________________
dense_2 (Dense)                 (None, 10)           20490       global_average_pooling2d[0][0]   
==================================================================================================
Total params: 20,881,970
Trainable params: 20,490
Non-trainable params: 20,861,480
__________________________________________________________________________________________________

</details>


## Discussion/Next steps
<p align='middle'>
    <td><img src='img/accuracy_xc_model-20.png' align='center' style='width: 250px;'></td>
    <td><img src='img/accuracy_simple_cnn_model-20.png' align='center' style='width: 250px;'></td>
    
</p>

<p align='middle'>
<td><img src='img/loss_xc_model-20.png' align='center' style='width: 250px;'></td>
<td><img src='img/loss_simple_cnn_model-20.png' align='center' style='width: 247px;'></td>
</p>

<p align='middle'>
<td><img src='img/confusion_xc_model.png' align='center' style='width: 250px;'></td>
</p>

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
  

## References

Aversa, R., Modarres, M., Cozzini, S. et al. The first annotated set of scanning electron microscopy images for nanoscience. Sci Data 5, 180172 (2018). 
https://www.nature.com/articles/sdata2018172

F. Chollet, "Xception: Deep Learning with Depthwise Separable Convolutions," 2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), Honolulu, HI, 2017, pp. 1800-1807, doi: 10.1109/CVPR.2017.195.
https://arxiv.org/pdf/1610.02357.pdf


