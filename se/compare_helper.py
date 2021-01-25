import pandas as pd

def compare_dataframe(df1: pd.DataFrame, df2: pd.DataFrame, df_key, compare_field):
    merged_df = df1.merge(
        df2,
        indicator=True,
        how='outer',
        left_on=[df_key],
        right_on=[df_key]
    )
    new_columns_df = merged_df[(merged_df['_merge'] == 'left_only')]
    removed_columns_df = merged_df[(merged_df['_merge'] == 'right_only')]
    data_type_mismatch_df = merged_df[
        (merged_df['_merge'] == 'both') & (merged_df[compare_field + '_x'] != merged_df[compare_field + '_y'])]
    return new_columns_df, removed_columns_df, data_type_mismatch_df

def get_default_value(data_type):
    return {
        'int': 'cast(NULL as int)',
        'double': 'cast(NULL as double)',
        'string': 'cast(NULL as string)'
    }.get(data_type, 'cast(NULL as {})'.format(data_type))


def map_array_new_cols(array_col):
    global explode_columns
    explode_columns += "LATERAL VIEW explode({}) exploded_table AS arr_{}\n".format(array_col, array_col)


def map_new_struct_col(struct_column,new_struct_cols:pd.DataFrame):
    struct_col = ""
    for index, row in new_struct_cols.iterrows():
        struct_col += '"{}",{},'.format(row['column'], get_default_value(row['datatype']))
    return "named_struct({}) ".format(struct_col.rstrip(','))


def map_existing_struct_col(struct_column,new_struct_cols:pd.DataFrame,old_struct_def:pd.DataFrame,in_array='Y'):
    old_struct_cols_list = []
    struct_col = ""
    for index, row in old_struct_def.iterrows():
        old_struct_cols_list.append(row['column'])
    for index, row in new_struct_cols.iterrows():
        if row['column'] in old_struct_cols_list:
            struct_col += '"{}",{},'.format(row['column'], "{}.{}".format(struct_column, row['column']))
        else:
            struct_col += '"{}",{},'.format(row['column'], get_default_value(row['datatype']))
    suffix_column=''
    if in_array=='Y':
        suffix_column='_elements'
    return "named_struct({}) as {}{}".format(struct_col.rstrip(','), struct_column,suffix_column)
