from __future__ import (
    division,
    absolute_import,
    with_statement,
    print_function,
    unicode_literals,
)
import torch
import torch.utils.data as data
import numpy as np
import os
import h5py
import subprocess
import shlex

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_data_files(list_filename):
    with open(list_filename) as f:
        return [line.rstrip() for line in f]


def _load_data_file(name):
    f = h5py.File(name,"r")
    data = f["data"][:]
    label = f["label"][:]
    #print(data)
    label=np.reshape(label,(label.shape[0],label.shape[1]))
    #print(label[0])
    #print(label.shape)

    return data, label


class Indoor3DSemSeg(data.Dataset):
    def __init__(self, num_points,use_colour,split=""):
        super().__init__()
        BASE_DIR="path/to/directory/of/split/data/directories"
        self.num_points = num_points

        all_files = _get_data_files(os.path.join(BASE_DIR,split, "all_files.txt"))
        data_batchlist, label_batchlist = [], []
        for f in all_files:
            data, label = _load_data_file(os.path.join(BASE_DIR,split, f))
            data_batchlist.append(data)
            label_batchlist.append(label)

        self.points = np.concatenate(data_batchlist, axis=0)
        self.labels = np.concatenate(label_batchlist, axis=0)

        if use_colour==0:
            self.points=self.points[...,0:6]

    def __getitem__(self, idx):
        pt_idxs = np.arange(0, self.num_points)
        np.random.shuffle(pt_idxs)
        current_points = torch.from_numpy(self.points[idx, pt_idxs].copy()).type(
            torch.FloatTensor
        )
        current_labels = torch.from_numpy(self.labels[idx, pt_idxs].copy()).type(
            torch.LongTensor
        )

        return current_points, current_labels,idx

    def __len__(self):
        return int(self.points.shape[0])

    def set_num_points(self, pts):
        self.num_points = pts

    def randomize(self):
        pass


if __name__ == "__main__":
    dset = Indoor3DSemSeg(16, train=True)
    print(dset[0])
    print(len(dset))
    dloader = torch.utils.data.DataLoader(dset, batch_size=32, shuffle=True)
    for i, data in enumerate(dloader, 0):
        inputs, labels = data
        print(inputs)
        print (labels)
        if i == len(dloader) - 1:
            print(inputs.size())
