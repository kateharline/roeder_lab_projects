import pandas as pd

df = pd.read_csv('/Users/kateharline/workspace/finals/d_full_for_parent_track.csv', index_col=False)
# remove weird index
df = df.iloc[:, 1:]

# get samples and time steps for iteration
samples = df['sample_id'].unique()
# forward order for colnames
times = list(df['time'].unique())
lineage_df = pd.DataFrame(columns=['sample_id'] + times)
print(lineage_df)

i_end = 0
for s in samples:
    print('Finding parents sample '+str(s))
    # recalculate time for a given sample ... so that time point traverse is correct
    times = list(df[df['sample_id'] == s]['time'].unique())
    # reverse the order for iteration
    times = times[::-1]
    for t in times:
        # check that time exists for that sample
        if not df[(df['sample_id'] == s) & (df['time'] == t)].empty:
            print('time '+str(t))
            i = i_end
            # last time point label
            if t == times[0]:
                # select df per this sample and time
                s_d = df.loc[(df['sample_id'] == s) & (df['time'] == t)]
                # set the oldest labels
                for o_l in s_d['Label']:
                    lineage_df.loc[i, t] = o_l
                    lineage_df.loc[i, 'sample_id'] = s
                    i += 1

            else:
                # select df previous sample and time
                s_d = df.loc[(df['sample_id'] == s) & (df['time'] == t+1)]
                # whoopsies, def have to make sample specific
                for l in lineage_df[lineage_df['sample_id'] == s][t+1]:
                    # check that parent exists
                    if s_d[s_d['Label'] == l].empty:
                        lineage_df.loc[i, t] = 0
                    else:  # lookup parents
                        lineage_df.loc[i, t] = int(s_d[s_d['Label'] == l]['Parent'])
                    i += 1

            if t == times[-1]:
                i_end = i

lineage_df.to_csv('/Users/kateharline/workspace/finals/all_parents.csv')
