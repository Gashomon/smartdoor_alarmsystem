from supabase import create_client, Client

url: str = ''
key: str = ''
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