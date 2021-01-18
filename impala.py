import pandas as pd

new_table = pd.read_csv(r'hive_new.csv', sep=';')
old_table = pd.read_csv(r'hive_old.csv', sep=';')
new_table_df = pd.DataFrame(new_table, columns=['column', 'datatype', 'comment'])
old_table_df = pd.DataFrame(old_table, columns=['column', 'datatype', 'comment'])
table_name = "DB.TABLE_NAME"
select_columns = ""
explode_columns = ""
group_by = ""


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


new_columns_diff, removed_columns_diff, data_type_mismatch_diff = compare_dataframe(new_table_df, old_table_df,
                                                                                    df_key='column',
                                                                                    compare_field='datatype')

new_columns_list = []
print("----------------------New columns added----------------------")
for index, row in new_columns_diff.iterrows():
    print("{}".format(row['column']))
    new_columns_list.append(row['column'])

print("----------------------Removed columns------------------------")
for index, row in removed_columns_diff.iterrows():
    print("{}".format(row['column']))

print("----------------------Data type mismatch----------------------")
for index, row in data_type_mismatch_diff.iterrows():
    print("{} : {}  -->  {}".format(row['column'].ljust(20), row['datatype_x'], row['datatype_y']))


def get_default_value(data_type):
    return {
        'int': '0',
        'double': '0.0',
        'string': "'None'"
    }.get(data_type, 'null')


def map_array_new_cols(array_col):
    global explode_columns
    explode_columns +="LATERAL VIEW explode({}) exploded_table AS arr_{}\n".format(array_col,array_col)


def map_new_struct_col(struct_column):
    struct_col = ""
    struct_def = pd.read_csv(r'struct_column.csv', sep=';')
    struct_col_df = pd.DataFrame(struct_def, columns=['column', 'datatype', 'comment'])
    for index, row in struct_col_df.iterrows():
        struct_col += '"{}":{},'.format(row['column'], get_default_value(row['datatype']))
    return "named_struct({}) {}".format(struct_col.rstrip(','),struct_column)

def map_existing_struct_col(struct_column):
    old_struct_cols_list=[]
    struct_col = ""
    new_struct_def = pd.read_csv(r'struct_column1.csv', sep=';')
    old_struct_def = pd.read_csv(r'struct_column2.csv', sep=';')
    new_struct_cols = pd.DataFrame(new_struct_def, columns=['column', 'datatype', 'comment'])
    for index, row in old_struct_def.iterrows():
        old_struct_cols_list.append(row['column'])
    for index, row in new_struct_cols.iterrows():
        if row['column'] in old_struct_cols_list:
            struct_col += '"{}":{},'.format(row['column'], "arr_{}.{}".format(struct_column,row['column']))
        else:
            struct_col += '"{}":{},'.format(row['column'], get_default_value(row['datatype']))

    return "named_struct({}) {}".format(struct_col.rstrip(','),struct_column)


print(map_new_struct_col('col_pos'))
print(map_existing_struct_col('arr_col2'))

def construct_complex_column(complex_col):
    # cal

    return 'named_struct("col1":string,"col2":int)' + ' as ' + complex_col


for index, row in new_table_df.iterrows():
    if row['column'] in new_columns_list:
        if str(row['datatype']).startswith('array<') or str(row['datatype']).startswith('struct<'):
            # complex data type
            select_columns += construct_complex_column(row['column']) + ','
        select_columns += get_default_value(row['datatype']) + ' as ' + row['column'] + ','
    else:
        select_columns += row['column'] + ','

print(select_columns)
map_array_new_cols('arry_col1')
map_array_new_cols('arry_col2')
print(explode_columns)
