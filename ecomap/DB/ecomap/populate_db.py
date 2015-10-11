# coding=utf-8
from pprint import pprint
import MySQLdb
from mysql.connector import OperationalError, ProgrammingError
import re
# from settings import password

PATH = '/home/padalko/ss_projects/Lv-164.UI'

db = MySQLdb.connect("localhost", 'root', 'nirvana94', 'ecomap')

COLUMN_INFO = [
    'Field',
    'Type',
    'Null',
    'Key',
    'Default',
    'Extra'
]


# get_tables = db.cursor()
# get_tables.execute('show tables;')
# tables = reduce_seq(get_tables.fetchall())


def reduce_seq(seq):
    res = []
    for item in seq:
        if hasattr(item, '__iter__'):
            for x in item:
                res.append(x)
        else:
            res.append(item)
    return res


def make_dict(keys, vals):
    result = dict(zip(keys, vals))
    extra_keys = set(keys) - set(result.iterkeys())
    if extra_keys:
        for key in extra_keys:
            result[key] = None
    return result


def show_full_table_info(table):
    q = db.cursor()
    q.execute("show columns FROM %s;" % table)
    qs = q.fetchall()
    detailed_qs = ([make_dict(COLUMN_INFO, row) for row in qs if qs])
    output_query = {}
    for dct in detailed_qs:
        table_field_key = dct.pop('Field')
        output_query[table_field_key] = {}
        output_query[table_field_key].update((k.upper(), v) for (k, v) in dct.iteritems())
        output_query[table_field_key]['__TABLE_NAME__'] = table
    return output_query


def make_query(sql, table=None):
    """
    :rtype : list of dictionaries
    """
    qs = db.cursor()
    qs.execute("%s" % sql)
    values = qs.fetchall()
    result = []
    if table:
        get_table_info = db.cursor()
        get_table_info.execute("show columns FROM %s;" % table)
        keys = get_table_info.fetchall()
        parsed_keys = [x[0] for x in keys if keys]
        for val in values:
            result.append(dict(zip(parsed_keys, val)))
        return result
    else:
        for val in values:
            result.append(val)
        return result

# pprint(make_query("select * from Product;" "Product"))
# pprint(show_full_table_info('Region'))
# pprint(map(show_full_table_info, tables))

def exec_sql_file(cursor, sql_file):
    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    sql_statement = ""
    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            sql_statement += line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            sql_statement += line
            # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (sql_statement)
            try:
                cursor.execute(sql_statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            sql_statement = ""

exec_sql_file(db.cursor(), '{}/ecomap/DB/ecomap/CREATE_DB.sql'.format(PATH))
exec_sql_file(db.cursor(), '{}/ecomap/DB/ecomap/INSERT_DATA.sql'.format(PATH))

print 'Users:'
pprint(make_query('select * from Users;', 'Users'))
print 'Problems:'
pprint(make_query('select * from Problems;', 'Problems'))
print 'Detailed_problems:'
pprint(make_query('select * from Detailed_problems;', 'Detailed_problems'))
# pprint(tables)
# pprint(show_full_table_info('Photos'))
# pprint(map(show_full_table_info, tables))
db.close()
