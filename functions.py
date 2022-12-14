import torch
import numpy as np
import glob
import os
import contextlib
from scipy.io import loadmat
from renderer import Renderer

def supress_stdout(func):
    def wrapper(*a, **ka):
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                return func(*a, **ka)
    return wrapper


class Sampler():
    def __init__(self,
        file_path = "/media/socialvv/d5a43ee1-58b7-4fc1-a084-7883ce143674/SG2_Skeleton/datasets/ffhq_coeffs_224_aligned/*"):
        self.mat_list = np.array(list(glob.glob(file_path)))
        self.n = len(self.mat_list)
    
    def sample_m(self, batch_size):
        # mat_paths = self.mat_list[np.random.randint(self.n, size=batch_size)]
        coeff_tensor = np.zeros((batch_size, 257))

        # print(mat_paths)
        for i in range(batch_size):
            coeff_tensor[i] = self.sample_m_single()
            # coeff_tensor[i] = self.sample_m_single_ffhq()
        coeff_tensor = torch.from_numpy(coeff_tensor).float()
        # print(coeff_tensor)
        # print(coeff_tensor.shape)
        return coeff_tensor

    def sample_m_single(self):
        # Dirac Delta in the product space
        d_delta_idx = np.random.randint(0, self.n, size=6)

        coeffs = np.hstack([
            loadmat(self.mat_list[d_delta_idx[0]])["id"],
            loadmat(self.mat_list[d_delta_idx[1]])["exp"],
            loadmat(self.mat_list[d_delta_idx[2]])["tex"],
            loadmat(self.mat_list[d_delta_idx[3]])["angle"],
            loadmat(self.mat_list[d_delta_idx[4]])["gamma"],
            loadmat(self.mat_list[d_delta_idx[3]])["trans"],
        ]).squeeze()

        return coeffs

    def sample_m_single_ffhq(self):
        idx = np.random.randint(self.n)
        coeffs = np.hstack([
            loadmat(self.mat_list[idx])["id"],
            loadmat(self.mat_list[idx])["exp"],
            loadmat(self.mat_list[idx])["tex"],
            loadmat(self.mat_list[idx])["angle"],
            loadmat(self.mat_list[idx])["gamma"],
            loadmat(self.mat_list[idx])["trans"],
        ]).squeeze()

        return coeffs

sampler = Sampler()

def sample_m(batch_size):
    return sampler.sample_m(batch_size)

def run_test():
    renderer = Renderer()
    sampler = Sampler()
    coeffs_tensor = sampler.sample_m_single()
    img_tensor, _ = renderer.render(coeffs_tensor, 1)
    renderer.visualize(img_tensor, path = 'test_output/sample_m_single.png')

# Testing here
if __name__ == "__main__":
    run_test()
