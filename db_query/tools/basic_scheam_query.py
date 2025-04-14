import logging
from typing import Any, Generator
import tabulate
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.mongo_util import MongoDbUtil


class BasicScheamQuery(Tool):
    def _invoke(
            self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke MongoDB query tool.
        """
        db_host = tool_parameters.get("db_host", "")
        if not db_host:
            raise ValueError("Please fill in the MongoDB host")

        db_port = tool_parameters.get("db_port", 27017)  # Default MongoDB port
        db_username = tool_parameters.get("db_username", "")
        db_password = tool_parameters.get("db_password", "")
        db_name = 'table_info'
        collection_name = 'table_simple_info'
        query = {}
        projection = tool_parameters.get("projection", {})
        # Validate required parameters
        if not collection_name:
            raise ValueError("Please specify the MongoDB collection name")
        try:
            # Initialize MongoDB utility
            mongo_util = MongoDbUtil(
                db_type='mongodb',
                username=db_username,
                password=db_password,
                host=db_host,
                port=db_port,
                database=db_name
            )
        except Exception as e:
            message = "MongoDB connection creation exception."
            logging.exception(message)
            raise Exception(message + f" {e}")

        try:
            # Execute query
            records = mongo_util.run_query(collection_name, query, projection)
            if records:
                text = tabulate.tabulate(records, headers="keys", tablefmt="github")
            else:
                text = "No records found matching the query."

            # Return result
            yield self.create_text_message(text)
        except Exception as e:
            message = "MongoDB query execution exception."
            logging.exception(message)
            raise Exception(message + f" {e}")
