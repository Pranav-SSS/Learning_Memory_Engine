# Learning Memory Engine

A **memory-aware, adaptive learning system** that models how students *learn, forget, and improve* over time using **vector databases, cognitive decay, and lightweight reinforcement learning**.

This project was built as a **hackathon-ready, research-inspired system** focusing on *correctness, explainability, and personalization* rather than heavy training pipelines.

---

## 🎯 Problem Statement

Most learning platforms:

* Assume all learners forget at the same rate
* Use static difficulty progression

**Learning Memory Engine** addresses this by explicitly modeling:

* Long-term student memory
* Forgetting over time
* Learning confidence and stability
* Adaptive teaching decisions

---

## 🧠 High-Level Idea

The system treats **learning as a dynamic process**:

1. Knowledge is stored semantically (vector database)
2. Each student has evolving memory per concept
3. Memory decays over time (spaced repetition)
4. Learning updates are non-linear
5. Reinforcement Learning chooses teaching strategy

All decisions are **interpretable and online**.

---

## 🏗️ System Architecture Overview

```
+-------------------+
|   Student Query   |
+-------------------+
          |
          v
+-------------------+
| Student Memory DB |
|   (Qdrant)        |
+-------------------+
          |
          v
+-------------------+      +----------------------+
| RL Policy (Bandit)| ---> | Teaching Strategy    |
+-------------------+      +----------------------+
          |
          v
+-------------------+
| Knowledge DB      |
| (Semantic Search) |
+-------------------+
          |
          v
+-------------------+
| Answer + Feedback |
+-------------------+
```

---

## 📦 Core Components

### 1️⃣ Knowledge Memory (Global)

* Educational content is chunked and embedded using **Sentence Transformers**
* Stored in **Qdrant** as semantic vectors
* Retrieved via similarity search with difficulty filtering

**Purpose:** Provide grounded, relevant learning content

---

### 2️⃣ Student Memory (Personalized)

Each student–concept pair stores:

| Field     | Meaning                     |
| --------- | --------------------------- |
| mastery   | Current understanding (0–1) |
| stability | Resistance to forgetting    |
| mistakes  | Repeated error patterns     |

This memory evolves after every interaction.

---

## ⏳ Forgetting Model (Spaced Repetition)

We use a **stability-based decay function** inspired by cognitive science:

```
mastery = mastery × exp(-days_passed / stability)
```

* **Low stability** → fast forgetting
* **High stability** → slow forgetting

### Stability Update Rule

* Correct recall → stability increases
* Incorrect recall → stability decreases slightly

This mimics human long-term retention.

---

## 📈 Learning Model (Non-Linear Mastery)

Learning updates follow three principles:

1. **Diminishing returns** — learning slows near mastery
2. **Confidence-aware** — stable memories learn faster
3. **Error sensitivity** — mistakes hurt more at high mastery

This avoids unrealistic linear learning curves.

---

## 🎯 Reinforcement Learning (Adaptive Teaching)

Instead of training heavy RL models, we use a **Contextual Multi-Armed Bandit**.

### RL Design

| Element | Description                                  |
| ------- | -------------------------------------------- |
| State   | (mastery, stability)                         |
| Actions | explanation, example, practice, prerequisite |
| Reward  | Change in mastery                            |
| Policy  | ε-greedy (online)                            |

The system **learns which teaching strategy works best** per student and concept.

---

## 🔁 End-to-End Workflow

```
1. Student answers question
2. Apply time-based decay
3. Update mastery & stability
4. RL selects teaching action
5. Retrieve relevant knowledge
6. Generate grounded response
7. Store updated memory
```

This loop repeats for every interaction.

---

## 🔍 Explainability

Every decision is transparent:

* Why a concept was retrieved
* Why a teaching strategy was chosen
* Why mastery changed

No black-box learning.

---

## 🧪 Demo Execution Flow

Running `main.py` demonstrates:

* Memory decay over time
* Mastery updates after mistakes
* RL strategy selection
* Semantic retrieval from Qdrant
* Personalized recommendation

Demo is deterministic using:

```python
random.seed(42)
```

---

## ▶️ How to Run

### 1️⃣ Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 2️⃣ Install dependencies

```bash
pip install qdrant-client sentence-transformers tf-keras
```

### 3️⃣ Run the system

```bash
python main.py
```

---

## 🧠 Why This System Stands Out

* Models **learning over time**, not single interactions
* Combines **vector search + cognition + RL**
* Fully online and adaptive
* Interpretable at every step
* No heavy training or black-box models

---

## 🏁 Project Status

✅ Core system complete
✅ Demo stable and reproducible
✅ Ready for submission and evaluation

---

## 👤 Author

**Satyagari Sai Sree Pranav**

---

> *“Learning is not remembering once — it is remembering over time.”*
