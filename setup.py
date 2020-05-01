from setuptools import find_packages, setup
import torch

torch_ver = [int(x) for x in torch.__version__.split(".")[:2]]
assert torch_ver >= [1, 4], "Requires PyTorch >= 1.4"

setup(
    name='background_changer',
    packages=find_packages(exclude="configs"),
    version='0.1.0',
    description='Change Background of videos for data augmentation using Instance Segmentation.',
    author='Hamza Mughal',
    python_requires=">=3.6",
    install_requires=[
        "yacs>=0.1.6",
        "pyyaml>=5.1",
        "numpy",
        "fvcore",
        "detectron2",
        "opencv-python",
    ],
    license='MIT',
)
