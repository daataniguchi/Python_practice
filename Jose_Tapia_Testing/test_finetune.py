# -*- coding: utf-8 -*-
"""
deply a trained_model
Deploys a trained model on a set of unlabeled images. Output is lists of image paths, seperated into the appropriate label.
With a flag will save mosaics of labeled images.
This is based heavily on The Transfer Learning Tutorial from pytorch:
https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
"""
# License: BSD
# Author(s): Paul Roberts, Eric Orenstein


from __future__ import print_function, division

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms


import os

import shutil
import argparse



class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path



if __name__ == "__main__":

    # define parser
    parser = argparse.ArgumentParser(description='Make a train and val set from labels')

    parser.add_argument('data_dir', metavar='data_dir', help='path to unlabeled data')
    parser.add_argument('test_output', metavar='test_output', help='path to the output directory')
    parser.add_argument('saved_model', metavar='saved_model', help='path to trained weights')


    args = parser.parse_args()

    data_dir = args.data_dir
    test_output = args.test_output
    saved_model = args.saved_model


    # Data augmentation and normalization for training 
    # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomAffine(degrees=0,scale=(0.5, 2),shear=(-5, 5)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }


    # image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
    #                                           data_transforms[x])
    #                   for x in ['train', 'val']}
    # dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
    #                                              shuffle=True, num_workers=4)
    #               for x in ['train', 'val']}
    # dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    # class_names = image_datasets['train'].classes

    test_dataset = ImageFolderWithPaths(data_dir, data_transforms['val'])

    dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=8,
                                             shuffle=True, num_workers=4)

    class_names = ['Ciliate','L_poly', 'Other']

    print(class_names)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # load the saved model
    model_conv = models.resnet18(pretrained=True)
    num_ftrs = model_conv.fc.in_features
    model_conv.fc = nn.Linear(num_ftrs, len(class_names))
    model_conv.load_state_dict(torch.load(saved_model))

    model_conv = model_conv.to(device)

    model_conv.eval()

    optimizer = optim.SGD(model_conv.parameters(), lr=0.001, momentum=0.9)

    

    for inputs, labels, paths in dataloader:
        inputs = inputs.to(device)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward
        # track history if only in train
        with torch.set_grad_enabled(False):
            outputs = model_conv(inputs)
            _, preds = torch.max(outputs, 1)

        for i, p in enumerate(preds):

            dir_name = os.path.join(test_output, class_names[p])

            if not os.path.exists(dir_name):
                os.makedirs(dir_name)



            # copy image to dir
            #If a folder exists, this line will return an error. Delete your output folder and rerun the code if needed.
            shutil.copy(paths[i],dir_name)
    
