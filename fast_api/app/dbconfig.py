from databases import Database

    # Set your database connection string
DATABASE_URL = "mysql+asyncmy://root:Test@1262@localhost/fastapi"


database = Database(DATABASE_URL)


async def connect_db():
    try:
        await database.connect()
        print("Database connection successful!")
    except Exception as e:
            print(f"Error connecting to database: {e}")

async def disconnect_db():
    try:
        await database.disconnect()
        print("Database disconnected successfully!")
    except Exception as e:
            print(f"Error disconnecting from the database: {e}")
