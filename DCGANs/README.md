# DCGANs : Overview and Implementation

<img src="./assets/first.png" alt="DCGANs overall">
<hr>

DCGANs (Deep Convolutional Generative Adversial Networks) : 

### Architecture

<img src="./assets/second.png" alt="DCGANs overall">
<hr>

I find it truly amazing that there are no fully connected layers in the complete architecture of DCGANs. We only have convolutional layers in the network. 

The generator network in the DCGAN model is structured like this : 

First, we give the generator a 100-dimensional noise vector as input, project and reshape it. Then we have 4 convolutional operations. Now each time we get an increment in height and width and the channels keep on reducing. We start with 512 output channels and reduce it down to 128. And finally we generate an image of 64 X 64 dimensions and three output channels. Also in the convolutional layers, after the first layer, all other layers have a stride of 2. 

Also in the architecture, we do not use max pooling for downsampling as should be clear from the fact that there are no fully connected layers. All the operations will be through strided convolutions only. 

The authors of the paper provide a stable way to train DCGAN and most of it boils down to two things. The first is how we build the generator/discriminator and the second is how we set the parameters/hyperparameters. 

In the generator, we use the ReLU activation function in all the layers except the last one. For the last layer, we use the Tanh activation Function. While For the discriminator, we will use LeakyReLU for all the convolutional layers after applying Batch Normalization. 

Further the authors have provided certain HyperParameters that I will use while implementing the DCGAN.