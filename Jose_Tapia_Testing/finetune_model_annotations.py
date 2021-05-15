# -*- coding: utf-8 -*-
"""
finetune_model
Finetune a convnet from a pretrained model using training and validation data
This is based heavily on The Transfer Learning Tutorial from pytorch:
https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
"""
# License: BSD
# Author(s): Paul Roberts, Eric Orenstein

from __future__ import print_function, division
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

"""
train_model
finetunes the net based on input params and train/val data
"""
def train_model(model, criterion, optimizer, scheduler,
    dataloaders, classes, num_epochs=25):

    since = time.time()
    
    torch.cuda.is_available()
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                scheduler.step()
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            class_corrects = np.zeros(len(classes))
            class_counts = np.zeros(len(classes))

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

                for i,p in enumerate(preds):
                    class_corrects[labels.data[i]] += p == labels.data[i]
                    class_counts[labels.data[i]] += 1


            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            class_acc = class_corrects/class_counts

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            for i,c in enumerate(classes):
                print('{} Class: {} Acc {:.4f}'.format(phase,c,class_acc[i]))


            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())

        print()

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    # load best model weights
    model.load_state_dict(best_model_wts)
    return model


if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Finetune a convnet')

    parser.add_argument('data_dir',metavar='data_dir',help='path to train and val data')

    parser.add_argument('--model',default='resnet18',choices=['resnet18','resnet34','squeezenet'],
        help='The type of model to finetune')

    parser.add_argument('--epochs',default=24,type=int,help='The number of training epochs')

    args = parser.parse_args()

    nepochs = args.epochs
    

    # Data augmentation and normalization for training
    # Just normalization for validation
    data_transforms = {
        'train': transforms.Compose([
            #transforms.RandomResizedCrop(224),
            transforms.Resize((224,224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomAffine(degrees=0,scale=(0.5, 2), shear=(-5, 5)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((224,224)),
            #transforms.CenterCrop(128),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    data_dir = args.data_dir 
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                              data_transforms[x])
                      for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=8,
                                                 shuffle=True, num_workers=4)
                  for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes

    
    
    #torch.cuda.is_available()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(torch.cuda.device_count())
    print(torch.cuda.current_device())
    print(torch.cuda.get_device_name(torch.cuda.current_device()))
    print(torch.cuda.is_available())
    #print(device)

    model_type = 'resnet18'

    if model_type == 'resnet34':
        model_conv = models.resnet34(pretrained=True)
        num_ftrs = model_conv.fc.in_features
        model_conv.fc = nn.Linear(num_ftrs, len(class_names))
    if model_type == 'resnet18':
        model_conv = models.resnet18(pretrained=True)
        num_ftrs = model_conv.fc.in_features
        model_conv.fc = nn.Linear(num_ftrs, len(class_names))
    if model_type == 'squeezenet':
        model_conv = models.squeezenet1_0(pretrained=True)
        # change the last Conv2D layer in case of squeezenet. there is no fc layer in the end.
        num_ftrs = 512
        model_conv.classifier._modules["1"] = nn.Conv2d(512, len(classes), kernel_size=(1, 1))
        # because in forward pass, there is a view function call which depends on the final output class size.
        model_conv.num_classes = len(classes)

    model_conv = model_conv.to(device)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_conv.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    # do the training and validation
    model_conv = train_model(model_conv, criterion, optimizer_ft, exp_lr_scheduler,
                           dataloaders, class_names, num_epochs= nepochs)


    # save the trained model
    torch.save(model_conv.state_dict(),
        os.path.join(data_dir,model_type+'_'+str(int(time.time()))+'_model_conv.pt'))



    def imshow(inp, title=None):
        """Imshow for Tensor."""
        inp = inp.numpy().transpose((1, 2, 0))
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        inp = std * inp + mean
        inp = np.clip(inp, 0, 1)
        plt.imshow(inp)
        if title is not None:
            plt.title(title)
        plt.pause(0.001)  # pause a bit so that plots are updated


    # Get a batch of training data
    inputs, classes = next(iter(dataloaders['train']))
    
    # Make a grid from batch
    out = torchvision.utils.make_grid(inputs)
    
    #
    
    imshow(out, title=[class_names[x] for x in classes])    
    
    #Visualizing the data.  
    def visualize_model(model, num_images=6):
        was_training = model.training
        model.eval()
        images_so_far = 0
       
    
        with torch.no_grad():
            for i, (inputs, labels) in enumerate(dataloaders['val']):
                inputs = inputs.to(device)
                labels = labels.to(device)
    
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
    
                for j in range(inputs.size()[0]):
                    images_so_far += 1
                    ax = plt.subplot(num_images//2, 2, images_so_far)
                    ax.axis('off')
                    ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                    imshow(inputs.cpu().data[j])
    
                    if images_so_far == num_images:
                        model.train(mode=was_training)
                        return
            model.train(mode=was_training)
    
    visualize_model(model_conv)

    plt.legend(frameon=False)
    
    plt.ioff()
    plt.show()