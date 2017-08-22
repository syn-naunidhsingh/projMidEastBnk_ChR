
import dbnames


# Input: Dictionary containing name value pairs of extracted data from passport.
# Objective insert data into database and return status
def insert(mongo, subVal, uniqueId):
    # Connect with the database and insert Data

    try:
        if not dbnames.__PP_NO__ in subVal:
            return False
        else:
            subVal[dbnames.__PP_USER_ID__] = uniqueId
        if not dbnames.__PP_NAME__ in subVal:
            subVal[dbnames.__PP_NAME__] = None
        if not dbnames.__PP_EXPIRY__ in subVal:
            subVal[dbnames.__PP_EXPIRY__] = None
        if not dbnames.__PP_COUNTRY__ in subVal:
            subVal[dbnames.__PP_COUNTRY__] = None
        if not dbnames.__PP_DOB__ in subVal:
            subVal[dbnames.__PP_DOB__] = None

    except Exception as e:
        print e
        return False


    try:
        user_collection = mongo.db.passportdetails
        # check if data exists
        if user_collection.find_one({dbnames.__PP_USER_ID__: uniqueId}):
            user_collection.update_one({dbnames.__PP_USER_ID__: subVal[dbnames.__PP_USER_ID__]}, {"$set": subVal})
        # Otherwise override the existing data
        else:
            user_collection.insert_one(subVal)

        return True

    except:
        return False


