import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

#入力1
#全体直接影響マトリクスを入力
#空行ありで入れないとだめ

total_direct_dataframe = pd.read_excel("入力_詳細モデル_全体直接影響マトリクス.xlsx",header=[0,1,2,3,4], index_col=[0,1,2,3,4], engine='openpyxl')

#入力2
#属性変化分df
#(ラベル多階層，属性ラベルが行ラベル(縦長))
change_atr_dataframe = pd.read_excel("入力_施策_属性変化分.xlsx",header=[0],index_col=[0,1,2,3,4], engine='openpyxl')

#行列の正規化
#入力の形
# dataframe = pd.DataFrame([[0,3,1,0],[0,0,2,3],[0,0,0,2],[0,0,0,0]],
#                   columns=['act1', 'act2', 'dp1', 'dp2'],
#                   index=['act1', 'act2', 'dp1', 'dp2'])
def normalized_matrix(df):
    #Nanは全て0で埋める
    df.fillna(0, inplace=True)
    new_df = df.abs()
    return(df/max(new_df.sum(axis = 1)))



#直接影響行列を入力とし，総合影響行列を出力
#DEMATEL法(逆行列を用いる)
#入力の形
# # dataframe = pd.DataFrame([[0,3,1,0],[0,0,2,3],[0,0,0,2],[0,0,0,0]],
#                   columns=['act1', 'act2', 'dp1', 'dp2'],
#                   index=['act1', 'act2', 'dp1', 'dp2'])
def total_effect_matrix(df):
    #NaNは全て0で埋める
    df.fillna(0, inplace=True)
    #直接影響行列を正規化し，正規化直接影響行列を作成
    normalized_df = normalized_matrix(df)
    #単位行列
    identity_df = pd.DataFrame(np.eye(len(df)),
                  columns=df.columns,
                  index=df.index)
    #(単位行列-正規化直接影響行列)の逆行列
    identity_df_minus_normalized_df_inv = pd.DataFrame(np.linalg.pinv(identity_df-normalized_df.values), df.columns, df.index)
    #総合影響行列=正規化直接影響行列×((単位行列-正規化直接影響行列)の逆行列)
    total_effect_df = normalized_df.dot(identity_df_minus_normalized_df_inv)
#     #-0.0をなくすため，±小数点7桁以下のものは全て0とする
#     round_total_effect_df = total_effect_df.applymap(lambda x: 0 if -1*(10**-7)<x<1*(10**-7) else x)
    return(total_effect_df)


#任意のマトリクス(ラベル多階層でもOK)を入力とし，
#ラベルをシンプル化=1階層(label1,label2,,,)にしたマトリクスを作成
def label_simplify(df):
    simple_index = ["label"+str(i) for i in range(len(df))]
    simple_columns = ["label"+str(i) for i in range(len(df.columns))]
    simple_label_df = pd.DataFrame(df.values, index=simple_index,columns=simple_columns)
    return(simple_label_df)


#全体直接影響行列を入力とし，属性&act層のみdematelにかけ，全体総合影響行列を出力
def all_total_effect_matrix(df):
    #Nanは全て0で埋める
    df.fillna(0, inplace=True)
    #ラベルをシンプル化(label1,label2,,,)した全体直接影響行列を作成
    all_dsm = label_simplify(df)
    #属性act直接影響DSM(ラベルシンプルver)を抜き出す
    atr_act_num = len(df.loc[["activity層","実体層"],["activity層","実体層"]])
    atr_act_dsm = all_dsm.iloc[(len(all_dsm)-atr_act_num):,(len(all_dsm)-atr_act_num):]
    #属性act直接影響DSM(ラベルシンプルver)から全体総合影響行列(ラベルシンプルver)を作成
    copy_all_dsm = all_dsm.copy()
    copy_all_dsm.iloc[(len(all_dsm)-atr_act_num):,(len(all_dsm)-atr_act_num):]=total_effect_matrix(atr_act_dsm)
    #全体総合影響行列(ラベルちゃんとしてるver)を作成
    all_total_effect_mtx = pd.DataFrame(copy_all_dsm.values, index=df.index,columns=df.columns)
    #0をNaNに置換したうえで返す
    return(all_total_effect_mtx.replace(0, np.nan))


#下位要素→上位要素DSM(一層ラベル)と，下位要素の一行df(列ラベルは一層ラベル)を入力とし，
#上位要素の変化分をpositive変化分，negative変化分，total変化分にわけて出力
def calculate_changes(dsm,input_changes):
    #Nanは全て0で埋める
    dsm.fillna(0, inplace=True)
    output_changes = pd.DataFrame(columns=dsm.columns,index=['positive変化分','negative変化分','total変化分'])
    for column in range(len(dsm.columns)):
        #そのcolumn(上位要素)が受ける好影響と悪影響
        positive=0
        negative=0
        for index in range(len(dsm.index)):
            #その([index,column])影響が正の場合
            if input_changes.iloc[0,index]*dsm.iloc[index,column]>=0:
                positive += input_changes.iloc[0,index]*dsm.iloc[index,column]
            #その([index,column])影響が負の場合
            else:
                negative += input_changes.iloc[0,index]*dsm.iloc[index,column]
        output_changes.iloc[0,column] = positive
        output_changes.iloc[1,column] = negative
        output_changes.iloc[2,column] = positive + negative
    return(output_changes)


#実行プログラム
#全体直接影響行列(ラベル多階層)と属性変化行列(ラベル多階層，属性ラベルが行ラベル(縦長))を入力とし，
#属性変化によるact変化分df(ラベル多階層)を出力
def main(df, change_atr_df):
    #Nanは全て0で埋める
    df.fillna(0, inplace=True)
    change_atr_df.fillna(0, inplace=True)
    #全体直接影響行列から全体総合影響行列を作成
    total_mtx = all_total_effect_matrix(df)
    #Nanは全て0で埋める
    total_mtx.fillna(0, inplace=True)
    #ラベルをシンプル化(label1,label2,,,)した属性変化行列を作成(※転置した上で)
    change_atr = label_simplify(change_atr_df.T)
    #ラベルをシンプル化(label1,label2,,,)した属性→act直接影響DSMを作成
    atr_to_act_dsm = label_simplify(total_mtx.loc[["実体層"],["activity層"]])
    #act変化行列(ラベルシンプルver)を導出
    effect_to_act_df = calculate_changes(atr_to_act_dsm,change_atr)
    #ラベルをシンプル化(label1,label2,,,)したact→機能DSMを作成
    act_to_func_dsm = label_simplify(total_mtx.loc[["activity層"],["機能層"]])
    #機能変化行列(ラベルシンプルver)を導出
    effect_to_func_df = calculate_changes(act_to_func_dsm,effect_to_act_df.iloc[2:,:])
    #ラベルをシンプル化(label1,label2,,,)した機能→価値DSMを作成
    func_to_val_dsm = label_simplify(total_mtx.loc[["機能層"],["価値(人)層"]])
    #機能変化行列(ラベルシンプルver)を導出
    effect_to_val_df = calculate_changes(func_to_val_dsm,effect_to_func_df.iloc[2:,:])
    #正式ラベル(多階層)になおす
    #act変化分
    effect_to_act_mtx = pd.DataFrame(effect_to_act_df.values, index=['positive変化分','negative変化分','total変化分'],columns=df.loc[["activity層"],["activity層"]].columns)
    #機能変化分
    effect_to_func_mtx = pd.DataFrame(effect_to_func_df.values, index=['positive変化分','negative変化分','total変化分'],columns=df.loc[["機能層"],["機能層"]].columns)
    #価値変化分
    effect_to_val_mtx = pd.DataFrame(effect_to_val_df.values, index=['positive変化分','negative変化分','total変化分'],columns=df.loc[["価値(人)層"],["価値(人)層"]].columns)
    return(effect_to_act_mtx,effect_to_func_mtx,effect_to_val_mtx)