# The Database class handles all CRUD operations to and from MongoDB

from bson import ObjectId
from pymongo.errors import PyMongoError

from database.patient import Patient

class Database:
    def __init__(self, db):
        self.db = db

    # Create empty collection when new bay created in UI
    def create_bay(self, bay_num: int) -> bool:
        collection_name = str(bay_num)

        if collection_name in self.db.list_collection_names():
            # Collection was not created - already existed
            return False

        self.db.create_collection(collection_name)
        # Collection was created - did not exist
        return True

    # Drop a bay collection when bay deleted in UI
    def delete_bay(self, bay_num: int) -> bool:
        collection_name = str(bay_num)

        if collection_name not in self.db.list_collection_names():
            # Collection was not dropped - did not exist
            return False

        self.db[collection_name].drop()
        # Collection was dropped - did exist
        return True

    # Inserts patient to Mongo - sends it to the same collection as BAY field
    def insert_patient(self, patient: Patient) -> ObjectId | None:
        collection = self.db.get_collection(str(patient.bay))
        try:
            result = collection.insert_one(patient.to_dict())
            patient.id = result.inserted_id

            # Return inserted patient id
            return patient.id
        except PyMongoError as e:
            print(f"Failed to insert patient: {e}")
            return None

    # Updates patient in Mongo - same collection as BAY field
    def update_patient(self, patient: Patient) -> bool:
        if not patient.id:
            raise ValueError("Patient does not have an _id.")

        collection = self.db.get_collection(str(patient.bay))

        try:
            result = collection.update_one(
                {"_id": patient.id},
                {"$set": patient.to_dict()} # all new fields
            )
            return result.modified_count == 1
        except PyMongoError as e:
            print(f"Failed to update patient: {e}")
            return False

    # Deletes patient from Mongo - from same collection as BAY field
    def delete_patient(self, patient: Patient) -> bool:
        if not patient.id:
            raise ValueError("Patient does not have an _id.")

        collection = self.db.get_collection(str(patient.bay))

        try:
            result = collection.delete_one({"_id": patient.id})
            return result.deleted_count == 1
        except PyMongoError as e:
            print(f"Failed to delete patient: {e}")
            return False

    # Finds existing MongoDB document by bay and bed location
    # If not existing, create new document with empty patient
    # Helps with populating empty beds that already have a document
    def find_create_patient(self, bay: int, bed: int) -> Patient:
        collection = self.db.get_collection(str(bay))

        doc = collection.find_one({"bay": bay, "bed": bed})

        if doc:
            return Patient.from_document(doc)
        else:
            empty_patient = Patient.empty(bay, bed)
            self.insert_patient(empty_patient)
            return self.find_create_patient(empty_patient.bay, bed)

    # List patients in ONE bay - specified by passed int
    def get_bay_patients(self, bay: int) -> list[Patient]:
        collection = self.db.get_collection(str(bay))

        try:
            docs = collection.find({
                # Get documents with an EXISTING presence
                # does NOT have to equal a specific value
                "presence": {"$exists": True}
            })
            return [Patient.from_document(doc) for doc in docs]
        except PyMongoError as e:
            print(f"Failed to get patients: {e}")
            return []