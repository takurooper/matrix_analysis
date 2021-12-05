import numpy as np
import pandas as pd

def solve_tradeoff_matrix(df):
    fngp = (df.iloc[:,1:].T*list(df.iloc[:,0])).T/81
    gp_list = fngp.columns
    list_2d = [[0] * len(fngp.columns) for i in range(len(fngp.columns))]
    for index in range(len(list_2d)):
        for row in range(len(list_2d)):
            if index==row:
                list_2d[index][row]=1
            elif index > row:
                #index=1 gp2, row=0 gp1
                dotproduct = np.dot(list(fngp.iloc[:,index]),list(fngp.iloc[:,row]))
                list_2d[index][row] = dotproduct
                list_2d[row][index] = dotproduct
    max_num_in_list = max(list(map(lambda x: max(x), list_2d)))
    gpgp = pd.DataFrame(list_2d,index=gp_list,columns=gp_list)
    return gpgp/max_num_in_list