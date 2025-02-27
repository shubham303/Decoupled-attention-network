# coding:utf-8
import torch
import torch.optim as optim
import os
from dataset_scene import *
from torchvision import transforms
from DAN import *

global_cfgs = {
    'state': 'Train',
    'epoch': 10,
    'show_interval': 1000,
    'test_interval': 1000
}

dataset_cfgs = {
    'dataset_train': lmdbDataset,
    'dataset_train_args': {
        'roots': ['/nlsasfs/home/ai4bharat/shubhamr/shubham/recognition-dataset/malayalam/training/MJ/MJ_test', '/nlsasfs/home/ai4bharat/shubhamr/shubham/recognition-dataset/malayalam/training/MJ/MJ_train'
                  ,'/nlsasfs/home/ai4bharat/shubhamr/shubham/recognition-dataset/malayalam/training/ST'],
        'img_height': 32,
        'img_width': 128,
        'transform': transforms.Compose([transforms.ToTensor()]),
        'global_state': 'Train',
    },
    'dataloader_train': {
        'batch_size': 48,
        'shuffle': True,
        'num_workers': 3,
    },

    'dataset_test': lmdbDataset,
    'dataset_test_args': {
        'roots': ['/nlsasfs/home/ai4bharat/shubhamr/shubham/recognition-dataset/malayalam/evaluation/IIIT'],
        'img_height': 32,
        'img_width': 128,
        'transform': transforms.Compose([transforms.ToTensor()]),
        'global_state': 'Test',
    },
    'dataloader_test': {
        'batch_size': 36,
        'shuffle': False,
        'num_workers': 3,
    },

    'case_sensitive': False,
    'dict_dir' : 'dict/dic_ml.txt'
}

net_cfgs = {
    'FE': Feature_Extractor,
    'FE_args': {
        'strides': [(1,1), (2,2), (1,1), (2,2), (1,1), (1,1)],
        'compress_layer' : False, 
        'input_shape': [1, 32, 128], # C x H x W
    },
    'CAM': CAM,
    'CAM_args': {
        'maxT': 25, 
        'depth': 8, 
        'num_channels': 64,
    },
    'DTD': DTD,
    'DTD_args': {
        'nclass': 119, # extra 2 classes for Unkonwn and End-token
        'nchannel': 512,
        'dropout': 0.3,
    },

    'init_state_dict_fe':"/nlsasfs/home/ai4bharat/shubhamr/shubham/programs/Decoupled-attention-network/models/scene"
                         "/exp2_E0_I30000-98451_M0.pth",
    'init_state_dict_cam':"/nlsasfs/home/ai4bharat/shubhamr/shubham/programs/Decoupled-attention-network/models/scene"
                          "/exp2_E0_I30000-98451_M1.pth",
    'init_state_dict_dtd': "/nlsasfs/home/ai4bharat/shubhamr/shubham/programs/Decoupled-attention-network/models"
                           "/scene/exp2_E0_I30000-98451_M2.pth"
}

optimizer_cfgs = {
    # optim for FE
    'optimizer_0': optim.Adadelta,
    'optimizer_0_args':{
        'lr': 1.0,
    },

    'optimizer_0_scheduler': optim.lr_scheduler.MultiStepLR,
    'optimizer_0_scheduler_args': {
        'milestones': [3, 5],
        'gamma': 0.1,
    },

    # optim for CAM
    'optimizer_1': optim.Adadelta,
    'optimizer_1_args':{
        'lr': 1.0,
    },
    'optimizer_1_scheduler': optim.lr_scheduler.MultiStepLR,
    'optimizer_1_scheduler_args': {
        'milestones': [3, 5],
        'gamma': 0.1,
    },

    # optim for DTD
    'optimizer_2': optim.Adadelta,
    'optimizer_2_args':{
        'lr': 1.0,
    },
    'optimizer_2_scheduler': optim.lr_scheduler.MultiStepLR,
    'optimizer_2_scheduler_args': {
        'milestones': [3, 5],
        'gamma': 0.1,
    },
}

saving_cfgs = {
    'saving_iter_interval': 10000,
    'saving_epoch_interval': 1,
    'saving_path': 'models/scene/exp2_',
}

def mkdir(path_):
    paths = path_.split('/')
    command_str = 'mkdir '
    for i in range(0, len(paths) - 1):
        command_str = command_str + paths[i] + '/'
    command_str = command_str[0:-1]
    os.system(command_str)

def showcfgs(s):
    for key in s.keys():
        print(key , s[key])
    print('')

mkdir(saving_cfgs['saving_path'])
