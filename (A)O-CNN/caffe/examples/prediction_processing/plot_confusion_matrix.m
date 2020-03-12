function plot_confusion_matrix(actual,pred,C,N,name)

    %create heatmap for confusion matrix
    %figure(1);
    %tbl = array2table([actual.', pred.'], 'VariableNames', {'Actual', 'Predicted'});
    %heatmap(tbl,'Predicted','Actual');

    target=zeros(C,N);
    output=zeros(C,N);
    targetIdx=sub2ind(size(target),actual+1,1:N);
    outputIdx=sub2ind(size(output),pred+1,1:N);
    target(targetIdx)=1;
    output(outputIdx)=1;
    disp(target);
    disp("---------------");
    disp(output);
    %figure(2);
    plotconfusion(target,output);
    
    fh = gcf; % access the figure handle for the confusion matrix plot
    ah = fh.Children(2); % access the corresponding axes handle
    for i = 1:9
        ah.XTickLabel{i} = i-1; % change the tick labels
       ah.YTickLabel{i} = i-1;
    end
    ah.XLabel.String = 'Actual'; % change the axes labels
    ah.YLabel.String = 'Predicted';
    xticklabels({'0-PUBLIC','1-RESIDENTIAL','2-RELIGIOUS','3-COMMERCIAL','4-MILITARY','5-STADIUM'});
    title(['Confusion Matrix ' name]);
end