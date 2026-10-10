import os
import sys
import json
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class NetworkDataExtract:

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = json.loads(data.T.to_json()).values()
            records = list(records)

            logging.info(
                f"CSV converted to JSON records: {len(records)}"
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        try:
            if not MONGO_DB_URL:
                raise ValueError(
                    "MONGO_DB_URL is missing from the .env file"
                )

            mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=15000
            )

            # Check connection
            mongo_client.admin.command("ping")

            # Select database and collection
            db = mongo_client[database]
            collection_obj = db[collection]

            # Insert CSV records into MongoDB
            if records:
                result = collection_obj.insert_many(records)
                inserted_count = len(result.inserted_ids)
            else:
                inserted_count = 0

            logging.info(
                f"Successfully inserted {inserted_count} records"
            )

            mongo_client.close()

            return inserted_count

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE = "TEJAS"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()

    print("Reading CSV file...")

    records = networkobj.csv_to_json(
        file_path=FILE_PATH
    )

    print(f"Total records converted: {len(records)}")

    print("Uploading records to MongoDB Atlas...")

    no_of_records = networkobj.insert_data_to_mongodb(
        records=records,
        database=DATABASE,
        collection=COLLECTION
    )

    print(f"Successfully uploaded {no_of_records} records!")
