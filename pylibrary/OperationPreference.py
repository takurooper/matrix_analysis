import numpy as np

#操作リスク(：無い=No_Risk,低い=Low_Risk,高い=High_Risk)の導出
def calculate_operational_risk_matrix(df_qfd, df_fn_imp):
    #リスクマトリクスの入れ物(df)を作っておく
    operational_risk_matrix = df_qfd.copy()
    #トレードオフの判定
    #各設計変数ごとに…
    for i in range(1,len(df_qfd.columns)): 
        #その設計変数が持つ影響関係のリスト
        #その設計変数にトレードオフが生じない場合
        if (all(relation >=0 for relation in df_qfd.iloc[:,i]) or all(relation <=0 for relation in df_qfd.iloc[:,i])):
            for j in range(len(df_qfd.iloc[:,i])):
                #操作リスク無し
                if df_qfd.iloc[j,i] != 0:
                    operational_risk_matrix.iloc[j,i] = "No_Risk"
        #その設計変数にトレードオフが生じる場合
        #支配的な影響特性の判定
        else :
            dominance_list = []
            for j in range(len(df_qfd.iloc[:,i])):
                #支配度算出
                dominance = abs(df_qfd.iloc[j,i])*df_fn_imp.iloc[j,1]
                dominance_list.append(dominance)
            max_dominance = max(dominance_list)
            if dominance_list.count(max_dominance) > 1:
                print("支配的な影響特性が複数あります。")
            else:
                max_dominance_index = dominance_list.index(max_dominance)
                for k in range(len(df_qfd.iloc[:,i])):
                    #自身の特性が支配的な影響特性と一致する場合、操作リスク低い
                    if df_qfd.iloc[k,i]*df_qfd.iloc[max_dominance_index,i] > 0:
                        operational_risk_matrix.iloc[k,i] = "Low_Risk"
                    #自身の特性が支配的な影響特性と一致しない場合、操作リスク高い
                    elif df_qfd.iloc[k,i]*df_qfd.iloc[max_dominance_index,i] < 0:
                        operational_risk_matrix.iloc[k,i] = "High_Risk"
    return(operational_risk_matrix)

#操作選好(=赤緑)の導出(前提条件重視)
def calculate_design_policy_matrix_a(df_qfd, df_dp_precon, operational_risk_matrix):
    #操作選好マトリクスの入れ物(df)を作っておく
    design_policy_matrix = df_qfd.copy()
    design_policy_matrix.replace(0,np.nan)
    for i in range(1,len(df_qfd.columns)):
        #前提条件ない場合
        if df_dp_precon.iloc[i-1,1] == "Not Preconditioned":      
            for j in range(len(df_qfd.iloc[:,i])):
                if abs(df_qfd.iloc[j,i]) == 3:
                    if operational_risk_matrix.iloc[j,i] == "No_Risk":
                        design_policy_matrix.iloc[j,i] = "Preferred"
                    elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                        design_policy_matrix.iloc[j,i] = "Preferred"
                    elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                        design_policy_matrix.iloc[j,i] = "Not Preferred"
                elif abs(df_qfd.iloc[j,i]) == 1:
                    if operational_risk_matrix.iloc[j,i] == "No_Risk":
                        design_policy_matrix.iloc[j,i] = "Controversial"
                    elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                        design_policy_matrix.iloc[j,i] = "Controversial"
                    elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                        design_policy_matrix.iloc[j,i] = "Not Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        #前提条件ある場合
        else:
            for j in range(len(df_qfd.iloc[:,i])):
                if df_qfd.iloc[j,i] != 0:
                    design_policy_matrix.iloc[j,i] = "Not Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan              
    return(design_policy_matrix)

#操作選好(=赤緑)の導出(前提条件重視)
def calculate_design_policy_matrix_b(df_qfd, df_dp_precon, operational_risk_matrix):
    #操作選好マトリクスの入れ物(df)を作っておく
    design_policy_matrix = df_qfd.copy()
    design_policy_matrix.replace(0,np.nan)
    for i in range(1,len(df_qfd.columns)):
        #前提条件ないもある場合も     
        for j in range(len(df_qfd.iloc[:,i])):
            if abs(df_qfd.iloc[j,i]) == 3:
                if operational_risk_matrix.iloc[j,i] == "No_Risk":
                    design_policy_matrix.iloc[j,i] = "Preferred"
                elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                    design_policy_matrix.iloc[j,i] = "Preferred"
                elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                    design_policy_matrix.iloc[j,i] = "Not Preferred"
            elif abs(df_qfd.iloc[j,i]) == 1:
                if operational_risk_matrix.iloc[j,i] == "No_Risk":
                    design_policy_matrix.iloc[j,i] = "Controversial"
                elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                    design_policy_matrix.iloc[j,i] = "Controversial"
                elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                    design_policy_matrix.iloc[j,i] = "Not Preferred"
            else:
                design_policy_matrix.iloc[j,i] = np.nan         
    return(design_policy_matrix)

#順位尺度の導出
def calculate_rank_scale_matrix(df_qfd, df_dp_precon, operational_risk_matrix):
    #順位尺度マトリクスの導出
    #順位尺度マトリクスの入れ物(df)を作っておく
    rank_scale_matrix = df_qfd.copy()
    rank_scale_matrix.replace(0,np.nan)
    for i in range(1,len(df_qfd.columns)):
        #前提条件ない場合
        if df_dp_precon.iloc[i-1,1] == "Not Preconditioned":      
            for j in range(len(df_qfd.iloc[:,i])):
                if abs(df_qfd.iloc[j,i]) == 3:
                    if operational_risk_matrix.iloc[j,i] == "No_Risk":
                        rank_scale_matrix.iloc[j,i] = 2
                    elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                        rank_scale_matrix.iloc[j,i] = 2
                    elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                        rank_scale_matrix.iloc[j,i] = 0
                elif abs(df_qfd.iloc[j,i]) == 1:
                    if operational_risk_matrix.iloc[j,i] == "No_Risk":
                        rank_scale_matrix.iloc[j,i] = 1
                    elif operational_risk_matrix.iloc[j,i] == "Low_Risk":
                        rank_scale_matrix.iloc[j,i] = 1
                    elif operational_risk_matrix.iloc[j,i] == "High_Risk":
                        rank_scale_matrix.iloc[j,i] = 0
                else:
                    rank_scale_matrix.iloc[j,i] = np.nan
        #前提条件ある場合
        else:
            for j in range(len(df_qfd.iloc[:,i])):
                if df_qfd.iloc[j,i] != 0:
                    rank_scale_matrix.iloc[j,i] = 0
                else:
                    rank_scale_matrix.iloc[j,i] = np.nan              
    return(rank_scale_matrix)

#列の最大値と最小値を返す
def min_max(raw):
    raw_ = [i for i in raw if i == i and type(i) == float]
    return  max(raw_), min(raw_)

#操作選好(=赤緑)の導出(機能尺度毎に引き直した操作選好導出)
def calculate_design_policy_matrix_c(df_qfd, rank_scale_matrix):
    #赤緑マトリクスの導出
    #赤緑マトリクスの入れ物(df)を作っておく
    design_policy_matrix = df_qfd.copy()
    for j in range(len(df_qfd)):
        if rank_scale_matrix.apply(min_max, axis=1)[j] == (2,0):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 2:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                elif rank_scale_matrix.iloc[j,i] == 1:
                    design_policy_matrix.iloc[j,i] = "Controversial"
                elif rank_scale_matrix.iloc[j,i] == 0:
                    design_policy_matrix.iloc[j,i] = "Not Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        elif rank_scale_matrix.apply(min_max, axis=1)[j] == (2,1):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 2:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                elif rank_scale_matrix.iloc[j,i] == 1:
                    design_policy_matrix.iloc[j,i] = "Controversial"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        elif rank_scale_matrix.apply(min_max, axis=1)[j] == (2,2):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 2:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        elif rank_scale_matrix.apply(min_max, axis=1)[j] == (1,0):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 1:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                elif rank_scale_matrix.iloc[j,i] == 0:
                    design_policy_matrix.iloc[j,i] = "Not Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        elif rank_scale_matrix.apply(min_max, axis=1)[j] == (1,1):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 1:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        elif rank_scale_matrix.apply(min_max, axis=1)[j] == (0,0):
            for i in range(1,len(df_qfd.columns)):
                if rank_scale_matrix.iloc[j,i] == 0:
                    design_policy_matrix.iloc[j,i] = "Preferred"
                else:
                    design_policy_matrix.iloc[j,i] = np.nan
        else:
            for i in range(1,len(df_qfd.columns)):
                design_policy_matrix.iloc[j,i] = np.nan
    return(design_policy_matrix)

#メイン関数
def main(df_qfd, df_fn_imp, df_dp_precon, calc_type):
    df_qfd = df_qfd.fillna(0)
    operational_risk_matrix = calculate_operational_risk_matrix(df_qfd, df_fn_imp)
    if calc_type=="a=前提条件重視":
        design_policy_matrix = calculate_design_policy_matrix_a(df_qfd, df_dp_precon, operational_risk_matrix)
    elif calc_type=="b=前提条件軽視":
        design_policy_matrix = calculate_design_policy_matrix_b(df_qfd, df_dp_precon, operational_risk_matrix)
    elif calc_type=="c=機能尺度ごとに引き直し":
        rank_scale_matrix = calculate_rank_scale_matrix(df_qfd, df_dp_precon, operational_risk_matrix)
        design_policy_matrix = calculate_design_policy_matrix_c(df_qfd, rank_scale_matrix)
    return design_policy_matrix.fillna("null")