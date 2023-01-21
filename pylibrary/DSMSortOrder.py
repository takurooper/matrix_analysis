def DSM_sort_order(priority_df):
    priority_weight = priority_df.sum()
    priority_order =  priority_weight.sort_values(ascending=True).index
    priority_df = priority_df[priority_order].reindex(priority_order)
    priority_weight = priority_df.T.sum()
    priority_order =  priority_weight.sort_values(ascending=False).index
    priority_df = priority_df[priority_order].reindex(priority_order)
    priority_order = '→'.join(priority_order)
    return(priority_df, priority_order)
