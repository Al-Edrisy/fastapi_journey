# Design Decisions

1. **Connection Management** — How does your connection manager track connected clients? What happens if a client disconnects mid-vote? Does your app handle this gracefully, or does it crash?
*Answer:* The `ConnectionManager` class maintains a dictionary mapping `poll_id` to a list of active `WebSocket` objects. When a client connects, their socket is appended to the respective poll's list. If a client disconnects unexpectedly, a `WebSocketDisconnect` exception is caught, and the `disconnect` method is called to safely remove the socket from the list without crashing the server.

2. **State Storage** — You are storing vote counts in memory. Why did you choose this over writing votes to a database? What breaks if you restart the server? What would need to change to make this production-ready?
*Answer:* In-memory storage (a Python dictionary) was chosen for simplicity and low latency for this mini-project, as real-time interaction was the primary goal. However, if the server restarts, all polls and vote data are lost. To make this production-ready, I would implement a persistent database (e.g., PostgreSQL or Redis) to ensure state survives server restarts.

3. **Concurrency** — What would happen if two users voted at exactly the same moment? Did you handle this in your implementation? If not, what is the risk?
*Answer:* Because FastAPI runs asynchronously, standard dictionary operations in Python (like incrementing an integer in our votes dictionary) are generally thread-safe within a single event loop. However, in a multi-worker production environment, a race condition could occur if two requests modify the same poll simultaneously. In a real-world scenario, using a database with row-level locks or atomic increments (like Redis `INCR`) would prevent this risk.

4. **REST vs WebSocket** — You now have two ways to vote: `POST /polls/{id}/vote` and the WebSocket. What is the key difference in behavior between them? When would a client prefer one over the other?
*Answer:* The REST endpoint is a traditional, stateless request-response interaction: the client sends a vote, the server updates it and replies once, meaning the client won't know if someone else votes unless they poll again. The WebSocket connection remains open, allowing the server to actively push new vote counts to the client the moment any vote happens. A client would prefer REST for a quick, one-off vote if they don't care about seeing live results, but would strongly prefer WebSockets for an interactive, live dashboard experience.
