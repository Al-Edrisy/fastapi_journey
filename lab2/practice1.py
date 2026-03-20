from fastapi import FastAPI, Request

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]

@app.post("/crew")
async def add_crew(req: Request):
    data = await req.json()
    name = data.get('name')
    role = data.get('role')
    new_id = max(person['id'] for person in crew) + 1 if crew else 1
    new_member = {"id": new_id, "name": name, "role": role}
    crew.append(new_member)
    
    return new_member

@app.post("/add_crew/")
async def create_crew_member(req: Request):
    data = await req.json()
    name = data.get('name')
    role = data.get('role')
    
    new_id = max(person['id'] for person in crew) + 1 if crew else 1
    new_member = {"id": new_id, "name": name, "role": role}
    crew.append(new_member)
    
    return new_member
