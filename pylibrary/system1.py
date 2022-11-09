import pandas as pd

#任意のマトリクス(ラベル多階層でもOK)を入力とし，
#ラベルをシンプル化=1階層(label1,label2,,,)にしたマトリクスを作成
def label_simplify(df):
    simple_index = ["label"+str(i) for i in range(len(df))]
    simple_columns = ["label"+str(i) for i in range(len(df.columns))]
    simple_label_df = pd.DataFrame(df.values, index=simple_index,columns=simple_columns)
    return(simple_label_df)

#実体act細直接実現QFDと実体間物理関係DSMを入力とし，実体act細間接実現QFDを出力
def indirect_effect_ent_act_minute_matrix(qfd, dsm):
    #NaNがあれば0にする
    qfd.fillna(0, inplace=True)
    dsm.fillna(0, inplace=True)
    #空(全て0)のact間マトリクスを作成
    effect_mtx = pd.DataFrame(index=qfd.index, columns=qfd.columns)
    effect_mtx.fillna(0, inplace=True)
    #(index,column)にあたるent→actには波及関係があるかどうか
    for index in range(len(effect_mtx)):
        for column in range(len(effect_mtx.columns)):
            for i in range(len(qfd.iloc[:,column])):
#※修正前
#                 if qfd.iloc[i,column] != 0 and dsm.iloc[index,i]:
                if (qfd.iloc[i,column] != 0) and (dsm.iloc[index,i] == 1):
                    #回数気にしない場合
                    effect_mtx.iloc[index,column] = 1
#                     #回数気にする場合
#                     effect_mtx.iloc[index,column] += 1
    return(effect_mtx)

#実体act細直接実現QFDと実体act細間接実現QFDの和をとり，実体act細影響関係QFDを作成
def effect_ent_act_minute_matrix_(direct_qfd, indirect_qfd):
    effect_mtx = pd.DataFrame(index=direct_qfd.index, columns=direct_qfd.columns)
    effect_mtx.fillna(0, inplace=True)
    for index in range(len(effect_mtx)):
        for column in range(len(effect_mtx.columns)):
            effect_mtx.iloc[index,column] = direct_qfd.iloc[index,column] + indirect_qfd.iloc[index,column]
    return(effect_mtx)

#入力から出力
def main(dataframe1,dataframe2):
    #二つの入力データのラベルをシンプル(一層)に
    df1 = label_simplify(dataframe1)
    df2 = label_simplify(dataframe2)
    #実体act細影響関係QFD(出力)
    effect_qfd = effect_ent_act_minute_matrix_(df1, indirect_effect_ent_act_minute_matrix(df1, df2))
    #ラベルをきちんとしたものに戻す
    labeled_effect_qfd = pd.DataFrame(effect_qfd.values, index=dataframe1.index,columns=dataframe1.columns)
    return(labeled_effect_qfd)

