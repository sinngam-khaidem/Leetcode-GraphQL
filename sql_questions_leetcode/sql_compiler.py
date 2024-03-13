import sqlite3
import json


def get_output(SQL_solution, input_testcase):
    """
    parameters:
        SQL_solution(str): SQL solution code
        input_tescase(dict)
    returns:
        output(dict)

    """
    # Convert input_testcase to SQL table
    input_data = input_testcase

    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    for table, rows in input_data['rows'].items():
        columns = ', '.join(input_data['headers'][table])
        placeholders = ', '.join(['?' for _ in input_data['headers'][table]])
        c.execute(f'CREATE TABLE {table} ({columns})')
        c.executemany(f'INSERT INTO {table} VALUES ({placeholders})', rows)
    conn.commit()
    
    # Execute SQL solution
    c.execute(SQL_solution)
    
    # Convert output table to JSON
    result = c.fetchall()
    columns = [description[0] for description in c.description]
    output = {'headers': columns, 'rows': result}
    
    return output
    

if __name__ == "__main__":
    pass






