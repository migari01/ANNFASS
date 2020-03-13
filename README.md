# ANNFASS

## &nbsp; Introduction

The Artificial Neural Network Framework for understanding historical monuments Architectural Structure and Style, in short ANNFASS, uses several deep learning methods for the studying and understanding of buildings/monuments in 3D format. At the end of the project, an online tool will be introduced to people with interest to this kind of data, such as archeologists and architects, with the hope of making them more keen to the use of such tools.

Our main goals are:
- Recognise the structure and style of monuments with deep learning neural networks
- Exctract building/monument grammar and generate new buildings of a certain period (ex. Byzantine)
- Set the base for a 3D monument database
- Build an online platform broadly accepted, and
- Preserve cultural heritage

## 1 &nbsp; Installation
Currently, we are using two different artificial neural networks in our project, that need to be seperately setup, since one is built in [Caffe](https://github.com/BVLC/caffe) framework and the other on [PyTorch](https://pytorch.org/).

Clone ANNFASS directory, so that you will have the required files to make the necessary changes and recreate our project.

### 1.1 &nbsp; (A)O-CNN Setup
1. Follow the steps for installing the [O-CNN and AO-CNN](https://github.com/microsoft/O-CNN), as described in [**1.1 Manual Setup**](https://github.com/microsoft/O-CNN#11--manual-setup). If the ***make runtest*** command produces and error, you can ignore it and continue to the next steps. But ***make all*** must be completed without any errors (warnings can be ignored). **Make sure you have all the prerequisites of [Caffe](https://github.com/BVLC/caffe) before building the project**

2. Once [Caffe](https://github.com/BVLC/caffe) and [(A)O-CNN](https://github.com/microsoft/O-CNN) are setup, copy the code under our `(A)O-CNN/caffe` directory into the caffe directory. Build the project again, in order to overwrite the initial code and integrate our changes.

### 1.2 &nbsp; PointNet++ Setup
1. For installing the [PointNet++](https://github.com/charlesq34/pointnet2), follow the instractions of the [PyTorch](https://pytorch.org/) implementation here: `https://github.com/erikwijmans/Pointnet2_PyTorch#setup`
2. **Before installing** the dependencies of [Pointnet2_PyTorch](https://github.com/erikwijmans/Pointnet2_PyTorch) and building the project, our changes need to be integrated.
   - Clone/Download the [etw_pytorch_utils](https://github.com/erikwijmans/etw_pytorch_utils) directory and replace the script `etw_pytorch_utils/pytorch_utils.py` with the one we provide.
   - Change the first line of `Pointnet2_PyTorch/requirements.txt` from `git+git://github.com/erikwijmans/etw_pytorch_utils.git@v1.1.1#egg=etw_pytorch_utils` to the path of the `etw_pytorch_utils` directory you just downloaded.
   - Replace the scripts `Pointnet2_PyTorch/data/Indoor3DSemSegLoader.py` and `Pointnet2_PyTorch/train/train_sem_seg.py` with the ones we provide.

## 2 &nbsp; Data Preprocessing
1. The first step of data preprocessing for both methods is sample points from the 3D models. This can be done with any sampling method, in our case we preferred [Thea](https://github.com/sidch/Thea) toolkit, because:
   - Processes the file format of our models (OBJ)
   - Produces uniformly sampled point clouds and their normals
   - Resulting samples have exactly the predifined number of points
   - Returns the mesh triangle from which the points were sampled (_optional, needed for point colour finding_)

 ***Be sure that the models are triangulated, in order for Thea to work as expected.***   

 Information on how to install and use [Thea](https://github.com/sidch/Thea) can be found here: `https://github.com/sidch/Thea`

If you want to run experiments **only** with the spatial coordinates and normals (**no point colours**), you can skip the next steps and continue to sections [2.1 (A)O-CNN](https://github.com/migari01/ANNFASS#21--ao-cnn) and [2.2 PointNet++](https://github.com/migari01/ANNFASS#22--pointnet), for the method specific data preprocessing steps.

2. Once you have the point cloud for each model you need to extract their colour. To do that you can use the script `getPixelColorFromTextureFromOBJ.py`.  It can be used to find the colours of a single mesh's samples or of a list of meshes, example executions:

 Single file:
`python getPixelColorFromTextureFromOBJ.py file filename path/to/obj/file/directory path/to/texture/folder/directory path/to/ply/file/directory path/to/mtl/file/directory path/to/save/coloured/ply`

 List of files:
`python getPixelColorFromTextureFromOBJ.py list path/to/file/listing/filenames/to/process path/to/obj/file/directory path/to/texture/folder/directory path/to/ply/file/directory path/to/mtl/file/directory path/to/save/coloured/ply`
**Note** The obj, mtl, ply files and the texture folder must have the same name as the filename (or listed filenames) parameter.
### 2.1 &nbsp; (A)O-CNN
Details will be added soon.
### 2.2 &nbsp; PointNet++
Details will be added soon.

***Our work uses implementations from the following repositories:***

* _Caffe:_ https://github.com/BVLC/caffe.git
* _(A)O-CNN:_ https://github.com/microsoft/O-CNN.git
* _Caffe weighted Softmax:_ https://github.com/gustavla/caffe/tree/gustav
* _PointNet++:_ https://github.com/erikwijmans/Pointnet2_PyTorch#example-training
