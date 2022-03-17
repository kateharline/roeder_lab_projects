import pandas as pd

lineage_df = pd.read_csv('/Users/kateharline/workspace/finals/all_parents.csv', index_col=False)

def get_family(lineage_df, time_span, sample_id, save_csv=False):
    # select for sample, time span
    lineage = lineage_df.loc[lineage_df['sample_id'] == sample_id,time_span]
    if save_csv:
        lineage.to_csv('/Users/kateharline/workspace/finals/'+str(sample_id)+'_d'+str(time_span[0])+'_d'+str(time_span[1]))
    return lineage

def get_family_h(lineage_df, time_spans, sample_ids, save_csv=False):
    for sample_id in sample_ids:
        for s in range(len(time_spans)):
            get_family(lineage_df, time_spans[s], sample_id, save_csv)
    return

get_family(lineage_df, [3,5], 'jawD_2-7')