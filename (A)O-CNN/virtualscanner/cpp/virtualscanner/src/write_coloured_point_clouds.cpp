#include "points.h"
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>


using namespace std;

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cout << "Usage: write_coloured_point_clouds.exe <file name/folder name> "
    "[labels]" << endl;
    return 0;
  }
  string filename=argv[1];
  string label;
  if(argc==3){
    label=argv[2];
  }
  else if (argc>3){
    cout<<"Invalid number of inputs"<<endl;
    return 0;
  }

  ifstream infile(filename.c_str());
  float x,y,z,nx,ny,nz,r,g,b,a;
  int n=0;
  Points point_cloud;
  // points(3 channels) are required,  labels(1 channel) are optional,
  // and at least one of normal(3 channels) and features(any channels) are required.
  vector<float> points, normals, features, labels;
  string line;
  while(getline(infile,line)){
    if (line.find("element vertex")!= string::npos){
      stringstream ss;
    	/* Storing the whole string into string stream */
    	ss << line;
    	/* Running loop till the end of the stream */
    	string temp;
    	while (!ss.eof()) {
    		/* extracting word by word from stream */
    		ss >> temp;
    		/* Checking the given word is integer or not */
    		if (stringstream(temp) >> n) {
    			cout << "Number of points: "<<n<<endl;
          break;
        }
    		temp = "";
    	}
      if (n==0){
        cout<<"Something is wrong with the input file!!!Exiting..."<<endl;
        return 0;
      }
    }
    else if (line.find("end_header")!= string::npos)
      break;
  }
  if (labels.empty())
    while (infile >> x >> y >>z>>nx>>ny>>nz>>r>>g>>b>>a){
      points.push_back(x);
      points.push_back(y);
      points.push_back(z);
      normals.push_back(nx);
      normals.push_back(ny);
      normals.push_back(nz);
      features.push_back(r);
      features.push_back(g);
      features.push_back(b);
      features.push_back(a);
    }
    else{
      int l;
      while (infile >> x >> y >>z>>nx>>ny>>nz>>r>>g>>b>>a>>l){
        points.push_back(x);
        points.push_back(y);
        points.push_back(z);
        normals.push_back(nx);
        normals.push_back(ny);
        normals.push_back(nz);
        features.push_back(r);
        features.push_back(g);
        features.push_back(b);
        features.push_back(a);
        labels.push_back(l);
      }
    }
  // fill your point infomation into points, normals, features...
  bool suc=point_cloud.set_points(points, normals, features, labels);
  if (!suc){
    cout<<"Was not able to set points. Exiting..."<<endl;
    return 0;
  }
  // save the points into one binary file.
  suc=point_cloud.write_points("my_points.points");
  if (!suc){
    cout<<"Was not able to write points. Exiting..."<<endl;
    return 0;
  }
  suc=point_cloud.write_ply("my_points.ply");
  if (!suc){
    cout<<"Was not able to write ply. Exiting..."<<endl;
    return 0;
  }
  // Then the octree generator can take the saved points file to generate octree
}
