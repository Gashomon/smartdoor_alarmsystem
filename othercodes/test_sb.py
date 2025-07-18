from supabase import create_client, Client

url: str = 'https://tlgkpnmiwlqqkxzoequy.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsZ2twbm1pd2xxcWt4em9lcXV5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MTczMjI2NiwiZXhwIjoyMDY3MzA4MjY2fQ.AS_0mU5D-7c7V9IjoWyS23OIQEsTIRGEzZWc7uExEKA'
supabaser: Client = create_client(url, key)

response = (
    supabaser.storage.get_bucket("test-bucket")
)
print(response)
response = (
    supabaser.table("test_table")
    .select("*")
    .execute()
)

print("supabase client is " + str(supabaser))
print("supabase content is " + str(response))

    # (
    #     supabaser.table('test_table')
    #     .insert(
    #         {
    #             "id" : 2,
    #             "value" : "hi"
    #         }
    #     )
    #     .execute()
    # )