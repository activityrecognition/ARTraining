import os
import random
import numpy as np
from PIL import Image
import pickle
import csv
from tflearn.data_utils import *
from tflearn.data_augmentation import ImageAugmentation

class ThermalImageAugmentation(ImageAugmentation):
    def add_random_temperature_fluctuation(self,max_degrees_change=2):
        """ add_random_flip_leftright.
        Randomly flip an image (left to right).
        Returns:
            Nothing.
        """
        self.methods.append(self._random_temperature_fluctuation)
        self.args.append([max_degrees_change])

    def _random_temperature_fluctuation(self, batch, max_degrees_change=2):
        for i in range(len(batch)):
            change = random.choice(np.arange(-max_degrees_change,max_degrees_change+1,0.5))
            if change != 0:
                func = np.vectorize(lambda x:max(0,min(x+2*change,239)))
                batch[i] = func(batch[i])
                #batch[i] = (2*change) + batch[i]
        return batch

def build_hdf5_thermal_image_dataset(target_path, image_shape, output_path='dataset.h5',
                                     mode='file', categorical_labels=True,
                                     normalize=True, grayscale=False,
                                     files_extension=None, chunks=True):
    """ Build HDF5 Image Dataset.
    Build an HDF5 dataset by providing either a root folder or a plain text
    file with images path and class id.
    'folder' mode: Root folder should be arranged as follow:
    ```
    ROOT_FOLDER -> SUBFOLDER_0 (CLASS 0) -> CLASS0_IMG1.jpg
                                         -> CLASS0_IMG2.jpg
                                         -> ...
                -> SUBFOLDER_1 (CLASS 1) -> CLASS1_IMG1.jpg
                                         -> ...
                -> ...
    ```
    Note that if sub-folders are not integers from 0 to n_classes, an id will
    be assigned to each sub-folder following alphabetical order.
    'file' mode: Plain text file should be formatted as follow:
    ```
    /path/to/img1 class_id
    /path/to/img2 class_id
    /path/to/img3 class_id
    ```
    Examples:
        ```
        # Load path/class_id image file:
        dataset_file = 'my_dataset.txt'
        # Build a HDF5 dataset (only required once)
        from tflearn.data_utils import build_hdf5_image_dataset
        build_hdf5_image_dataset(dataset_file, image_shape=(128, 128),
                                 mode='file', output_path='dataset.h5',
                                 categorical_labels=True, normalize=True)
        # Load HDF5 dataset
        import h5py
        h5f = h5py.File('dataset.h5', 'w')
        X = h5f['X']
        Y = h5f['Y']
        # Build neural network and train
        network = ...
        model = DNN(network, ...)
        model.fit(X, Y)
        ```
    Arguments:
        target_path: `str`. Path of root folder or images plain text file.
        image_shape: `tuple (height, width)`. The images shape. Images that
            doesn't match that shape will be resized.
        output_path: `str`. The output path for the hdf5 dataset. Default:
            'dataset.h5'
        mode: `str` in ['file', 'folder']. The data source mode. 'folder'
            accepts a root folder with each of his sub-folder representing a
            class containing the images to classify.
            'file' accepts a single plain text file that contains every
            image path with their class id.
            Default: 'folder'.
        categorical_labels: `bool`. If True, labels are converted to binary
            vectors.
        normalize: `bool`. If True, normalize all pictures by dividing
            every image array by 255.
        grayscale: `bool`. If true, images are converted to grayscale.
        files_extension: `list of str`. A list of allowed image file
            extension, for example ['.jpg', '.jpeg', '.png']. If None,
            all files are allowed.
        chunks: `bool` or `list of int`. Whether to chunks the dataset or not.
            Additionaly, a specific shape for each chunk can be provided.
    """
    import h5py

    assert image_shape, "Image shape must be defined."
    assert image_shape[0] and image_shape[1], \
        "Image shape error. It must be a tuple of int: ('width', 'height')."
    assert mode in ['folder', 'file'], "`mode` arg must be 'folder' or 'file'"

    if mode == 'folder':
        images, labels = directory_to_samples(target_path,
                                              flags=files_extension)
    else:
        with open(target_path, 'r') as f:
            images, labels = [], []
            for l in f.readlines():
                l = l.strip('\n').split()
                images.append(l[0])
                labels.append(int(l[1]))

    n_classes = np.max(labels) + 1

    d_imgshape = (len(images), image_shape[0], image_shape[1], 3) \
        if not grayscale else (len(images), image_shape[0], image_shape[1])
    d_labelshape = (len(images), n_classes) \
        if categorical_labels else (len(images), )

    dataset = h5py.File(output_path, 'w')
    dataset.create_dataset('X', d_imgshape, chunks=chunks)
    dataset.create_dataset('Y', d_labelshape, chunks=chunks)

    for i in range(len(images)):
        img = load_image(images[i])
        width, height = img.size
        if width != image_shape[0] or height != image_shape[1]:
            img = resize_image(img, image_shape[0], image_shape[1])
        if grayscale:
            img = img.split()[0]#convert_color(img, 'L')
        elif img.mode == 'L':
            img = convert_color(img, 'RGB')

        img = pil_to_nparray(img)
        if normalize:
            img /= 255.
        dataset['X'][i] = img
        if categorical_labels:
            dataset['Y'][i] = to_categorical([labels[i]], n_classes)[0]
        else:
            dataset['Y'][i] = labels[i]