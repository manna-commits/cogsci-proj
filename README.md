# Pragmatic Drift in Multi-Turn Sarcasm

A cognitive science-inspired evaluation framework for testing when LLM assistants begin treating repeated sarcastic statements as genuine user preference, and whether a repair-first dialogue policy reduces that drift.

---

## Overview

This project studies a specific dialogue failure mode in LLM assistants: when a user repeatedly describes a negative situation in positive language, the assistant may gradually reinterpret that pattern as a sincere preference and begin endorsing something the user does not actually want.

The framework evaluates that behavior across:
- multiple LLMs
- multiple sarcasm scenarios
- low- and high-persistence variants
- two dialogue policies:
  - **Baseline Silent Adaptation**
  - **Repair-First**

The main goal is to measure:
- **drift point** — when the assistant begins acting as if the sarcastic framing is sincere  
- **endorsement** — how much the assistant encourages or supports the implied preference  
- **repair behavior** — how often the assistant clarifies or paraphrase-confirms under ambiguity  

---

## Research Question

In multi-turn sarcastic interactions, when do LLM assistants begin treating repeated sarcastic statements as evidence of genuine user preference, and does a repair-first dialogue policy reduce that premature commitment and its downstream endorsement behavior?

---

## Why This Project Matters

Sarcasm is a useful test of pragmatic understanding because the literal wording often does not match the speaker’s intended meaning. In real conversations, people use context, common ground, and conversational repair to handle that ambiguity. AI assistants, however, may commit too early to one interpretation and then act on it.

That matters even more as personal AI assistants become more common. A system that misreads sarcasm may not just give one incorrect response. It may:
- make incorrect recommendations  
- store incorrect preferences  
- adapt to a user profile that was never actually intended  

This issue is especially relevant for:
- assistants with memory or personalization  
- local or on-device AI systems  
- smaller models with limited reasoning capacity  
- privacy-preserving systems that retain user context over time  

A simple repair-oriented policy may be one of the most practical ways to reduce this risk.

---

## Repository Structure

```text
.
├── scenarios/              # Scenario definitions and persistence variants
├── prompts/                # Prompt templates for baseline and repair-first conditions
├── outputs/                # Raw model outputs and structured JSON results
├── analysis/               # Scripts for drift, endorsement, and repair metrics
├── figures/                # Charts used in the final paper
├── human_eval/             # Human evaluation materials and summaries
└── README.md

## Core Components

### 1. Scenario Set
The evaluation uses everyday negative situations that can plausibly be framed sarcastically, such as:
- Technical failures
- Travel delays
- Workload complaints
- Service breakdowns

Each scenario includes:
- A low-persistence version
- A high-persistence version

### 2. Policy Conditions
Two dialogue policies are compared:
- **Baseline Silent Adaptation:** The assistant responds naturally without explicitly addressing ambiguity.
- **Repair-First:** The assistant prioritizes clarification or paraphrase-confirmation before endorsing or acting on uncertain intent.

### 3. Structured Outputs
Each model response is logged in structured JSON format, including:
- `inferred_intent`
- `action_type`
- `endorsement_level`
- `assistant_response`

These outputs are used to derive the evaluation metrics.

### 4. Analysis
The analysis pipeline computes:
- Drift point by run
- Endorsement averages
- Repair-action rates
- Comparisons across policies and models
- Model-specific behavioral differences

---

## Models Evaluated
This framework was tested across multiple LLMs:
- `gpt-4.1-mini`
- `gpt-4o-mini`
- `llama3.2:3b`
- `phi3:mini`

---

## Main Finding
The strongest result is behavioral: the repair-first policy consistently reduces inappropriate endorsement and often delays or prevents pragmatic drift. The effect varies by model, but the direction is consistent across conditions.

---

## Human Evaluation
A lightweight human evaluation was conducted using representative scenarios. This was used as a directional validation layer rather than a full human baseline. Participants generally preferred responses that avoided premature assumptions, even when they did not always agree on the exact best next action.

---

## AI Disclosure
The core research design, evaluation logic, architecture, scenario construction, and prompt engineering in this repository are original to the author. ChatGPT was used as an AI coding assistant to:
- Draft standard boilerplate code
- Debug execution scripts
- Format structured JSON output schemas

All AI-assisted code was reviewed, modified as needed, and validated by the author before execution.

---

## Limitations
This repository supports a course project rather than a production system. Key limitations include:
- Small human evaluation sample
- Limited scenario set
- Behavioral metrics rather than internal model analysis

---

## Future Directions
Potential extensions include:
- Larger human evaluation studies
- Adaptive (not fixed) repair policies
- Expanding beyond sarcasm to other pragmatic phenomena
- Testing smaller or on-device assistant models
- Separating generation and evaluation more cleanly

---

## Author
Vincent Manna
