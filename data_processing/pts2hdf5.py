import h5py
import numpy as np
import argparse
import os
from tqdm import tqdm

parser=argparse.ArgumentParser(description="Write point clouds in hdf5 file with along with their labels. Label files must have the same filename as the point cloud.")
parser.add_argument("-i","--input",required=True,help="Directory with point clouds to write in hdf5 format.")
parser.add_argument("-l","--label",required=True,help="Directory with point labels.")
parser.add_argument("-o","--output",default=".",help="Name of output file.(Will be saved in the same directory as the input files.) Default: models.hdf5")
ARGS=parser.parse_args()

if __name__=="__main__":
	if not os.path.exists(ARGS.input) or os.path.isfile(ARGS.input):
		print("Problem with input. Check if the path to the directory is correct or if it is indeed a directory. Exiting...")
		exit()
	if ARGS.output==".":
		ARGS.output=os.path.join(ARGS.input,"models.hdf5")
	else:
		ARGS.output=os.path.join(ARGS.input, ARGS.output)
	points=[]
	labels=[]
	h=h5py.File(ARGS.output,"w")
	for root,_,files in os.walk(ARGS.input):
		for file in tqdm(files):
			if ".txt" in file:
				pc=np.loadtxt(os.path.join(root,file))
				points.append(pc)
				l=np.loadtxt(os.path.join(ARGS.label,file))
				labels.append(l)
	h.create_dataset("data",data=points,compression='gzip',compression_opts=4,dtype='float32')
	h.create_dataset('label',data=labels,compression='gzip',compression_opts=4,dtype='int32')
