import json

def load_room():
    with open ("json/room.json", encoding = "utf-8") as f:
        return json.load(f)

def search_room(guest=2, type=None, trang_thai="Available"):
    with open("json/room.json", encoding="utf-8") as f:
        rooms = json.load(f) 
        rooms = [r for r in rooms if guest <= r['capacity'] and r['status'].__eq__(trang_thai)]
        if type:
            rooms = [r for r in rooms if r['type'].__eq__(type)]
        return rooms



# if __name__== "__main__":
#     print(search_room(3))