# **Identify loops by path Searching**
# Compare *Gebala, D. A. and Eppinger, S. D., Methods for analyzing design procedures, in Proceedings of 3rd International ASME Conference on Design Theory and Methodology, 1991, pp. 227-233*
# https://dsmweb.org/sequencing-a-dsm/#path-searching

import itertools

#DataFrameのテーブル作り(本来はここが入力値に当たるところ)
#※数字のみで構成されていること
#例：
#data_list = [[1,1,0,0,0,0],[1,1,1,0,1,1],[0,0,1,0,0,0],[0,0,0,1,0,1],[0,0,0,0,1,0],[1,0,1,0,1,0]]
#label_list = ["A","B","C","D","E","F"]
#df_DSM = pd.DataFrame(data=data_list, index=label_list, columns=label_list)​

#他の要素からの入力がなくて決定される(行が対角成分以外空白)要素らを、リストで返す
def independent_row_list(df_DSM):
    independent_row_list = []
    for i in range(len(df_DSM)):
        check_list = [0] * len(df_DSM.iloc[i])
        check_list[i] = df_DSM.iloc[i,i]
        #行の対角成分以外が空白な場合、リターンするリストに追加
        if df_DSM.iloc[i].to_list() == check_list:
            independent_row_list.append(df_DSM.columns[i])
    return independent_row_list

#指定した要素ら(リストの形)を指定したDSMの上端に移動させて、df(DSM)で返す
def move_to_the_top_DSM(df_DSM, move_label_list):
    label_sequence_list = df_DSM.columns.to_list()
    for i in range(len(df_DSM.columns.to_list())):
        if df_DSM.columns.to_list()[i] in move_label_list:
            label_sequence_list.remove(df_DSM.columns.to_list()[i])
    new_label_sequence_list = move_label_list + label_sequence_list
    new_df_DSM = df_DSM.reindex(index=new_label_sequence_list, columns=new_label_sequence_list)
    return(new_df_DSM)

#指定した要素ら(リストの形)を指定したDSMから削除した部分的DSMを返す
def remove_part_of_DSM(df_DSM, remove_label_list):
    new_label_list = df_DSM.columns.to_list()
    for i in range(len(df_DSM.columns.to_list())):
        if df_DSM.columns.to_list()[i] in remove_label_list:
            new_label_list.remove(df_DSM.columns.to_list()[i])
    new_part_of_DSM = df_DSM.reindex(index=new_label_list, columns=new_label_list)
    return(new_part_of_DSM)

#step1:他の要素からの入力がなくて決定される(行が対角成分以外空白)要素らを上端に移動させて、その要素らを削除したDSMで同じことを繰り返し、最終的に並び替え終わったDSMを返す。
# 2.    Task F does not depend on information from any other tasks as indicated by an empty column. Schedule task F first in the matrix and remove it from further consideration.
def step1(df_DSM):
    new_DSM = df_DSM.copy()
    part_of_new_DSM = df_DSM.copy()
    while len(independent_row_list(part_of_new_DSM)) != 0:
        new_DSM = move_to_the_top_DSM(new_DSM, independent_row_list(new_DSM))
        part_of_new_DSM = remove_part_of_DSM(part_of_new_DSM, independent_row_list(part_of_new_DSM))
    return [new_DSM,part_of_new_DSM]

#他の要素に情報を伝達しない(列が対角成分以外空白)要素らを、リストで返す
def independent_column_list(df_DSM):
    independent_column_list = []
    for i in range(len(df_DSM)):
        check_list = [0] * len(df_DSM.iloc[:,i])
        check_list[i] = df_DSM.iloc[i,i]
        #列の対角成分以外が空白な場合、リターンするリストに追加
        if df_DSM.iloc[:,i].to_list() == check_list:
            independent_column_list.append(df_DSM.columns[i])
    return independent_column_list

#指定した要素ら(リストの形)を指定したDSMの下端に移動させて、df(DSM)で返す
def move_to_the_bottom_DSM(df_DSM, move_label_list):
    label_sequence_list = df_DSM.columns.to_list()
    for i in range(len(df_DSM.columns.to_list())):
        if df_DSM.columns.to_list()[i] in move_label_list:
            label_sequence_list.remove(df_DSM.columns.to_list()[i])
    new_label_sequence_list = label_sequence_list + move_label_list
    new_df_DSM = df_DSM.reindex(index=new_label_sequence_list, columns=new_label_sequence_list)
    return(new_df_DSM)

#step2:他の要素に情報を伝達しない(列が対角成分以外空白)要素らを下端に移動させて、その要素らを削除したDSMで同じことを繰り返し、最終的に並び替え終わったDSMを返す。
# 3.    Task E does not provide  information to any tasks in the matrix as indicated by an empty row. Schedule task E last in the matrix and remove it from further consideration.
def step2(df_DSM):
    new_DSM = df_DSM.copy()
    part_of_new_DSM = df_DSM.copy()
    while len(independent_column_list(part_of_new_DSM)) != 0:
        new_DSM = move_to_the_bottom_DSM(new_DSM, independent_column_list(new_DSM))
        part_of_new_DSM = remove_part_of_DSM(part_of_new_DSM, independent_column_list(part_of_new_DSM))
    return [new_DSM,part_of_new_DSM]

# def searchEffectLoopInMatrix(rest_part_df, loop_num):
#     loop_candidates = []
#     for index in list(rest_part_df.index):
#         for col in list(rest_part_df.columns):
#             if rest_part_df.loc[index,col] != 0:
#                 start_node = index
#                 loop_candidates.push[start_node]
#                 loop_candidate = col
#                 if rest_part_df.loc[loop_candidate, start_node] != 0:
#                     loop_param.push([loop_candidate, start_node])
#     return loop_param

# def findLoopByLength(loop_length, rest_part_df):
#     # loop_length数のつながりだけ探索する
#     # loopのクラスタリングは小さなまとまり（変数が少ない）の方がいい
#     loop_params = []
#     for loop_num in range(loop_length):
#         loop_param = searchEffectLoopInMatrix(rest_part_df, loop_num)
#         loop_params.push(loop_param)
#     loop_length += 1
#     return loop_length, loop_params

# def findLoopByLength(loop_length, rest_part_df):
    

# ループを検索してクラスタにまとめる
# 4.    Now, no tasks have empty rows or columns. A loop exists and can be traced starting with any of the remaining tasks. In this case, we select task A (arbitrary) and trace its dependence on task C. Task C is simultaneously dependent upon information from task A. Since task A and task C are in a loop, collapse one into the other and represent them in a single, composite task (i.e. task CA).
def findloop(df_DSM, rest_part_df_original):
    rest_part_df = rest_part_df_original.copy()
    clusters = []
    loop_length = 2
    while(1):
        if loop_length <= len(list(rest_part_df.columns)):
            loop_length, loop_params = findLoopByLength(loop_length, rest_part_df)
            original_cols = rest_part_df.columns.to_list()
            col_list = [col for col in original_cols if col not in loop_params]
            clusters.push(col_list)
            rest_part_df = rest_part_df.loc[col_list, col_list]
        elif loop_length > len(rest_part_df.columns):
            break
    return clusters

# クラスタがindependent(step1)であるか、independent column(step2)であるかを確認する
def sequence_clusters(step2_DSM, rest_part_df):
    clusters = findloop(step2_DSM, rest_part_df)


# Partitioning Orderを反転させる（駒野さんと宗教の違い）
def sort_DSM_ascending(df):
    new_df = df[df.columns[::-1]]
    new_df = new_df.iloc[::-1]
    new_df.index = new_df.columns.to_list()
    return new_df

#メイン(これを実行すればOK)
def DSM_sequencing(input_df):
    df_DSM = input_df.copy().fillna(0)
    #入力がDSMでない場合、実行しない
    if df_DSM.columns.to_list() != df_DSM.index.to_list():
        print("入力はDSMではありません")
    #入力がDSMであるがラベルに重複したものがある場合、実行しない
    elif len(df_DSM.columns.to_list()) != len(set(df_DSM.columns.to_list())):
        print("ラベルに重複しているものがあります")
    #入力がDSMでありラベルに重複したものがない場合、実行する
    else:
        step1_DSM = step1(df_DSM)[0]
        print('step1_DSM.columns')
        rest_part_of_step1_DSM = step1(df_DSM)[1]
        step2_DSM = step2(step1_DSM)[0]
        print('step2_DSM.columns')
        print(step2_DSM.columns)
        #step1とstep2を経ても残った要素のDSM(あとで活用するかも)
        rest_part_df = step2(rest_part_of_step1_DSM)[1]
        df_dsm, rest_part_df = sequence_clusters(step2_DSM, rest_part_df)
        
    #return(step2_DSM,rest_part_of_step1_and_step2_DSM)
    return(sort_DSM_ascending(df_dsm))
