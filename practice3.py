from fastapi import FastAPI

app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]

@app.delete("/delete_member/{crew_id}")
def delete_member(crew_id: int):
    for i, member in enumerate(crew):
        if member['id'] == crew_id:
            del crew[i]
            return {"message": f"Crew member with ID {crew_id} has been deleted"}
            
    return {"message": "Crew member not found"}
