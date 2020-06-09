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

The dataset contains 21,283 scanning electron microscope (SEM) images produced at Institute of Materials, CNR (https://b2share.eudat.eu/records/80df8606fcdb4b2bae1656f0dc6db8ba)

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









<img src='img/example_categories_plot.png' align='center' style='width: 800px;'>

## Exploratory Data Analysis

## Models


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


