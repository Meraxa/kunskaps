import math
from typing import Any, Mapping, TypeVar

import motor.motor_asyncio
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedDatabaseResponse:
    """
    A class for handling paginated database responses.

    Args:
        items (list): The list of items to be returned.
        pages (int): The number of pages.
        total (int): The total number of items.
    """

    def __init__(self, items: list = [], pages: int = 0, total: int = 0):
        """Constructor method for the PaginatedDatabaseResponse class.

        Args:
            items (list, optional): The items that are returned in the current
                page. Defaults to [].
            pages (int, optional): The current page that is returned.
                Defaults to 0.
            total (int, optional): The total amount of available pages.
                Defaults to 0.
        """
        self.items = items
        self.pages = pages
        self.total = total


class DatabaseBaseHandler:
    """
    A base class for handling database operations.

    Args:
        database_url (str): The URL of the database.
        database_name (str): The name of the database.
        database_collection_name (str): The name of the collection in the
            database.

    Attributes:
        database_client: The client for connecting to the database.
        database: The database object.
        database_collection: The collection object in the database.
    """

    def __init__(
        self,
        database_url: str,
        database_name: str,
        database_collection_name: str,
    ):
        """
        Constructor method for the DatabaseBaseHandler class.

        Args:
            database_url (str): The URL of the database.
            database_name (str): The name of the database.
            database_collection_name (str): The name of the collection in the
                database.
        """
        self.database_client = motor.motor_asyncio.AsyncIOMotorClient(
            host=database_url
        )
        self.database = self.database_client[database_name]
        self.database_collection = self.database.get_collection(
            database_collection_name
        )

    async def add_entry_to_database(
        self, model: T
    ) -> Mapping[str, Any] | None:
        """
        Adds an entry to the database.

        Args:
            model (T): The model object to be added to the database.

        Returns:
            Mapping[str, Any] | None: If successful the inserted entry as
                dictionary, otherwise None.
        """
        insert_response = await self.database_collection.insert_one(
            model.model_dump(by_alias=True)
        )
        inserted_entry = await self.database_collection.find_one(
            {"_id": insert_response.inserted_id}
        )
        if inserted_entry:
            return inserted_entry
        return None

    async def retrieve_entries_from_database(
        self,
        query: dict,
        page: int = 1,
        sort: dict = {"_id": 1},
        limit: int = 10,
    ) -> PaginatedDatabaseResponse:
        """
        Retrieves entries from the database based on the given query.

        Args:
            query (dict): The query to filter the entries.
            page (int): The page number for pagination.
            sort (dict): The sort order of the retrieved entries.
            limit (int): The maximum number of entries to retrieve.

        Returns:
            PaginatedDatabaseResponse: The list of retrieved entries from the
                database.
        """

        skip = 0
        if page > 1:
            skip = (page - 1) * limit

        entries = [
            entry
            async for entry in self.database_collection.find(query)
            .sort(sort)
            .skip(skip)
            .limit(limit)
        ]

        total = await self.database_collection.count_documents(query)

        response = PaginatedDatabaseResponse(
            items=entries, pages=math.ceil(total / limit), total=total
        )
        return response

    async def retrieve_entry_from_database(
        self, query: dict
    ) -> Mapping[str, Any] | None:
        """
        Retrieves a single entry from the database based on the given ID.

        Args:
            query (dict): The query to filter the entry.

        Returns:
            T: The retrieved entry from the database.
        """
        entry = await self.database_collection.find_one(query)
        if entry:
            return entry
        return None

    async def update_entry_in_database(
        self, query: dict, model: T
    ) -> Mapping[str, Any]:
        """
        Updates an entry in the database based on the given ID.

        Args:
            query (dict): The query to filter the entry.
            model (T): The updated model object.

        Returns:
            T: The updated entry from the database.
        """
        updated_response = await self.database_collection.update_one(
            query, {"$set": model.model_dump(by_alias=True)}
        )
        if updated_response:
            updated_entry = await self.database_collection.find_one(query)
            if updated_entry:
                return updated_entry

    async def delete_entry_from_database(self, query: dict) -> bool:
        """
        Deletes an entry from the database based on the given ID.

        Args:
            query (dict): The query to filter the entry.

        Returns:
            bool: True if the entry was successfully deleted, False otherwise.
        """
        entry = await self.database_collection.find_one(query)
        if entry:
            await self.database_collection.delete_one(query)
            return True
        return False
