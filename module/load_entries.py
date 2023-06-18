from clickhouse_driver import Client # type: ignore
import datetime
import concurrent.futures
from tqdm import tqdm
from typing import List, Tuple, Any

# Connect to ClickHouse server
client = Client('localhost')

# Create the table if it doesn't exist
create_table_query = '''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id Int32,
        movie_id Int32,
        progress Float64,
        timestamp DateTime
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMMDD(timestamp)
    ORDER BY (user_id, movie_id, timestamp)
'''
client.execute(create_table_query)


# Function to generate user progress entries
def generate_entries(start_index: int, end_index: int) -> List[Tuple[int, int, float, datetime.datetime]]:
    entries = []
    for i in range(start_index, end_index):
        progress = i / 1000.0  # Example: Progress ranges from 0.0 to 10,000.0
        timestamp = current_timestamp + datetime.timedelta(seconds=i)

        entry = (user_id, movie_id, progress, timestamp)
        entries.append(entry)

    return entries


# Generate and insert user progress entries in parallel using threads
user_id = 1
movie_id = 123
current_timestamp = datetime.datetime.now()

batch_size = 1000
total_entries = 10000000
batches = total_entries // batch_size

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for batch in tqdm(range(batches), desc='Batches', unit='batch'):
        start_index = batch * batch_size
        end_index = start_index + batch_size

        future = executor.submit(generate_entries, start_index, end_index)
        futures.append(future)

    for future in tqdm(concurrent.futures.as_completed(futures), desc='Inserts', total=batches, unit='batch'):
        entries = future.result()

        insert_query = 'INSERT INTO user_progress (user_id, movie_id, progress, timestamp) VALUES'
        client.execute(insert_query, entries, types_check=True)

# Close the connection
client.disconnect()
