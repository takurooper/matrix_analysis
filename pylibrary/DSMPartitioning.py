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
def step1(df_DSM):
    new_DSM = df_DSM
    part_of_new_DSM = df_DSM
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
def step2(df_DSM):
    new_DSM = df_DSM
    part_of_new_DSM = df_DSM
    while len(independent_column_list(part_of_new_DSM)) != 0:
        new_DSM = move_to_the_bottom_DSM(new_DSM, independent_column_list(new_DSM))
        part_of_new_DSM = remove_part_of_DSM(part_of_new_DSM, independent_column_list(part_of_new_DSM))
    return [new_DSM,part_of_new_DSM]

#メイン(これを実行すればOK)
def DSM_partitioning(input_df):
    df_DSM = input_df.copy().fillna(0)
    #入力がDSMでない場合、実行しない
    if df_DSM.columns.to_list() != df_DSM.index.to_list():
        print("入力はDSMではありません")
    #入力がDSMであるがラベルに重複したものがある場合、実行しない
    elif len(df_DSM.columns.to_list()) != len(set(df_DSM.columns.to_list())):
        print("ラベルに重複しているものがあります")
    #入力がDSMでありラベルに重複したものがない場合、実行する
    else:
        #step1を実行
        step1_DSM = step1(df_DSM)[0]
        rest_part_of_step1_DSM = step1(df_DSM)[1]
        #step2を実行
        step2_DSM = step2(step1_DSM)[0]
        #step1とstep2を経ても残った要素のDSM(あとで活用するかも)
        rest_part_of_step1_and_step2_DSM = step2(rest_part_of_step1_DSM)[1]
    #return(step2_DSM,rest_part_of_step1_and_step2_DSM)
    return(step2_DSM)