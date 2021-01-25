from compare_helper import *
import pandas as pd
from collections import namedtuple

new_table = pd.read_csv(r'hive_new.csv', sep=';')
old_table = pd.read_csv(r'hive_old.csv', sep=';')
new_table_df = pd.DataFrame(new_table, columns=['column', 'datatype', 'comment'])
old_table_df = pd.DataFrame(old_table, columns=['column', 'datatype', 'comment'])
table_name = "DB.TABLE_NAME"
final_select_columns = ""
select_columns = ""
explode_collect_columns = ""
explode_columns = ""
group_by = ""
select_lookup = namedtuple('select_lookup', 'column explode_cols collect_cols struct_cols new_cols')
select_lookup_list = []
explode_select = ''

(new_columns_diff, removed_columns_diff, data_type_mismatch_diff) = compare_dataframe(new_table_df, old_table_df,
                                                                                      df_key='column',
                                                                                      compare_field='datatype')

new_columns_list = []
data_type_mismatch_list = []
print("----------------------Columns added----------------------------")
for index, row in new_columns_diff.iterrows():
    print("{}".format(row['column']))
    new_columns_list.append(row['column'])

print("\n----------------------Columns removed------------------------")
for index, row in removed_columns_diff.iterrows():
    print("{}".format(row['column']))

print("\n----------------------Data type mismatch----------------------")
for index, row in data_type_mismatch_diff.iterrows():
    print("{} : {}  -->  {}".format(row['column'].ljust(20), row['datatype_x'], row['datatype_y']))
    data_type_mismatch_list.append(row['column'])

print("\n----------------------Construct select-------------------------")


def describe_info1(path):
    print("DESC {}".format(path))
    df = pd.DataFrame(pd.read_csv(r'struct1.csv', sep=';'), columns=['column', 'datatype', 'comment'])
    return df


def describe_info2(path):
    print("DESC {}".format(path))
    df = pd.DataFrame(pd.read_csv(r'struct2.csv', sep=';'), columns=['column', 'datatype', 'comment'])
    return df

def describe_info3(path):
    print("DESC {}".format(path))
    df = pd.DataFrame(pd.read_csv(r'struct3.csv', sep=';'), columns=['column', 'datatype', 'comment'])
    return df

def describe_info4(path):
    print("DESC {}".format(path))
    df = pd.DataFrame(pd.read_csv(r'struct4.csv', sep=';'), columns=['column', 'datatype', 'comment'])
    return df

def is_nested_struct(table_name, column):
    nested_flag = False
    df = describe_info1("{}.{}".format(table_name, column))
    for index, row in df.iterrows():
        if str(row['datatype']).startswith('array<') or str(row['datatype']).startswith('struct<'):
            nested_flag = True
    return nested_flag


# struct1.csv
# If array<struct pass col.struct_name
# If col.item
# column_type = array/struct
def construct_struct_column(table_name, column, exists="Y"):
    struct_lookup_list = []
    new_col_df = describe_info1("{}.{}".format(table_name, column))
    old_col_df = describe_info2("{}.{}".format(table_name, column))

    if exists == 'Y':
        struct_lookup_list.append(
            select_lookup(column=column,
                          explode_cols='',
                          collect_cols='',
                          struct_cols=map_existing_struct_col(column, new_col_df, old_col_df,'N'),
                          new_cols=''))
    else:
        struct_lookup_list.append(
            select_lookup(column=column,
                          explode_cols='',
                          collect_cols='',
                          struct_cols='',
                          new_cols=map_new_struct_col(column, new_col_df)))
    return struct_lookup_list


def construct_arr_column(table_name, column, exists="Y"):
    select_lookup_list = []
    new_col_df = describe_info1("{}.{}".format(table_name, column))
    old_col_df = describe_info2("{}.{}".format(table_name, column))
    if exists == 'Y':
        select_lookup_list.append(
            select_lookup(column=column,
                          explode_cols="LATERAL VIEW explode({}) exploded_table as arr_{}".format(column, column),
                          collect_cols="collect_set(arr_{}_elements)".format(column),
                          struct_cols=map_existing_struct_col("arr_{}".format(column), new_col_df, old_col_df),
                          new_cols=''))

    else:
        select_lookup_list.append(
            select_lookup(column=column,
                          explode_cols='',
                          collect_cols='',
                          struct_cols='',
                          new_cols=map_new_struct_col(column, new_col_df)))
    return select_lookup_list

def construct_nested_column(column,new_nested_df: pd.DataFrame, old_nested_df: pd.DataFrame):
    (new_ncol_diff, removed_nested_columns_diff, data_type_mismatch_diff) = compare_dataframe(new_nested_df,
                                                                                          old_nested_df,
                                                                                          df_key='column',
                                                                                          compare_field='datatype')
    'named_struct() as {}'.format(column)
    select_columns=''
    global explode_columns
    global explode_collect_columns
    # construct new table columns
    if row['column'] in new_columns_diff:
        if str(row['datatype']).startswith('array<'):
            select_lookup_list = construct_arr_column(table_name, row['column'], 'N')
            for element in select_lookup_list:
                select_columns += "array({}) as {}\n,".format(element.new_cols, row['column'])
        elif str(row['datatype']).startswith('struct<'):
            if ':struct<' in str(row['datatype']) or ':array<struct<' in str(row['datatype']):
                pass
            else:
                select_struct_list = construct_struct_column(table_name, row['column'], 'N')
                for element in select_struct_list:
                    select_columns += "{} as {}\n,".format(element.new_cols, row['column'])
        else:
            select_columns += get_default_value(row['datatype']) + ' as ' + row['column'] + '\n,'

    # construct existing table columns with difference
    if row['column'] in data_type_mismatch_list:
        if str(row['datatype']).startswith('array<'):
            # complex data type
            select_lookup_list = construct_arr_column(table_name, row['column'])
            for element in select_lookup_list:
                explode_columns += element.explode_cols + '\n'
                select_columns += "{} as {}\n,".format(element.collect_cols, row['column'])
                explode_collect_columns += "{}\n,".format(element.struct_cols)
        elif str(row['datatype']).startswith('struct<'):
            if ':struct<' in str(row['datatype']) or ':array<struct<' in str(row['datatype']):
                # nested structure
                new_nested_df = describe_info3("{}.{}".format(table_name, row['column']))
                old_nested_df = describe_info4("{}.{}".format(table_name, row['column']))
                construct_nested_column(row['column'],new_nested_df,old_nested_df)
            else:
                select_struct_list = construct_struct_column(table_name, row['column'])
                for element in select_struct_list:
                    select_columns += "{} \n,".format(element.struct_cols)


# iterate by table columns

for index, row in new_table_df.iterrows():
    final_select_columns += '{},'.format(row['column'])

    if row['column'] not in new_columns_list and row['column'] not in data_type_mismatch_list:
        group_by += '{} ,'.format(row['column'])
        select_columns += '{}\n,'.format(row['column'])

    if row['column'] not in new_columns_list:
        explode_select += '{} ,'.format(row['column'])

    # construct new table columns
    if row['column'] in new_columns_list:
        if str(row['datatype']).startswith('array<'):
            select_lookup_list = construct_arr_column(table_name, row['column'], 'N')
            for element in select_lookup_list:
                select_columns += "array({}) as {}\n,".format(element.new_cols, row['column'])
        elif str(row['datatype']).startswith('struct<'):
            if ':struct<' in str(row['datatype']) or ':array<struct<' in str(row['datatype']):
                pass
            else:
                select_struct_list = construct_struct_column(table_name, row['column'], 'N')
                for element in select_struct_list:
                    select_columns += "{} as {}\n,".format(element.new_cols, row['column'])
        else:
            select_columns += get_default_value(row['datatype']) + ' as ' + row['column'] + '\n,'

    # construct existing table columns with difference
    if row['column'] in data_type_mismatch_list:
        if str(row['datatype']).startswith('array<'):
            # complex data type
            select_lookup_list = construct_arr_column(table_name, row['column'])
            for element in select_lookup_list:
                explode_columns += element.explode_cols + '\n'
                select_columns += "{} as {}\n,".format(element.collect_cols, row['column'])
                explode_collect_columns += "{}\n,".format(element.struct_cols)
        elif str(row['datatype']).startswith('struct<'):
            if ':struct<' in str(row['datatype']) or ':array<struct<' in str(row['datatype']):
                # nested structure
                new_nested_df = describe_info3("{}.{}".format(table_name, row['column']))
                old_nested_df = describe_info4("{}.{}".format(table_name, row['column']))
                construct_nested_column(row['column'],new_nested_df,old_nested_df)
            else:
                select_struct_list = construct_struct_column(table_name, row['column'])
                for element in select_struct_list:
                    select_columns += "{} \n,".format(element.struct_cols)

explode_sql = '(SELECT\n {}\n,{} FROM database.tableName \n{} \n) as l1 '.format(explode_select.rstrip(','),
                                                                                 explode_collect_columns.rstrip(','),
                                                                                 explode_columns)
select_for_insert_sql = 'SELECT\n{} \nfrom (\nSELECT \n{} \n{} \nGROUP BY {} ) as l2 '.format(final_select_columns.rstrip(','), select_columns.rstrip(','), explode_sql, group_by.rstrip(','))
print(select_for_insert_sql)
