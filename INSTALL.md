## Installing Instructions

The codebase relies on FAIR's [Detectron2](https://github.com/facebookresearch/detectron2). Therefore you need to install detectron2 by following instructions in [INSTALL.md](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md):

### Requirements
- torch ≥ 1.4
- torchvision - that matches the PyTorch installation.
- opencv-python
- cython
- pycocotools
- pyyaml
- gcc & g++ ≥ 5 

```
pip install -U torch==1.4 torchvision==0.5
pip install cython pyyaml==5.1
pip install -U 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```
For more detailed instructions, follow steps [here](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md).

### Background-Changer Setup
First clone the repository:
```
git clone https://github.com/m-hamza-mughal/background_changer.git
```

Then add the repository to PYTHONPATH
```
export PYTHONPATH=/path/to/background_changer/background_changer:$PYTHONPATH
```

Finally, run:
```
python setup.py build develop
```