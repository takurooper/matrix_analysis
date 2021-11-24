import numpy as np
import pandas as pd

def solve_tradeoff_matrix(sample_df):
  fr_list = list(sample_df.index)
  tradeoff_df = pd.DataFrame(index = fr_list, columns=fr_list)
  for df_y in fr_list:
    for df_x in fr_list:
      if df_x==df_y:
        tradeoff_df.loc[df_x,df_y] = "-"
      else:
        if sum(np.array(sample_df.loc[df_x]) * np.array(sample_df.loc[df_y])) > 0:
          tradeoff_df.loc[df_x,df_y] = "○"
        elif sum(np.array(sample_df.loc[df_x]) * np.array(sample_df.loc[df_y])) < 0:
          tradeoff_df.loc[df_x,df_y] = "●"
        else:
          tradeoff_df.loc[df_x,df_y] = ""
  return tradeoff_df