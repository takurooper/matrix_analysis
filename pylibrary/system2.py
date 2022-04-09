import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

#入力
dataframe = pd.read_excel("システム2と3入力データ.xlsx",header=[0,1,2], index_col=[0,1,2], engine='openpyxl')

#任意のマトリクス(ラベル多階層でもOK)を入力とし，
#ラベルをシンプル化=1階層(label1,label2,,,)にしたマトリクスを作成
def label_simplify(df):
    simple_index = ["label"+str(i) for i in range(len(df))]
    simple_columns = ["label"+str(i) for i in range(len(df.columns))]
    simple_label_df = pd.DataFrame(df.values, index=simple_index,columns=simple_columns)
    return(simple_label_df)


#「実体actQFD」を入力(影響関係無し=NaNor0、数字はなんでも良い)とし
#(行ラベルに実体(設計変数)，列ラベルにact(機能尺度))
#「act間直接伝播感度行列」を出力
def change_propagation_df_dsm(df_qfd):
    #コピーし転置
    new_df_qfd = df_qfd.T.copy()
    ##入力QFDが(影響関係無し=NaN)であっても使えるようにするため、NaNの部分を0にする
    new_df_qfd.fillna(0, inplace=True)
    list0 = []
    #影響元となるfn
    for i in range(len(new_df_qfd)):
        listi = []
        #影響先となるfn
        for j in range(len(new_df_qfd)):
            #対角成分(fnDSMの)ではないものに対して
            if i != j:
                #感度の比(j/i)、の総和
                stvij = 0
                #各dpについて
                for k in range(len(new_df_qfd.columns)):
                    if new_df_qfd.iloc[j,k]*new_df_qfd.iloc[i,k]>0:
                        a = new_df_qfd.iloc[j,k] / new_df_qfd.iloc[i,k]
                        stvij += a
                #機能尺度i→機能尺度jの期待変更伝播感度の値
                if len(new_df_qfd.columns) - new_df_qfd.iloc[i,:].to_list().count(0) != 0:
                    #分母は機能尺度iと影響関係を持つ設計変数の数
                    psij = stvij/(len(new_df_qfd.columns) - new_df_qfd.iloc[i,:].to_list().count(0))
#                     #分母で割らずに出すパターン
#                     psij = stvij
                #分母が0になる(そのfnの行の全ての要素が0)場合
                else:
                    psij = 0
                listi.append(psij)
            #対角成分に対して
            else:
                listi.append(0)
        list0.append(listi)
    change_propagation_dsm = pd.DataFrame(data=list0, index=new_df_qfd.index, columns=new_df_qfd.index)
    return(change_propagation_dsm)



#各act重要度を入力として，act間伝播重要度マトリクスを出力
#入力の形
# dataframe = pd.DataFrame([[0.2,0.3,0.1,0.4]],
#                   columns=['act1', 'act2', 'act3', 'act4'],
#                   index=['重要度'])
def propagation_impact_matrix(df):
    #Nanは全て0で埋める
    df.fillna(0, inplace=True)
    #空(全てNaN)のact間マトリクスを作成
    propagation_impact_mtx = pd.DataFrame(index=df.columns, columns=df.columns)
    #空(全てNaN)のact間マトリクスの各マス(i行目，j列目)に，act(i)の重要度×act(j)の重要度を入れていく
    for i in range(len(propagation_impact_mtx)):
        for j in range(len(propagation_impact_mtx)):
            #i行目，j列目
            #重要度の積
            propagation_impact_mtx.iloc[i,j] = df.iloc[0][i]*df.iloc[0][j]
#             #重要度の積のルートver
#             propagation_impact_mtx.iloc[i,j] = (df.loc["重要度"][i]*df.loc["重要度"][j])**(1/2)
    #エクセルで出力
    #propagation_impact_mtx.to_excel("act間伝播重要度マトリクス.xlsx", encoding="shift_jis")
    return(propagation_impact_mtx)


#実行プログラム
#重要度つきの実体actQFDを入力として、act間副次関係構造マトリクスを出力
def main(df):
    #QFDと重要度抜き出し
    qfd = df.iloc[1:,:]
    imp = df.iloc[:1,:]
    #ラベルをシンプルに(一階層に)
    df_qfd = label_simplify(qfd)
    importance_df = label_simplify(imp)
    #act間副次関係構造マトリクスを作成
    synergy_structure_mtx = change_propagation_df_dsm(df_qfd)*propagation_impact_matrix(importance_df)
    #ラベルを戻す(多階層)
    labeled_synergy_structure_mtx = pd.DataFrame(synergy_structure_mtx.values, index=dataframe.columns,columns=dataframe.columns)
    #エクセルで出力
    #synergy_structure_mtx.to_excel("act間相乗構造マトリクス.xlsx", encoding="shift_jis")
    return(labeled_synergy_structure_mtx)



# #一連の途中段階の計算結果をエクセル出力する
# def output_to_excel(df_qfd, importance_df):
#     #「act間直接伝播感度行列」をエクセルで出力
#     change_propagation_df_dsm(df_qfd).to_excel("<2物理関係変更ver>output_act間直接伝播感度行列.xlsx", encoding="shift_jis")
#     #「act間伝播重要度行列」をエクセルで出力
#     propagation_impact_matrix(importance_df).to_excel("<2物理関係変更ver>output_act間伝播重要度行列.xlsx", encoding="shift_jis")
#     #「act間相乗構造行列」をエクセルで出力
#     synergy_structure_matrix(df_qfd, importance_df).to_excel("<2物理関係変更ver>final_output_act間相乗構造マトリクス.xlsx", encoding="shift_jis")