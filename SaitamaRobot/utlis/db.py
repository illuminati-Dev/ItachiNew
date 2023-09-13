# Import necessary modules
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient, AgnosticDatabase, AgnosticCollection
from SaitamaRobot import ANI_DB

# Define the list of symbols to export
__all__ = ['get_collection']

# Establish a connection to the MongoDB server
_MGCLIENT: AgnosticClient = AsyncIOMotorClient(ANI_DB)

# Function to check if the "Makima" database exists and create it if not
async def check_and_create_database():
    if "Makima" not in await _MGCLIENT.list_database_names():
        print("Makima Database Not Found :( => Creating New Database...")
        await _MGCLIENT["Makima"].list_collection_names()

# Run the database check and creation function
asyncio.get_event_loop().run_until_complete(check_and_create_database())

# Define the "Makima" database
_DATABASE: AgnosticDatabase = _MGCLIENT["Makima"]

# Function to get a collection from the "Makima" database
def get_collection(name: str) -> AgnosticCollection:
    """ Create or Get Collection from your database """
    return _DATABASE[name]

# Function to close the MongoDB client
def _close_db() -> None:
    _MGCLIENT.close()

# Usage example:
collection = get_collection("Makima")
# Perform database operations using the "collection" object

# To close the MongoDB client when done:
_close_db()
