# Design Decisions

1. Connection Management
I used a ConnectionManager class with a dictionary that maps each poll ID to a list of active websocket connections. If a client drops out mid-vote, the app catches the WebSocketDisconnect error and removes that specific socket from the list so the server does not crash.

2. State Storage
I stored the votes in a Python dictionary in memory. I chose this because it is fast and simple to set up for a small real-time app. The downside is that if the server restarts, all the polls and votes disappear. For a real production app, I would need to write the votes to a database like PostgreSQL or Redis so the data is saved permanently.

3. Concurrency
Because FastAPI uses an asynchronous event loop, simply adding to a dictionary is generally safe here. However, if two users vote at the exact same millisecond in a multi-worker setup, there is a small chance of a race condition where a vote could be missed. To fix this properly, I would use database locks or atomic counters.

4. REST vs WebSocket
The REST voting endpoint is a one-way street: the user sends a vote and gets a single response back, but they have no idea what other users are doing. The WebSocket keeps the connection open. This means the server can instantly push updates to the user whenever anyone else votes. WebSockets are much better for live dashboards, while REST is fine if you only need to submit data once without needing live feedback.
