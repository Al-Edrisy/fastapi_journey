# SFWE477 — Docker Lab 2: First Steps with Kubernetes 🚢

Welcome to **Docker Lab 2** for **SFWE477**.  
In this lab you will install Minikube on your local machine, spin up your first Kubernetes cluster, deploy pods using images you already know, and observe how Kubernetes manages container lifecycles — all documented with screenshots.

---

## 📁 Repository Setup

1. Use the same **`SFWE477-labs`** repository from Lab 1
2. Create a **new branch** for this lab following the naming policy below
3. Your submission must live in a folder named **`docker-lab-2/`** at the root of your repo

---

## 🌿 Branch Naming Policy

Branch names follow this format:

```
firstinitial+surname-docker-lab-2
```

**Example:** John Snow → `jsnow-docker-lab-2`

> ⚠️ Do not work on `main`. No spaces or capital letters in branch names.

```bash
git checkout -b jsnow-docker-lab-2
```

---

## 🖼️ Image Assignments

You will use the **same image assigned to you in Docker Lab 1**. Look up your image in the Lab 1 assignment table. If you are unsure, ask your instructor.

| Image | Assigned students |
|---|---|
| 🐍 `python:3.12-slim` | MOHAMMED AL-JABERI · SELİN TÜRKDOĞAN · GAYE İLERİ · GERMAN RACHKOV · DOĞANCAN YILMAZER |
| 🌐 `nginx:alpine` | SALIH OTMAN · SÜLEYMAN ŞAHAL · MOUNCIF BELRHRIB · NIKITA IGNATEV · HAYTAM CHARAFI |
| 🐘 `postgres:16-alpine` | ALİM ÖZTÜRK · HAYRUNNİSA İYİKÖŞKER · MERYEM BALILI · AHMED SULTAN · ALEYA KEWSEEDIN |
| 🏔️ `alpine:3.19` | BELLY SABUSHIMIKE · POLINA ZIMINA · AYYOUB ASRI · SALOUA OURICH · ABDULLAH GHANEM · AHMET ŞENEL |

---

## 🛠️ Prerequisites

Before starting the lab tasks, make sure you have:

- Docker Desktop installed and **running** (from Lab 1)
- WSL 2 enabled on Windows
- An internet connection to download Minikube

> ⚠️ Minikube uses Docker Desktop as its driver. Docker Desktop **must be running** before you start any Minikube commands.

---

## ✅ Lab Tasks

---

### Task 1 — Install Minikube

Open **PowerShell as Administrator** and run:

```powershell
# Install Minikube using winget
winget install Kubernetes.minikube

# Verify the installation
minikube version
```

**Screenshot required:** `minikube version` output showing the installed version.

> If `winget` is not available on your machine, download the Minikube installer directly from:  
> `https://minikube.sigs.k8s.io/docs/start/`  
> Choose: Windows / x86-64 / Stable / .exe download

---

### Task 2 — Start your first Kubernetes cluster

```bash
# Start Minikube using Docker as the driver
minikube start --driver=docker

# This will take 1–2 minutes the first time — Minikube downloads Kubernetes components
```

**Screenshot required:** full terminal output of `minikube start`, including the final "Done!" or status lines.

```bash
# Verify the cluster is running
kubectl cluster-info

# List the nodes in your cluster
kubectl get nodes
```

**Screenshot required:**
- `kubectl cluster-info` output
- `kubectl get nodes` output — confirm your node shows `Ready` in the STATUS column

---

### Task 3 — Explore the cluster

```bash
# Check what is running inside the cluster by default
kubectl get pods --all-namespaces

# Look at the system namespace specifically
kubectl get pods -n kube-system
```

**Screenshot required:** `kubectl get pods -n kube-system` — you should see the core control plane components listed as pods.

Answer in your `OBSERVATIONS.md`: What components do you see running in `kube-system`? Can you identify any components from the lecture (scheduler, etcd, api-server)?

---

### Task 4 — Deploy your assigned image as a pod

Replace `<your-image>` with your assigned image from the table above.

```bash
# Deploy your image as a pod
kubectl run my-pod --image=<your-image>

# Watch the pod status — run this a few times as it starts up
kubectl get pods

# Get full details about your pod
kubectl describe pod my-pod
```

**Screenshot required:**
- `kubectl get pods` showing your pod in `Running` state
- `kubectl describe pod my-pod` — scroll to show the **Events** section at the bottom

Answer in your `OBSERVATIONS.md`: In the Events section of `kubectl describe`, what sequence of events happened before the pod started running? Which component scheduled the pod?

---

### Task 5 — Image-specific observation

Complete only the task for **your assigned image**:

---

#### 🏔️ If your image is `alpine:3.19`

Alpine exits immediately when run without a command, so you need to give it one to keep it alive:

```bash
# Delete the pod from Task 4 first
kubectl delete pod my-pod

# Re-run with a command that keeps it alive
kubectl run my-pod --image=alpine:3.19 -- sleep 3600

# Verify it stays Running
kubectl get pods

# Open an interactive shell INSIDE the running pod
kubectl exec -it my-pod -- sh

# Inside the pod:
cat /etc/os-release
hostname
exit
```

**Screenshot required:**
- `kubectl get pods` showing the pod in `Running` state
- Interactive shell session showing `cat /etc/os-release` output inside the pod

---

#### 🌐 If your image is `nginx:alpine`

```bash
# Your pod should already be running from Task 4
kubectl get pods

# Forward a local port to the pod's port 80
kubectl port-forward pod/my-pod 8080:80
```

Open `http://localhost:8080` in your browser **while the port-forward is running**.

**Screenshot required:**
- Browser showing the nginx welcome page at `localhost:8080`
- Terminal showing the port-forward output with the incoming request logged

```bash
# In a NEW terminal (keep the port-forward running in the first):
kubectl logs my-pod
```

**Screenshot required:** `kubectl logs my-pod` showing the HTTP access log entry from your browser visit.

---

#### 🐍 If your image is `python:3.12-slim`

Python also exits immediately without a command:

```bash
# Delete the pod from Task 4
kubectl delete pod my-pod

# Re-run with a sleep command to keep it alive
kubectl run my-pod --image=python:3.12-slim -- sleep 3600

kubectl get pods

# Open a Python shell inside the running pod
kubectl exec -it my-pod -- python3

# Inside the Python REPL:
import sys
print(sys.version)
import platform
print(platform.node())   # this prints the pod's hostname
exit()
```

**Screenshot required:** Python REPL session inside the pod — note that `platform.node()` returns the **pod name**, not your laptop's hostname.

Answer in your `OBSERVATIONS.md`: Why does `platform.node()` return the pod name? What does this tell you about container networking isolation?

---

#### 🐘 If your image is `postgres:16-alpine`

Postgres requires environment variables to start. You need to delete and recreate the pod:

```bash
# Delete the pod from Task 4 (it likely crashed — Postgres needs env vars)
kubectl delete pod my-pod

# Re-run with the required environment variable
kubectl run my-pod \
  --image=postgres:16-alpine \
  --env="POSTGRES_PASSWORD=mysecret" \
  --env="POSTGRES_DB=labdb"

# Watch it start — may take a few seconds
kubectl get pods

# Check the logs
kubectl logs my-pod
```

**Screenshot required:** `kubectl logs my-pod` showing `database system is ready to accept connections`.

```bash
# Connect to the database inside the pod
kubectl exec -it my-pod -- psql -U postgres -d labdb

# Inside psql:
\l
CREATE TABLE kube_test (id SERIAL, note TEXT);
INSERT INTO kube_test (note) VALUES ('running inside Kubernetes');
SELECT * FROM kube_test;
\q
```

**Screenshot required:** psql session showing the table creation and query result.

---

### Task 6 — Simulate a pod failure and observe self-healing

This task is the same for all students regardless of image.

```bash
# Check your pod is running
kubectl get pods

# Delete the pod — this simulates a crash
kubectl delete pod my-pod

# Immediately watch what happens
kubectl get pods
```

**Screenshot required:** `kubectl get pods` after deletion — the pod is gone. Note this result.

Answer in your `OBSERVATIONS.md`:
- After deleting the pod manually, did Kubernetes bring it back? Why or why not?
- What would need to be different (hint: think about what you'll learn in Lecture 4) for Kubernetes to automatically restart a deleted pod?

> This question has a deliberate answer: a standalone pod has no controller watching over it. You need a **Deployment** for self-healing. You'll build one in Lecture 4.

---

### Task 7 — Clean up

```bash
# Remove any remaining pods
kubectl delete pod my-pod --ignore-not-found

# Confirm clean state
kubectl get pods

# Stop the Minikube cluster
minikube stop

# Verify it stopped
minikube status
```

**Screenshot required:**
- `kubectl get pods` showing `No resources found`
- `minikube status` showing the cluster is stopped

---

## 📝 OBSERVATIONS.md

Create an `OBSERVATIONS.md` file inside `docker-lab-2/`. Answer all of the following in your own words:

1. What is the difference between running a container with `docker run` and deploying a pod with `kubectl run`? Both used the same image — what changed?
2. In `kubectl describe pod`, what is the role of the **Scheduler** event? Which control plane component does that correspond to?
3. In `kubectl get pods -n kube-system`, name two components you recognised from the lecture and describe what they do.
4. **Image-specific observation** (answer only the one relevant to your image):
   - 🏔️ Alpine: What happened to any changes you made inside the pod shell when you exited? Compare this to your experience in Docker Lab 1.
   - 🌐 Nginx: What does `kubectl port-forward` do, and why is it needed? Can you access the pod without it?
   - 🐍 Python: Why does `platform.node()` return the pod name? What does this tell you about how Kubernetes assigns identities to pods?
   - 🐘 Postgres: Why did the pod crash in Task 4 without environment variables? What does this tell you about how images communicate their requirements?
5. Task 6 reflection: After deleting the pod, Kubernetes did **not** restart it. In one paragraph, explain why, and what Kubernetes object would change this behaviour.

---

## 💾 How to Commit — One Task at a Time

```bash
# After Tasks 1–2 (Minikube install and cluster start)
git add docker-lab-2/screenshots/
git commit -m "docker-lab-2: minikube install and cluster start screenshots"

# After Tasks 3–4 (explore cluster and deploy pod)
git add docker-lab-2/screenshots/
git commit -m "docker-lab-2: cluster exploration and pod deployment screenshots"

# After Task 5 (image-specific)
git add docker-lab-2/screenshots/
git commit -m "docker-lab-2: image-specific task screenshots"

# After Tasks 6–7 and OBSERVATIONS.md
git add docker-lab-2/OBSERVATIONS.md
git add docker-lab-2/screenshots/
git commit -m "docker-lab-2: self-healing task, cleanup, and OBSERVATIONS.md"
```

Push your branch when done:

```bash
git push origin jsnow-docker-lab-2
```

---

## 📸 Screenshots

Store all screenshots in `docker-lab-2/screenshots/`. Use the naming format:

**`task<number>-<short-description>.png`**

```
docker-lab-2/
└── screenshots/
    ├── task1-minikube-version.png
    ├── task2-minikube-start.png
    ├── task2-get-nodes.png
    ├── task3-kube-system-pods.png
    ├── task4-pod-running.png
    ├── task4-describe-events.png
    ├── task5-image-specific.png
    ├── task6-pod-deleted.png
    └── task7-cleanup.png
```

> ⚠️ Screenshots must show your **full terminal window** — command typed and complete output visible. Partial or cropped screenshots will not be accepted.

---

## 📁 Expected Folder Structure

```
SFWE477-labs/
└── docker-lab-2/
    ├── OBSERVATIONS.md
    └── screenshots/
        └── task*.png  (one per required screenshot above)
```

---

## 📬 Submission

Push your branch and submit the branch URL on Moodle:

```
https://github.com/<your-username>/SFWE477-labs/tree/jsnow-docker-lab-2
```

---

## 🎯 Grading

Pass or Fail — full grade or nothing.

### ✅ To pass, all three criteria must be met:

| # | Criteria | Details |
|---|----------|---------|
| 1 | **All tasks completed** | All required screenshots present, correctly named, showing full terminal output |
| 2 | **Correct branch and commits** | Branch follows `jsnow-docker-lab-2` format, at least 4 commits — one per task group |
| 3 | **OBSERVATIONS.md is genuine** | Answers must reflect what you actually observed — vague or AI-sounding answers will not pass |

### ❌ You will automatically fail if:
- Any required screenshot is missing or cropped
- Task 6 OBSERVATIONS answer does not correctly explain why the pod was not restarted
- `OBSERVATIONS.md` is missing or generic
- All work is in a single commit
- Branch is incorrectly named or missing
- Submission link is not on Moodle before the deadline
