from fastapi import FastAPI, Request

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


@app.put("/update_crew/{crew_id}")
async def update_crew(crew_id: int, req: Request):
    data = await req.json()
    name = data.get('name')
    role = data.get('role')
    
    for member in crew:
        if member['id'] == crew_id:
            member['name'] = name
            member['role'] = role
            return member
            
    return {"message": "Crew member not found"}


