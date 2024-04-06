import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["lego_sets"]
collection = db["sets"]



# Read data from TXT file and insert into MongoDB
with open("lego_sets.txt", "r") as file:
    for line in file:
        data = line.strip().split(",")
        theme = data[0]
        name = data[1]
        set_number = data[2]
        pieces = int(data[3])
        minifigs = int(data[4])
        price = float(data[5].replace("$", ""))
        price_per_piece = float(data[6].replace("c", ""))
        year = int(data[7])
        packaging = data[8]

        set_data = {
            "theme": theme,
            "name": name,
            "set_number": set_number,
            "pieces": pieces,
            "minifigs": minifigs,
            "price": price,
            "price_per_piece": price_per_piece,
            "year": year,
            "packaging": packaging
        }
        collection.insert_one(set_data)
