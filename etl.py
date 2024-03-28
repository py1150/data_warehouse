import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, validate_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        print('\n\n')
        print('-----------------')
        print(f'_Executing the following query:_')
        print(query)
        try:
            cur.execute(query)
            conn.commit()
            print('_execution successful_')
            print('-----------------')
        except psycopg2.Error as e:
            print(f'\n***Error during staging table load with: {e}')


def insert_tables(cur, conn):
    for query in insert_table_queries:
        print('\n\n')
        print('-----------------')
        print(f'_Executing the following query:_')
        print(query)
        try:
            cur.execute(query)
            conn.commit()
            print('_execution successful_')            
            print('-----------------')
        except psycopg2.Error as e:
            print(f'\n***Error during inserting tables with: {e}')


def validate_tables(cur,conn):
    for query in validate_table_queries:
        print('\n\n')
        print('-----------------')
        print(f'_Executing the following query:_')
        print(query)
        try:
            cur.execute(query)
            conn.commit()
            print('_execution successful_')
            print('_Result:')
            row = cur.fetchone()            
            print(row)
            print('-----------------')
        except psycopg2.Error as e:
            print(f'\n***Error during validating tables with: {e}')


def main():
    
    # retrieve parameters
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    #conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    HOST               = config.get('CLUSTER','HOST')
    DB_NAME            = config.get('CLUSTER','DB_NAME')
    DB_USER            = config.get('CLUSTER','DB_USER')
    DB_PASSWORD        = config.get('CLUSTER','DB_PASSWORD')
    DB_PORT            = config.get('CLUSTER','DB_PORT')

    ARN = config.get('IAM_ROLE','ARN')
    print('--------')    
    print('Configurations retrieved')
    print(f'roleARN is: {ARN}\n')

    # connect to database
    try:
        conn_string ="host={} dbname={} user={} password={} port={}"\
            .format(HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)
        conn = psycopg2.connect(conn_string)
        #conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"\
        #    .format(HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT))
        cur = conn.cursor()
        
        print(f'connected with: {conn_string}')        
        print('--------')
    except psycopg2.Error as e:
        print(f'\nError during connection with: {e}')

    # load stagin tables
    load_staging_tables(cur, conn)    

    # insert from staging into final tables
    insert_tables(cur, conn)
    
    # validate
    validate_tables(cur, conn)
    
    # close the connection
    conn.close()


if __name__ == "__main__":
    main()