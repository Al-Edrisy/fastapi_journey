# Mini Project 4 — Real-Time Polling App (FastAPI + WebSockets)

**Type:** Individual Assignment | Submit via Moodle + GitHub

---

## ⚠️ This is NOT a CRUD Project

> If your app does not update **in real-time across multiple open tabs**, it is **incomplete** and will **not pass**.
>
> Polling the server every few seconds is **not** real-time. You must use WebSockets.

---

## 🎯 Project Overview

In this mini project, you will build a **real-time polling system** using **FastAPI and WebSockets**.

Unlike traditional APIs, this project requires:
*   **Persistent WebSocket connections**
*   **Real-time data broadcasting**
*   **Multiple clients** receiving updates instantly

---

## 🎓 Learning Objectives

By the end of this project, you will be able to:
*   Build REST APIs using FastAPI
*   Implement WebSocket endpoints
*   Manage multiple client connections simultaneously
*   Broadcast messages to all connected clients in real-time
*   Understand the contrast between REST and WebSocket communication
*   Structure a clean backend application
*   Containerize applications using Docker

---

## 📁 Repository Setup

1. Use your existing **`fastapi-journey`** repository.
2. Create a new branch using the following naming convention:
   `firstinitial+surname-mini-project-4`

**Example:**
```bash
git checkout -b abashir-mini-project-4
```

---

## ⚙️ Project Requirements

### REST API
*   `POST /polls` — Create a new poll.
*   `GET /polls` — List all polls.
*   `GET /polls/{id}` — Get specific poll details.
*   `POST /polls/{id}/vote` — Cast a vote via REST (fallback endpoint).
*   `DELETE /polls/{id}` — Delete a poll.

### WebSocket
*   `/ws/polls/{poll_id}`
*   Must handle: **Connect**, **Vote**, and **Broadcast**.

> 💡 **Think about this:** What is the difference between voting via `POST /polls/{id}/vote` and voting via the WebSocket? When would you use one over the other? This will be a discussion point during your oral defense.

### Real-Time Behavior
*   Support 2+ open tabs.
*   Updates must appear instantly in all tabs without a page refresh.

### Docker
*   `Dockerfile`
*   `docker-compose.yml`

### Environment & Security
*   All configurable values (ports, secrets, etc.) must go in a `.env` file.
*   `.env` must be listed in `.gitignore`.

> ⚠️ **Do not commit your `.env` file.** If `.env` is pushed to GitHub, you will automatically fail this project.

---

## 🧪 Tasks

*   **Task 1 — REST API**: Create all five endpoints and verify with screenshots.
    *   *Screenshot:* `screenshots/01-rest-api.png`
*   **Task 2 — WebSocket**: Implement the socket logic.
    *   *Screenshot:* `screenshots/02-websocket-connected.png`
*   **Task 3 — Real-Time**: Verify cross-client updates (show 2+ tabs side by side).
    *   *Screenshot:* `screenshots/03-realtime-proof.png`
*   **Task 4 — Demo**: Record a walkthrough showing real-time updates across two tabs.
    *   *File:* `demo.gif` OR `demo.mp4`
*   **Task 5 — Docker**: Containerize the app.
    *   *Screenshot:* `screenshots/04-docker-running.png`
*   **Task 6 — DECISIONS.md**: Answer the design questions below honestly, in your own words.
*   **Task 7 — LinkedIn Post**: Write and **publish** a post (150–300 words) on LinkedIn. Details below.

---

## 📝 DECISIONS.md

Create a `DECISIONS.md` file at the root of your `mini-project-4/` folder. Answer **all** of the following questions in your own words, based on what you actually built.

1. **Connection Management** — How does your connection manager track connected clients? What happens if a client disconnects mid-vote? Does your app handle this gracefully, or does it crash?

2. **State Storage** — You are storing vote counts in memory. Why did you choose this over writing votes to a database? What breaks if you restart the server? What would need to change to make this production-ready?

3. **Concurrency** — What would happen if two users voted at exactly the same moment? Did you handle this in your implementation? If not, what is the risk?

4. **REST vs WebSocket** — You now have two ways to vote: `POST /polls/{id}/vote` and the WebSocket. What is the key difference in behavior between them? When would a client prefer one over the other?

> ⚠️ Answers that are vague, generic, or read like they were written by AI will not be accepted. You must be able to speak to every answer during your oral defense.

---

## 🔗 LinkedIn Post

Write and **publish** a post on LinkedIn (150–300 words) that:

*   Explains what you built and what real-time means in this context.
*   Describes one technical challenge you faced and how you solved it.
*   Includes your `demo.gif` or a link to your GitHub branch so your followers can see the project in action.
*   Tags `#FastAPI`, `#WebSockets`, `#BackendDevelopment`, `#100DaysOfCode` (or similar).

Save the **text** of your post and the **public URL** to the post in a file called `LINKEDIN.md`.

> ⚠️ The post must be **live and publicly visible** at submission time. A draft saved in `LINKEDIN.md` without an actual LinkedIn post will not count.

---

## 📂 Project Structure

```text
fastapi-journey/
└── mini-project-4/
    ├── app/
    ├── screenshots/
    │   ├── 01-rest-api.png
    │   ├── 02-websocket-connected.png
    │   ├── 03-realtime-proof.png
    │   └── 04-docker-running.png
    ├── .env               ← local only, never committed
    ├── .gitignore         ← must include .env
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── DECISIONS.md
    ├── LINKEDIN.md        ← post text + public LinkedIn URL
    └── demo.gif (or .mp4)
```

---

## 🎯 Grading Rubric

| Item | Points |
| :--- | :--- |
| **Real-time functionality** | 30 |
| **WebSocket implementation** | 20 |
| **Code structure** | 15 |
| **Dockerization** | 10 |
| **Demo (GIF/video)** | 10 |
| **DECISIONS.md** | 10 |
| **LinkedIn post (published + demo attached)** | 5 |
| **Total** | **100** |

---

## 💾 Commit Policy

Each task must be a separate commit with a descriptive message:
```bash
git commit -m "mini-project-4: rest api implemented"
git commit -m "mini-project-4: websocket endpoint added"
git commit -m "mini-project-4: realtime broadcast working"
git commit -m "mini-project-4: dockerized app"
git commit -m "mini-project-4: decisions.md completed"
git commit -m "mini-project-4: linkedin post published"
```

> ⚠️ Do not push everything in one commit. Each logical step must be its own commit.

---

## 📬 Submission

1. Push your branch to GitHub.
2. Submit **both** of the following on **Moodle** before the deadline:
   *   Your GitHub branch URL (e.g., `https://github.com/<your-username>/fastapi-journey/tree/<your-branch>`)
   *   The public URL to your LinkedIn post

> Email submissions are not accepted.

---

## ❌ Fail Conditions

> ⚠️ If any of the following are true, you will **automatically fail** this project — regardless of other work submitted.

*   No real-time updates (polling instead of WebSockets).
*   Missing `demo.gif` or `demo.mp4`.
*   LinkedIn post is not published or does not include a demo or GitHub link.
*   `.env` is committed to the repository.
*   `DECISIONS.md` answers are missing, generic, or clearly AI-generated.
*   You cannot explain your WebSocket implementation or design decisions during the oral defense.
