import psycopg

def is_module_exist(cursor, module_name:str, db_name:str) -> None:

    """
        Check if the module is in the database from assembly.
    """

    query = f"""
        SELECT 1
        FROM public.module_assembly
        WHERE module_name = %s
        LIMIT 1;
    """

    cursor.execute(query, (module_name,))
    result = cursor.fetchone()

    if not result:
        print(f"Value '{module_name}' does not exist in tabel 'module_assembly' of '{db_name}' database.")
        exit(1)

def count_insertion_iteration(cursor, module_state:str, which:str) -> int:

    """
        Count how much data for a given object is in database
    """

    query = f"""
        SELECT COUNT(*)
        FROM public.{module_state}_inspect
        WHERE {module_state}_name = %s;
    """
    cursor.execute(query, (which,))
    result = cursor.fetchone()

    return result[0]

def grade_module(info:dict) -> str:

    x_offset = abs(info['x_offset_mu'])
    y_offset = abs(info['y_offset_mu'])
    angle    = info['ang_offset_deg']

    if x_offset <= 50 and y_offset <= 50 and angle <= 0.02:
        return "A"
    elif x_offset <= 100 and y_offset <= 100 and angle <= 0.04:
        return "B"
    else:
        return "C"

def write_to_database(module_qc_dict: dict, config: dict) -> None:

    for module_name, module_qc in module_qc_dict.items():

        proto_data = {

            'proto_name'     : '',
            'x_offset_mu'    : module_qc['center_offsets']['sensor'][0],
            'y_offset_mu'    : module_qc['center_offsets']['sensor'][1],
            'ang_offset_deg' : module_qc['angle_offsets']['sensor'],
            'grade'          : None,
            'date_inspect'   : 0,
            'inspector'      : config['inspector'],
            'iteration'      : 1
        }

        proto_data_column = ', '.join(proto_data.keys())
        proto_data_column_placeholders = ', '.join(['%s'] * len(proto_data))

        module_data = {

            'module_name'      : module_name,
            'flatness'         : module_qc['Vacuum']['flatness'],
            'avg_thickness'    : module_qc['Vacuum']['thickness'],
            'max_thickness'    : module_qc['Vacuum']['max_height'],
            'x_offset_mu'      : module_qc['center_offsets']['pcb'][0],
            'y_offset_mu'      : module_qc['center_offsets']['pcb'][1],
            'ang_offset_deg'   : module_qc['angle_offsets']['pcb'],
            'grade'            : None,
            'date_inspect'     : 0,
            'inspector'        : config['inspector'],
#            'hexplot'          : None,
#            'offsetplot'       : None,
            'x_points'         : module_qc['Vacuum']['x_points'].tolist(),
            'y_points'         : module_qc['Vacuum']['y_points'].tolist(),
            'z_points'         : module_qc['Vacuum']['z_points'].tolist(),
            'iteration'        : 1

        }

        module_data_column = ', '.join(module_data.keys())
        module_data_column_placeholders = ', '.join(['%s'] * len(module_data))

        # Connect to database
        with psycopg.connect(
            dbname   = config['database_name'],
            user     = config['user'],
            password = config['password'],
            host     = config['host'],
            port     = 5432
        ) as connection:
            with connection.cursor() as cursor:

                is_module_exist(cursor, module_name, config['database_name'])

                # Fetch proto module information from module_assembly table
                query = f"""
                    SELECT proto_name, ass_run_date FROM public.module_assembly
                    WHERE module_name = %s
                """
                cursor.execute(query, (module_name,))
                results = cursor.fetchall()

                if len(results) == 0 or results[-1][0] == None:
                    print(f"Value '{module_name}' has no 'proto_name' in tabel 'module_assembly'.")
                    exit(1)
                proto_name, timestemp = results[-1]

                proto_data['proto_name']    = proto_name
                proto_data['date_inspect']  = timestemp
                proto_data['grade']         = grade_module(proto_data)
                proto_data['iteration']     = count_insertion_iteration(cursor, "proto", proto_name)
                module_data['date_inspect'] = timestemp
                module_data['grade']        = grade_module(module_data)
                module_data['iteration']    = count_insertion_iteration(cursor, "module", module_name)

                # Proto module data insertion
                insert_query = f"""
                    INSERT INTO proto_inspect ({proto_data_column})
                    VALUES ({proto_data_column_placeholders});
                """

                cursor.execute(insert_query, tuple(proto_data.values()))
                connection.commit()

                # Module data insertion
                insert_query = f"""
                    INSERT INTO module_inspect ({module_data_column})
                    VALUES ({module_data_column_placeholders});
                """

                cursor.execute(insert_query, tuple(module_data.values()))
                connection.commit()

                print(f"Module '{module_name}' QC data has been put into database successfully.")
