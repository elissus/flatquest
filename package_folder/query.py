from google.cloud import bigquery
import pandas as pd

def query_bq():
    client = bigquery.Client()

    query = f"""
    select *
    FROM `flatquest-430519.flatquest_dataset.berlin_cleaned`
    """

    print("Executing query:")
    print(query)

    query_job = client.query(query)
    results = query_job.result()
    rows = [dict(row) for row in results]
    df = pd.DataFrame(rows)

    if df.empty:
        print("No results found.")
    else:
        print(f"Found {len(df)} results.")

    return df

def main():
    results = query_bq()
    for row in results:
        print(row)

if __name__ == "__main__":
    main()
