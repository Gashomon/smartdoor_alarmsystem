from supabase import create_client, Client

url: str = ''
key: str = ''
supabaser: Client = create_client(url, key)
response = (
    supabaser.table("test_table")
    .select("*")
    .execute()
)
print("supabase client is " + str(supabaser))
print("supabase content is " + str(response))