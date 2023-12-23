import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def create_noise(sample_size, nz):
    """
    Fucntion to create noise
    :param sample_size: fixed sample size or batch size
    :param nz: latent vector size
    :returns random noise vector
    """
    return torch.randn(sample_size, nz, 1, 1).to(device)

print(create_noise(64, 128))
