import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["lego_sets"]
collection = db["sets"]

# Read data from TXT file and insert into MongoDB
with open("lego_sets.txt", "r") as file:
    set_data = {}
    for line in file:
        line = line.strip()
        if line.startswith("Name:"):
            set_data = {}  # Reset set_data for a new LEGO set
            line = line.replace("Name: ", "")
            set_data["name"] = line
        elif line.startswith("Pieces:"):
            line = line.replace("Pieces: ", "")
            try:
                set_data["pieces"] = int(line)
            except ValueError:
                set_data["pieces"] = None
        elif line.startswith("Minifigs:"):
            line = line.replace("Minifigs: ", "")
            if line.lower() == "none":
                set_data["minifigs"] = None
            else:
                try:
                    set_data["minifigs"] = int(line)
                except ValueError:
                    set_data["minifigs"] = None
        elif line.startswith("Theme:"):
            line = line.replace("Theme: ", "")
            set_data["theme"] = line
        elif line.startswith("Set Number:"):
            line = line.replace("Set Number: ", "")
            set_data["set_number"] = line
        elif line.startswith("Year:"):
            line = line.replace("Year: ", "")
            set_data["year"] = int(line)
        elif line.startswith("=" * 50):
            # End of set data, insert into MongoDB
            collection.insert_one(set_data)
