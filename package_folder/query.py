from google.cloud import bigquery

rent = 1000
area = 80
rooms = 2
balcony = 'True'
result_limit = 10

def query():#rent, area, rooms, balcony):

    client = bigquery.Client()

    query = f"""
    with data as (
    SELECT
        description as description,
        fullAddress as address,
         totalRent as rent,
        livingSpace as area,
        noRooms as rooms,
        balcony as balcony

        FROM `flatquest-430519.flatquest_dataset.df_berlin_cleaneed`
    )
    select *
    from data
    where rent <= 1000
    and area >= 80
    and rooms >= 2
    and balcony = 'True'
    limit 10
    """

    query_job = client.query(query)
    results = query_job.result()
    rows = [dict(row) for row in results]
    return rows

def main():
    results = query()
    for row in results:
        print(row)

if __name__ == "__main__":
    main()
