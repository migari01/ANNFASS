#ifndef _OCTREE_POINTS_
#define _OCTREE_POINTS_

#include <vector>
#include <string>
#include <iostream>
#include <fstream>

using std::vector;
using std::string;
using std::cout;
using std::endl;

class PtsInfo {
 public:
  enum PropType { kPoint = 1, kNormal = 2, kFeature = 4, kLabel = 8 };
  static const int kPTypeNum = 4;
  static const char kMagicStr[16];

 public:
  PtsInfo() { reset(); }
  void reset();
  bool check_format(string& msg) const;
  bool has_property(PropType ptype) const {
    return (content_flags_ & ptype) != 0;
  }

  int pt_num() const { return pt_num_; }
  int channel(PropType ptype) const;
  int ptr_dis(PropType ptype) const;
  int sizeof_points() const { return ptr_dis_[kPTypeNum]; }

  void set_pt_num(int num) { pt_num_ = num; }
  void set_channel(PropType ptype, const int ch);
  void set_ptr_dis();

void see_info(){
  cout<<"MAGIC STRING"<<endl;
  cout<<magic_str_<<","<<endl;
  cout<<"POINT NUM"<<endl;
  cout<<pt_num_<<endl;
  cout<<"CONTENT FLAG"<<endl;
  cout<<content_flags_<<endl;
  cout<<"CHANNELS"<<endl;
  for (int i=0;i<8;i++)
    cout<<channels_[i]<<endl;
  cout<<"PTR DIS"<<endl;
  for (int i=0;i<8;i++)
    cout<<ptr_dis_[i]<<endl;
}
void write_info(const string& filename)const{
  std::ofstream outfile(filename+"w/out_header_.txt", std::ios::binary);
  if (!outfile) {cout<<"Error opening file. Exiting..."<<endl; exit(-1);}
  outfile<<magic_str_<<endl;
  outfile<<pt_num_<<endl;
  outfile<<content_flags_<<endl;
  for (int i=0;i<8;i++)
    outfile<<channels_[i]<<",";
  outfile<<endl;
  for (int i=0;i<8;i++)
    outfile<<ptr_dis_[i]<<",";
  outfile<<endl;
  outfile.close();
}

 protected:
  int property_index(PropType ptype) const;

 protected:
  char magic_str_[16];
  int pt_num_;
  int content_flags_;
  int channels_[8];
  int ptr_dis_[8];

};


class Points {
 public:
  Points() : info_(nullptr), buffer_() {}
  bool is_empty() const { return info_ == nullptr || info_->pt_num() == 0; }
  bool createHeader(const string& filename);

  // the pts must not be empty, the labels may be empty,
  // the normals & features must not be empty at the same time.
  bool set_points(const vector<float>& pts, const vector<float>& normals,
      const vector<float>& features = vector<float>(),
      const vector<float>& labels = vector<float>());
  void set_points(vector<char>& data); // swap data and buffer_

  bool read_points(const string& filename);
  bool write_points(const string& filename) const;
  bool write_ply(const string& filename, bool f, bool l) const;
  bool write_txt(const string & filename, bool f, bool l) const;

  const PtsInfo& info() const { return *info_; }
  const float* ptr(PtsInfo::PropType ptype) const;
  float* mutable_ptr(PtsInfo::PropType ptype);

  void centralize(const float* center);
  void displace(const float dis);
  void rotate(const float angle, const float* axis);

 protected:
  PtsInfo* info_;
  vector<char> buffer_;
};

#endif // _OCTREE_POINTS_
