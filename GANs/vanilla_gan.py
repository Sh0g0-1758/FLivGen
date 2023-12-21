# After understanding the paper on GANs by Ian J. Goodfellow, Here is the implementation of the same.

# Vanilla GAN architecture using Linear neural network layers

# While Training, the D and G need to train simultaneously. We can implement this using Threads but that gets complicated. So we will try a different approach. 

# Training the Discriminator : Get the real data and labels. Do a forward pass into the DNN to get the real output. Use it to calculate the D-Loss and backpropagate it. Use the noice vector, generate fake data and labels using the generator and do a forward pass through the Discriminator to get the fake output. Use it to calculate the D-Loss and backpropagate it. Add the two losses and update the weights of the Discriminator.

# Training the Generator : Use the noice vector, generate fake data and labels using the generator and do a forward pass through the Discriminator to get the fake output. Use it to calculate the G-Loss and backpropagate it. Update the weights of the Generator.

# Importing the libraries
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torch.optim as optim
import torchvision.datasets as datasets
import imageio
import numpy as np
import matplotlib
from torchvision.utils import make_grid, save_image # to save PyTorch tensor images
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt
from tqdm import tqdm
matplotlib.style.use('ggplot')

# learning parameters
batch_size = 512 # Since the MNIST data-set is small, we can use much greater batch size also. 
epochs = 200 # number of training Epochs. After 200 epochs, the images will be clear. Less epochs will produce random noise.
sample_size = 64 # fixed sample size
nz = 128 # latent / noise vector size
k = 1 # number of steps to apply to the discriminator
# Citing Algorithm 1 mentioned in the paper as the reason : 
# Algorithm 1 Minibatch stochastic gradient descent training of generative adversarial nets. The number of
# steps to apply to the discriminator, k, is a hyperparameter. We used k = 1, the least expensive option, in our
# experiments.
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Preparing the dataset
transform = transforms.Compose([
                                transforms.ToTensor(),
                                transforms.Normalize((0.5,),(0.5,)),
]) # This converts the images to tensors and normalizes them as well

to_pil_image = transforms.ToPILImage() # To convert the images into PIL format, will be useful in changing the images in gif format. 

train_data = datasets.MNIST(
    root='dataset/vanilla_gan/',
    train=True,
    download=True,
    transform=transform
)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True) # loading the data in batches

# Generator Network
class Generator(nn.Module):
    def __init__(self, nz):
        super(Generator, self).__init__()
        self.nz = nz
        self.main = nn.Sequential(
            nn.Linear(self.nz, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, 784),
            nn.Tanh(),
        )
    def forward(self, x):
        return self.main(x).view(-1, 1, 28, 28)