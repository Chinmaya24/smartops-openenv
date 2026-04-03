---
title: SmartOps OpenEnv
emoji: ??
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---
$meta = "---`ntitle: SmartOps OpenEnv`nemoji: 🤖`ncolorFrom: blue`ncolorTo: purple`nsdk: docker`npinned: false`nlicense: mit`n---`n"
$content = Get-Content README.md -Raw
$meta + $content | Set-Content README.md
(Get-Content README.md) | Out-File README_backup.md
"---
title: SmartOps OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---
" + (Get-Content README.md -Raw) | Set-Content README.md
# SmartOps OpenEnv 🚀

## 🔍 Overview

SmartOps OpenEnv is a real-world AI-powered operations environment that simulates how organizations automatically process incoming emails, detect urgency, and recommend actions.

It follows the OpenEnv standard (`step() / reset() / state()`) and integrates with workflow automation using n8n to demonstrate end-to-end intelligent operations.

---

## 🎯 Problem Solved

Organizations receive large volumes of emails such as:

* Support requests
* Urgent incident alerts
* Billing issues
* General inquiries

Manually processing these is slow and error-prone.

👉 SmartOps automates this entire pipeline:

* Understand email content
* Detect urgency
* Recommend next actions
* Trigger automated workflows

---

## ⚙️ System Architecture

### Core Components

1. **OpenEnv FastAPI Environment**

   * Implements:

     * `POST /reset`
     * `POST /step`
     * `GET /state`
     * `POST /process-email`
   * Deployed on Hugging Face Spaces

2. **AI Task Engine**

   * Email Classification
   * Urgency Detection
   * Action Recommendation

3. **Grader System**

   * Evaluates outputs with scores between `0.0 – 1.0`

4. **n8n Automation Layer**

   * Connects real-world inputs (Gmail)
   * Triggers AI processing
   * Automates responses/actions

---

## 🔄 End-to-End Workflow (n8n Integration)

Using n8n, SmartOps becomes a real automation system:

### Flow:

Gmail API / Trigger
↓
Extract email + sender
↓
HTTP Request (to OpenEnv API)
↓
AI Processing (`/process-email`)
↓
Receive:

* category
* urgency
* recommended_action
  ↓
  Automated Action:
* Send reply
* Trigger alert
* Create task

---

## 📧 Example Workflow

### Input Email:

"URGENT: Server is down, fix immediately"

### Output:

```json
{
  "category": "incident",
  "urgency": "high",
  "recommended_action": "escalate_to_engineering"
}
```

### Automated Action (via n8n):

* Send Slack alert 🚨
* Notify engineering team
* Create incident ticket

---

## 🧪 OpenEnv API

### `POST /reset`

Resets environment state

### `POST /step`

```json
{
  "action": "process_email"
}
```

Returns:

```json
{
  "observation": "...",
  "reward": 0.8,
  "done": false
}
```

### `GET /state`

Returns current environment state

### `POST /process-email`

Processes raw email input

---

## 📊 Tasks Implemented

1. **Email Classification (Easy)**
2. **Urgency Detection (Medium)**
3. **Action Recommendation (Hard)**

Each task:

* Has input/output examples
* Includes grader functions
* Returns scores in `[0.0, 1.0]`

---

## 🎯 Reward Function

* Based on correctness of predictions
* Partial rewards for partially correct outputs
* Normalized between `0.0 – 1.0`

---

## 🤖 Inference Pipeline

The `inference.py` script:

* Calls deployed API
* Runs all tasks
* Produces structured logs:

```
[START]
[STEP] task=email_classification score=1.0
[STEP] task=urgency_detection score=1.0
[STEP] task=action_recommendation score=1.0
[END]
```

---

## 🚀 Deployment

* Hosted on Hugging Face Spaces
* Dockerized FastAPI app
* Compatible with:

  * 2 CPU
  * 8GB RAM

---

## 🔐 Environment Variables

* `API_BASE_URL` – API endpoint
* `MODEL_NAME` – model used for inference
* `HF_TOKEN` – API key

---

## 🐳 Setup Instructions

```bash
docker build -t smartops-openenv .
docker run -p 7860:7860 smartops-openenv
```

---

## 🔗 Live Deployment

👉 https://chinu248-smartops-openenv-final.hf.space

---

## 🧠 Key Highlights

* Real-world AI operations system
* Fully OpenEnv compliant
* End-to-end automation using n8n
* Scalable and extensible architecture
* Demonstrates AI + workflow integration

---

## 🏁 Conclusion

SmartOps OpenEnv goes beyond a simulation by combining:

* AI decision-making
* structured environments
* real-world automation

It showcases how intelligent agents can operate in production-like workflows and make meaningful decisions autonomously.

