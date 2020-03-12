#include <iostream>
#include <string>
#include <time.h>
#include <boost/filesystem.hpp>
#include "virtual_scanner/virtual_scanner.h"

using namespace std;

void get_all_filenames(vector<string>& _all_filenames, string _filename, bool _header);

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cout << "Usage: VirtualScanner.exe <file name/folder name> "
    "[header (true/exclude)][view_num] [flags] [normalize]" << endl;
    return 0;
  }
  string filename(argv[1]);
  bool header=false;//input is already converted to point clouds need to convert
  //them in the format octree expects [header, points, normals,features,labels]

  int view_num = 6; // scanning view number
  bool flag = false; // output normal flipping flag
  bool normalize = false; // normalize input meshes
  if(argc >= 3&&(argv[2]==std::string("true")))
  header=true;
  else{
    if (argc >= 3) view_num = atoi(argv[2]);
    if (argc >= 4) flag = atoi(argv[3]);
    if (argc >= 5) normalize = atoi(argv[4]);
  }
  vector<string> all_files;
  get_all_filenames(all_files, filename,header);

  #pragma omp parallel for
  for (int i = 0; i < all_files.size(); i++) {
    clock_t t1 = clock();
    VirtualScanner scanner;
    if (header){
      scanner.get_point_cloud().createHeader(all_files[i]);
    }
    /*else{
      cout<<"error!!!!"<<endl;
      exit(0);
    }*/
    else{
      scanner.scanning(all_files[i], view_num, flag, normalize);
      string out_path  = all_files[i].substr(0, all_files[i].rfind('.'));
      scanner.save_binary(out_path+ ".points");
      scanner.save_ply(out_path+ ".ply");
      scanner.save_txt(out_path+".txt");
    }
    clock_t t2 = clock();

    string messg = all_files[i].substr(all_files[i].rfind('\\') + 1) +
    " done! Time: " + to_string(t2 - t1) + "\n";
    #pragma omp critical
    cout << messg;
  }

  return 0;
}

bool is_convertable_file(string extension, bool header) {
  if (header)
    return extension.compare(".pts") == 0;
  else
    return extension.compare(".off") == 0 || extension.compare(".obj") == 0;
}

void get_all_filenames(vector<string>& _all_filenames, string _filename,bool _header) {
  using namespace boost::filesystem;
  if (is_regular_file(_filename)) {
    if (_header){
      if(_filename.find(".pts") != std::string::npos){
        _all_filenames.push_back(_filename);}
        else{
          cout<<"Incompatible file extension. Exiting..."<<endl;
          exit(-1);
        }
      }
      else
      _all_filenames.push_back(_filename);
    } else if (is_directory(_filename)) {
      for (auto& file : recursive_directory_iterator(_filename)) {
        auto extension = file.path().extension().string();
        std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);
        if (is_regular_file(file) && is_convertable_file(extension, _header)) {
          _all_filenames.push_back(file.path().string());
        }
      }
    }
  }
