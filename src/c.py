import requests
import sqlite3
import pandas as pd

def download_database(url, local_path='score.db'):
    """
    Downloads a SQLite database from a specified URL and saves it locally.
    
    Parameters:
    - url: str, the URL where the database can be downloaded
    - local_path: str, the local file path to save the database to
    """
    response = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(response.content)
    print(f"Database downloaded and saved to {local_path}.")

def connect_database(db_path='score.db'):
    """
    Connects to a SQLite database and returns the connection object.
    
    Parameters:
    - db_path: str, the path to the database file
    
    Returns:
    - conn: sqlite3.Connection, the connection object to the database
    """
    try:
        conn = sqlite3.connect(db_path)
        print("Successfully connected to the database.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def load_data_from_database(conn):
    """
    Loads data from all tables in the SQLite database into pandas DataFrames.
    
    Parameters:
    - conn: sqlite3.Connection, the connection object to the database
    
    Returns:
    - dataframes: dict, a dictionary where keys are table names and values are DataFrames containing the table data
    """
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(tables_query, conn)
    
    dataframes = {}
    for table_name in tables['name']:
        print(f"Loading data from table: {table_name}")
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        dataframes[table_name] = df
    return dataframes

# Example usage
if __name__ == "__main__":
    url = "https://techassessment.blob.core.windows.net/aiap-preparatory-bootcamp/score.db"
    db_path = 'score.db'
    
    # Download the database
    download_database(url, db_path)
    
    # Connect to the database
    conn = connect_database(db_path)
    
    # Load data from the database
    if conn:
        dataframes = load_data_from_database(conn)
        
        # Example: Print the first few rows of each table
        for table_name, df in dataframes.items():
            print(f"\nTable: {table_name}")
            print(df.head())
        
        # Close the connection
        conn.close()
