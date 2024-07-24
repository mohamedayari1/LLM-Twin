import json
import logging

from bson import jsong_util
from mq import publish_data_to_rabbitmq

from db import MongoDatabaseConnector

#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def stream_process():
    try:
        # Setup MongoDB connection
        client = MongoDatabaseConnector()
        db = client["scrabble"] #change it to the name of your DB
        logging.info("Connected to MongoDB")
        
        # Watch changes in a specific collection
        changes = db.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])
        for change in changes:
            data_type = change["ns"]["coll"]
            entry_id = change["fullDocument"].pop("_id")
            change["fullDocument"]["type"] = data_type
            change["fullDocument"]["entry_id"] = entry_id
            
            #Use json_util to serialize the document
            data = json.dumps(change["fullDocument"], default=json_util.default)
            logging.info(f"Change detected and serialized:  {data}")

            # Send data to rabbitmq
            publish_data_to_rabbitmq(queue_name="default", data=data)
            logging.info("Data published to RabbitMQ")
            
    except Exception as e:
        logging.error(f"An error occured: {e}")
        
if __name__ == "__main__":
    stream_process()