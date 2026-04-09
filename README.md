---
title: SmartOps OpenEnv
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

<div align="center">

# 🚀 SmartOps OpenEnv

### AI Multi-Agent Customer Support Environment

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compliant-blue?style=for-the-badge)](https://github.com/meta-pytorch/OpenEnv)
[![HuggingFace](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow?style=for-the-badge)](https://huggingface.co/spaces/chinu248/smartops-openenv-final)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A production-ready reinforcement learning environment for AI-powered email operations**

[🌐 Live Demo](https://chinu248-smartops-openenv-final.hf.space) • [📖 API Docs](https://chinu248-smartops-openenv-final.hf.space/docs) • [💻 GitHub](https://github.com/Chinmaya24/smartops-openenv)

</div>

---

## 🎯 Overview

SmartOps OpenEnv is a **real-world AI operations environment** that simulates how organizations automatically process incoming emails using a **multi-agent architecture** with reinforcement learning.

Built for the **Meta × Hugging Face OpenEnv Hackathon**, it demonstrates:
- 🤖 Multi-agent collaboration (Triage → Response → Escalation)
- 🎯 Reward-based evaluation with partial progress signals
- ⚙️ Full OpenEnv spec compliance (`reset()` / `step()` / `state()`)
- 🔄 End-to-end automation with Gmail + n8n integration

---

## 🏗️ System Architecture

```
📧 Incoming Email
       │
       ▼
┌─────────────────┐
│  Gmail Trigger  │  ← n8n Automation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP Request   │  ← POST /process-email
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│           SmartOps OpenEnv              │
│                                         │
│  🧠 Triage Agent → classifies + urgency │
│         ↓                               │
│  💬 Response Agent → generates reply    │
│         ↓                               │
│  🚨 Escalation Agent → priority flag   │
│         ↓                               │
│  📊 Reward Grader → scores 0.0–1.0     │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   Gmail Send    │  ← AI-powered reply
└─────────────────┘
```

---

## 🤖 Agents

| Agent | Role | Output |
|-------|------|--------|
| 🧠 **Triage Agent** | Classifies email + assigns urgency | `category`, `urgency` |
| 💬 **Response Agent** | Generates professional reply | `response` |
| 🚨 **Escalation Agent** | Decides escalation + priority | `escalated`, `priority` |

---

## 📊 Tasks & Benchmark Scores

| Task | Difficulty | Score |
|------|-----------|-------|
| 📧 Email Classification | 🟢 Easy | **0.9000** |
| ⚡ Urgency Detection | 🟡 Medium | **0.9000** |
| 🎯 Action Recommendation | 🔴 Hard | **0.9000** |
| | **Average** | **0.9000** ✅ |

---

## 🎯 Reward Function

```
score = category_match (0.4)
      + response_keywords (0.3)
      + escalation_correctness (0.2)
      + priority_correctness (0.1)
      - inefficiency_penalty (step_count > 4)
```

Scores normalized to the open interval `(0.0, 1.0)` with partial progress signals at each step.

---

## 🌐 API Reference

### `POST /reset`
Resets environment for new episode.
```json
{"observation": "ready", "reward": 0.0, "done": false}
```

### `POST /step`
Execute agent action.
```json
{"action": "triage"}
```
Returns: `{"observation": "...", "reward": 0.3, "done": false}`

### `GET /state`
Current environment state.

### `POST /process-email`
End-to-end email processing.
```json
{
  "subject": "URGENT: Website is down",
  "body": "We are losing money every minute!",
  "customer_tier": "premium"
}
```
Returns:
```json
{
  "category": "technical",
  "urgency": 5,
  "response": "We are aware of the issue and fixing it urgently.",
  "escalated": true,
  "priority": 5,
  "score": 0.85
}
```

---

## 🔄 n8n Automation Integration

SmartOps connects to real-world Gmail via n8n:

```
Customer Email → Gmail Trigger → HTTP Request → AI Processing → Gmail Reply
```

✅ Fully automated — zero human interaction required.

---

## 🧪 Inference Pipeline

```bash
python inference.py
```

Output:
```
[START]
[STEP] task=email_classification score=0.9
[STEP] task=urgency_detection    score=0.9
[STEP] task=action_recommendation score=0.9
[END]
```

---

## 🚀 Quick Start

### Run locally
```bash
pip install -r requirements.txt
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Run with Docker
```bash
docker build -t smartops-openenv .
docker run -p 7860:7860 smartops-openenv
```

### Run baseline benchmark
```bash
python scripts/run_baseline.py
```

---

## 📁 Project Structure

```
smartops-openenv/
├── server/
│   └── app.py          ← FastAPI OpenEnv server
├── agents/
│   ├── triage.py       ← Classification + urgency
│   ├── response.py     ← Reply generation
│   └── escalation.py   ← Priority decisions
├── tasks/
│   ├── email_classification.py
│   ├── urgency_detection.py
│   └── action_recommendation.py
├── env/
│   ├── smart_ops_env.py ← OpenEnv core
│   ├── models.py        ← Typed models
│   └── graders.py       ← Reward system
├── scripts/
│   └── run_baseline.py  ← Benchmark runner
├── inference.py         ← Inference script
├── openenv.yaml         ← OpenEnv manifest
└── Dockerfile           ← HF Spaces deployment
```

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + Uvicorn |
| Environment | OpenEnv Core |
| RL | Stable-Baselines3 (PPO) |
| Automation | n8n + Gmail API |
| Deployment | Hugging Face Spaces |
| Container | Docker |

---

## 🏆 Why SmartOps Stands Out

- ✅ **Real-world use case** — not a toy or game
- ✅ **Full OpenEnv compliance** — spec_version 1
- ✅ **Strong benchmark scores** — strictly within (0,1) on all tasks
- ✅ **Production deployment** — live on HF Spaces
- ✅ **End-to-end automation** — Gmail → AI → Reply
- ✅ **Multi-agent architecture** — 3 specialized agents
- ✅ **RL-ready** — PPO training with reward shaping

---

## 👨‍💻 Author

Built with ❤️ for the **Meta × Hugging Face OpenEnv Hackathon**

[![GitHub](https://img.shields.io/badge/GitHub-Chinmaya24-181717?style=for-the-badge&logo=github)](https://github.com/Chinmaya24)

---

<div align="center">
⭐ Star this repo if you found it useful!
</div>