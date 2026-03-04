from fastapi import FastAPI, Request

# Initialize the FastAPI app
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


@app.get("/members/{crew_id}")
async def read_crew_member(crew_id: int):
    for member in crew:
        if member['id'] == crew_id:
            return member
    return {"message": "Crew member not found"}

@app.post("/members/")
async def add_crew_member(req: Request):
    data = await req.json()
    name = data.get('name')
    role = data.get('role')
    
    new_id = max(person['id'] for person in crew) + 1 if crew else 1
    new_member = {"id": new_id, "name": name, "role": role}
    crew.append(new_member)
    
    return new_member

@app.put("/members/{crew_id}")
async def update_crew_member(crew_id: int, req: Request):
    data = await req.json()
    name = data.get('name')
    role = data.get('role')
    
    for member in crew:
        if member['id'] == crew_id:
            member['name'] = name
            member['role'] = role
            return member
            
    return {"message": "Crew member not found"}

@app.delete("/members/{crew_id}")
async def delete_crew_member(crew_id: int):
    for i, member in enumerate(crew):
        if member['id'] == crew_id:
            removed_member = crew.pop(i)
            return {"message": f"Crew member {removed_member['name']} removed successfully"}
            
    return {"message": "Crew member not found"}
