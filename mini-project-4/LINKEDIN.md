Just wrapped up my latest backend project: a Real-Time Polling Dashboard built entirely with FastAPI and WebSockets.

Instead of using standard REST APIs where users have to constantly refresh their browser to see new votes, I used WebSockets. This allows the server to keep a persistent connection open and instantly push new vote counts to everyone the second a vote is cast. The difference in the user experience is huge.

The biggest technical challenge I ran into was handling sudden client drop-offs. If a user closed their browser while a vote was processing, the app would try to broadcast to a dead connection and crash. I fixed this by building a custom ConnectionManager that catches disconnect exceptions and safely cleans up inactive clients before sending out updates.

You can check out the demo below to see the cross-tab synchronization in action, or view the code on my GitHub.

[https://github.com/aledrisy/fastapi_journey/tree/aledrisy-mini-project-4](https://github.com/aledrisy/mfastapi_journey/tree/aledrisy-mini-project-4) 

[demo.mov]

#FastAPI #WebSockets #BackendDevelopment #Python #100DaysOfCode
