# importing essential libraries
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils import data
import torchvision

import matplotlib.pyplot as plt
import numpy as np

# setting up the hyperparameters
learning_rate = 2e-4
noise_dim = 32
image_dim = 28 * 28 * 1
batch_size = 32
num_epochs = 25

# Creating the Generator and Discriminator classes
class Generator(nn.Module):
    def __init__(self, noise_dim, image_dim):
        super(Generator, self).__init__()
        self.linear1 = nn.Linear(noise_dim, 128)
        self.relu = nn.LeakyReLU(0.01)
        self.linear2 = nn.Linear(128, image_dim)
        self.tanh = nn.Tanh()

    def forward(self, x):
        out = self.linear1(x)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.tanh(out)
        return out


class Discriminator(nn.Module):
    def __init__(self, in_image):
        super(Discriminator, self).__init__()
        self.linear1 = nn.Linear(in_image, 64)
        self.relu = nn.LeakyReLU(0.01)
        self.linear2 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.linear1(x)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.sigmoid(out)
        return out

# Creating the objects of the Generator and Discriminator classes
discriminator = Discriminator(image_dim)
generator = Generator(noise_dim, image_dim)
noise = torch.randn((batch_size, noise_dim))

# Loading the dataset
tf = torchvision.transforms.Compose(
    [torchvision.transforms.ToTensor(), torchvision.transforms.Normalize((0.5,), (0.5,)),]
)
ds = torchvision.datasets.MNIST(root="dataset/gan/", transform=tf, download=True)
loader = data.DataLoader(ds, batch_size=batch_size, shuffle=True)

# Visualizing real data
real_sample = next(iter(loader))[0]
img_grid_real = torchvision.utils.make_grid(real_sample, normalize=True)
npgrid = img_grid_real.cpu().numpy()
plt.imshow(np.transpose(npgrid, (1, 2, 0)), interpolation='nearest')
plt.axis('off')
plt.show()

# setting up the optimizers
opt_discriminator = optim.Adam(discriminator.parameters(), lr=learning_rate)
opt_generator = optim.Adam(generator.parameters(), lr=learning_rate)
criterion = nn.BCELoss()

# Training the GAN
for epoch in range(num_epochs):
    for id, (training_sample, _) in enumerate(loader):
        training_sample = training_sample.view(-1, 784)
        batch_size = training_sample.shape[0]

        # Training the Discriminator
        noise = torch.randn(batch_size, noise_dim)
        fake_sample = generator(noise)
        disc_realSample = discriminator(training_sample).view(-1)
        lossD_realSample = criterion(
            disc_realSample, torch.ones_like(disc_realSample))
        disc_fakeSample = discriminator(fake_sample).view(-1)
        lossD_fakeSample = criterion(
            disc_fakeSample, torch.zeros_like(disc_fakeSample))
        lossD = (lossD_realSample + lossD_fakeSample) / 2
        discriminator.zero_grad()
        # we are trying to minimize the total classification error
        lossD.backward(retain_graph=True)
        opt_discriminator.step()

        # Training the Generator
        lossD_fakeSample = discriminator(fake_sample).view(-1)
        # we are trying to maximize the error of classification of fake image by the discriminator
        lossG = criterion(lossD_fakeSample, torch.ones_like(lossD_fakeSample))
        generator.zero_grad()
        lossG.backward()
        opt_generator.step()

        if id == 0:
            print("Epoch: {epoch} \t Discriminator Loss: {lossD} Generator Loss: {lossG}".format(
                epoch=epoch, lossD=lossD, lossG=lossG))


# Visualizing fake data
fake = generator(noise).reshape(-1, 1, 28, 28)
img_grid_fake = torchvision.utils.make_grid(fake, normalize=True)
npgrid_fake = img_grid_fake.cpu().numpy()
plt.figure()
plt.imshow(np.transpose(npgrid_fake, (1, 2, 0)), interpolation='nearest')
plt.axis('off')
plt.show()
