def construct_nested_struct_column(table_name,nested_struct_column,exists="Y"):
    new_nested_col_df = describe_info3("{}.{}".format(table_name, nested_struct_column))
    old_nested_col_df = describe_info4("{}.{}".format(table_name, nested_struct_column))
    # iterate through struct columns
    (new_ncol_diff, removed_ncol_diff, mismatch_ncol_diff) = compare_dataframe(new_nested_col_df,
                                                                                              old_nested_col_df,
                                                                                              df_key='column',
                                                                                              compare_field='datatype')
    global explode_columns
    global explode_collect_columns
    struct_columns=''
    new_ncolumn_list=[]
    mismatch_ncolumn_list = []
    for index, row in new_ncol_diff.iterrows():
        #print("{}".format(row['column']))
        new_ncolumn_list.append(row['column'])
    for index, row in mismatch_ncol_diff.iterrows():
        #print("{}".format(row['column']))
        mismatch_ncolumn_list.append(row['column'])

    for index, row in new_nested_col_df.iterrows():
        struct_columns +='"{}",{}\n,'.format(row['column'],'{}.{}'.format(nested_struct_column,row['column']) )
        if row['column'] in new_ncolumn_list:
            if str(row['datatype']).startswith('array<'):
                select_lookup_list = construct_arr_column(table_name, row['column'], 'N')
                for element in select_lookup_list:
                    struct_columns =struct_columns.replace('{}.{}'.format(nested_struct_column,row['column']), "array({})".format(element.new_cols, row['column']))
            elif str(row['datatype']).startswith('struct<'):
                select_struct_list = construct_struct_column(table_name, row['column'], 'N')
                for element in select_struct_list:
                    struct_columns = struct_columns.replace('{}.{}'.format(nested_struct_column,row['column']),"{}".format(element.new_cols,row['column']))
            else:
                struct_columns = struct_columns.replace('{}.{}'.format(nested_struct_column,row['column']),get_default_value(row['datatype']))

        if row['column'] in mismatch_ncolumn_list:
            if str(row['datatype']).startswith('array<'):
                # complex data type
                select_lookup_list = construct_arr_column(table_name, '{}.{}'.format(nested_struct_column,row['column']))
                for element in select_lookup_list:
                    explode_columns += element.explode_cols + '\n'
                    struct_columns += "{} as {}\n,".format(element.collect_cols, row['column'])
                    explode_collect_columns += "{}\n,".format(element.struct_cols)
            elif str(row['datatype']).startswith('struct<'):
                select_struct_list = construct_struct_column(table_name, row['column'])
                for element in select_struct_list:
                    struct_columns = struct_columns.replace(',{},'.format(str(row['column'])),
                                                                            "\n,{} \n,".format(element.struct_cols))

    print('named_struct(\n{})'.format(struct_columns.rstrip(',')))
