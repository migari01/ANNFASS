function plot_class_accuracy(conf_ma,name)
    correct=diag(conf_ma);
    disp("Correct");
    disp(correct);
    incorrect=sum(conf_ma,2)-correct;
    disp("Incorrect");
    disp(incorrect);
    figure;
    b=bar([incorrect,correct],'stacked');
    xlabel("Class");
    ylabel("#Models");
    title(['Class accuracy ' name]);
    legend(["Incorrect","Correct"],'location','northwest');
    set(b,{'FaceColor'},{'r';'g'});
    acc=zeros(1,length(correct));
    % A loop that does num2str conversion only if value is >0
    disp("Total");
    total=sum(conf_ma,2);
    disp(total);
    disp("Accuracy");
    acc=correct*100.0./total;
    acc=num2str(acc,'%.2f');       
    acc=strcat(acc,'%');
    disp(acc);
        disp(sum(acc));
    text(1:size(acc,1),total,acc,'VerticalAlignment','bottom', 'HorizontalAlignment', 'center','FontWeight','bold','FontSize',10, 'Color','black');
    xticklabels({'0-PUBLIC','1-RESIDENTIAL','2-RELIGIOUS','3-COMMERCIAL','4-MILITARY','5-STADIUM'});
    xtickangle(45);
    grid on;
end