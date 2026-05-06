# LinkedIn Post

**Post Text:**
Just completed my latest project: a Real-Time Polling Dashboard built with FastAPI and WebSockets! 🚀 

Unlike traditional REST APIs where you have to constantly refresh the page to see new votes (polling), WebSockets allow the server to push updates to all connected clients instantly. The result? A true real-time experience! ✨ 

One technical challenge I faced was managing active connections cleanly. If a user closed their browser mid-vote, the app could crash trying to send data to a dead connection. I solved this by implementing a custom `ConnectionManager` class that catches `WebSocketDisconnect` exceptions and gracefully removes inactive clients before broadcasting updates.

Check out my GitHub repository to see the code or watch the attached demo to see real-time cross-tab updates in action!

[Link to GitHub Branch] / [Demo GIF]

#FastAPI #WebSockets #BackendDevelopment #100DaysOfCode #Python #RealTime

**Public URL:** 
[To be added by user after publishing]
