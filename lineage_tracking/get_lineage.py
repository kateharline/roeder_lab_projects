import pandas as pd

def get_parent(lineage_df, parent, sample_id):
    '''

    :param lineage_df: dataframe of a lineage for a given base time
    :param parent: int timepoint to retrieve parents for
    :param sample_id: str
    :return: df w giben timepoint's parent selected
    '''
    # select for sample, time span
    lineage = lineage_df[lineage_df['sample_id'] == sample_id][[str(parent)]]
    lineage.rename(columns={str(parent): 'Parent_d_'+str(parent)}, inplace=True)
    return lineage

def get_family(lineage_df, times, parents, sample_ids, save_csv=False):
    '''

    :param lineage_df: dataframe from all_parents with lineage backtracked
    :param time: int youngest time point
    :param parents: list of ints older time points to retrieve parents
    :param sample_ids: list of strings samples to survey
    :param save_csv: bool whether or not to export given family df
    :return:
    '''
    # for nice save string
    parent_string = '_'.join([str(p) for p in parents])
    print(parent_string)

    for time in times:
        families = pd.DataFrame()

        for sample_id in sample_ids:
            # check that lineage exists for a given timepoint
            if not lineage_df[lineage_df['sample_id'] == sample_id][['sample_id', str(time)]].empty:
                # select sample and time
                lineage = lineage_df[lineage_df['sample_id'] == sample_id][['sample_id', str(time)]]
                # make nice columns for use with R dataframes
                lineage['sample_id'] = sample_id
                lineage['time'] = time
                lineage.rename(columns={str(time): 'Label'}, inplace=True)
                for p in parents:
                    # lookup each prev time parent
                    p_lineage = get_parent(lineage_df, p, sample_id)
                    # add column for diff parent times
                    lineage = pd.concat([lineage, p_lineage], axis=1)

                # add rows for diff samples
                families = pd.concat([families, lineage], axis=0)
                print(families)

        if save_csv:
            families.to_csv('/Users/kateharline/workspace/finals/families_d'+str(time) + '_to_ds_'+parent_string+'.csv')
    return

lineage_df = pd.read_csv('/Users/kateharline/workspace/finals/all_parents.csv', index_col=False)

# all day 8 <- 3
get_family(lineage_df, [8, 7, 6, 5], [4], lineage_df['sample_id'].unique(), True)