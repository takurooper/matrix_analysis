import numpy as np
import pandas as pd

def solve_coordinate_matrix(sample_df):
  dp_list = list(sample_df.columns)
  coordinate_df = pd.DataFrame(index = dp_list, columns=dp_list)
  for df_y in dp_list:
    for df_x in dp_list:
      if df_x==df_y:
        coordinate_df.loc[df_x,df_y] = "-"
      else:
        if sum(np.array(sample_df[df_x]) * np.array(sample_df[df_y])) > 0:
          coordinate_df.loc[df_x,df_y] = "○"
        elif sum(np.array(sample_df[df_x]) * np.array(sample_df[df_y])) < 0:
          coordinate_df.loc[df_x,df_y] = "●"
        else:
          coordinate_df.loc[df_x,df_y] = ""
  return coordinate_df