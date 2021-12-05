import pandas as pd
import re

def Change_propagation_df_DSM(df_qfd):
    list0 = []
    for i in range(len(df_qfd)):
        listi = []
        list1 = df_qfd.iloc[i,1:len(df_qfd.columns)].to_list()
        for j in range(len(df_qfd)):
            list2 = df_qfd.iloc[j,1:len(df_qfd.columns)].to_list()
            #感度の比(j/i)、の総和
            stvij = 0
            for k in range(len(list1)):
                if (("↑" in str(list1[k])) and ("↓" in str(list2[k]))) or (("↓" in str(list1[k])) and ("↑" in str(list2[k]))):
                    number_of_tradeoff = +1
                    a = int(re.sub(r"\D", "", list2[k])) / int(re.sub(r"\D", "", list1[k]))
                    stvij += a
            #機能尺度i→機能尺度jの期待変更伝播感度の値
            psij = stvij/(df_qfd.count(axis=1)[i]-1)#分母は機能尺度iと影響関係を持つ設計変数の数
            listi.append(psij)
        list0.append(listi)
    label1 = df_qfd["機能尺度/設計変数"].to_list()
    change_propagation_dsm = pd.DataFrame(data=list0, index=label1, columns=label1)
    return(change_propagation_dsm)