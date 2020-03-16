import os
import argparse
from tqdm import tqdm

parser=argparse.ArgumentParser(description="Converts txt files to ply format.")
parser.add_argument("-o","--output",default=".",help="Directory/File to save converted files. Default= same as input directory")
parser.add_argument("-i","--input",required=True,help="Directory with txt files.")
ARGS=parser.parse_args()

def convert2ply(filename):
    with open(filename,"r") as f:
        lines=f.readlines()
    with open(os.path.join(ARGS.output,filename[:-3]+"ply"),"w") as f:
        cnt=lines[0].count(" ")
        f.write("ply\nformat ascii 1.0\nelement vertex {}\n".format(len(lines)))
        f.write("property float x\nproperty float y\nproperty float z\n")
	if cnt==3:
            #print("Uncoloured point cloud with sampled face id")
            f.write("property int face_id\nend_header\n")
        elif cnt==4:
            #print("Colour coded prediction")
            f.write("property float ground_truth\nproperty float prediction\nend_header\n")
        elif cnt==5:
            #print("Uncoloured point cloud")
            f.write("property float nx\nproperty float ny\nproperty float nz\nend_header\n")
        else:
            #print("Coloured point cloud")
            f.write("property float nx\n property float ny\nproperty float nz\n")
            f.write("property float red\n property float green\n property float blue\nproperty float transparency\nend_header\n")
        f.writelines(lines)


if __name__=="__main__":
    if not os.path.exists(ARGS.input):
        print("Input directory/file doesn't exist. Exiting...")
        exit()
    if ARGS.output==".":
        if os.path.isfile(ARGS.input):
            ARGS.output=os.path.dirname(ARGS.input)
        else:
            ARGS.output=ARGS.input
    elif not os.path.exists(ARGS.output):
        print("Output directory doesn't exist. Exiting...")
        exit()
    print(ARGS.output)

    if os.path.isfile(ARGS.input):
        with open(ARGS.input,"r") as f:
            for line in tqdm(f):
                convert2ply(line.strip())
    else:
        for root,_,files in os.walk(ARGS.input):
            for file in tqdm(files):
		if ".txt" in file:
                	convert2ply(os.path.join(root,file))
