% filename
file='THEA_30000_12_rot_no_batching_depth_6';
filename_list = '/media/maria/BigData1/Maria/data_split/Pratheba_split/test_dataset_w_labels_12_rot_shuffle.txt'; % the data list file with labels
filename_prob = strcat('../o-cnn/prob/',file,'_prob.dat'); % file containing probabilities of each class for each object
disp(filename_prob);
graphs=strrep(file, "_"," ");
disp(file);

% get prob
fid = fopen(filename_prob, 'r');
N = fread(fid, 1, 'int32');%number of models in test set
C = fread(fid, 1, 'int32');%number of classes
prob = fread(fid, [C, N], 'float32');
fclose(fid);

% get predicted label
[~, pred] = max(prob, [], 1);
pred=pred-1;
% read data list
fid = fopen(filename_list, 'r');
tline = fgetl(fid);
actual = zeros(1, N);
name = strings(1, N);
i = 1;
while ischar(tline)
    p = strfind(tline, ' ');
    actual(i) = str2double(tline(p+1:end));
    index=regexp(tline(1:p),'[A-Z]+[a-z]+_[a-z]+[0-9]+','end');
    name(i) =tline(1:index);
    i = i + 1;
    tline = fgetl(fid);
end
fclose(fid);

%write json file with prediction per model
s=struct('name',{},'prob',{},'actual',{},'predicted',{});
fid=fopen(strcat('../o-cnn/prob/',file,'_probabilities.json'),'w');
for i = 1 : N
    s(i).name=name(i);
    s(i).prob=prob(:,i);
    s(i).actual=actual(i);
    s(i).predicted=pred(i);  
end
j=jsonencode(s);
fwrite(fid,j,'char');
fclose(fid);

%create confusion matrix and save it
CON=confusionmat(actual,pred);
disp(CON);
writetable(array2table(CON),strcat('../o-cnn/prob/',file,'_confusion_matrix.csv'));

%plot confusion matrix and save it
plot_confusion_matrix(actual,pred,C,N,graphs);
plot_class_accuracy(CON,graphs);