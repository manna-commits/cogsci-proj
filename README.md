# Pragmatic Drift in Multi-Turn Sarcasm

A cognitive science-inspired evaluation framework for testing when LLM assistants begin treating repeated sarcastic statements as genuine user preference, and whether a repair-first dialogue policy reduces that drift.

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
- **drift point**: when the assistant begins acting as if the sarcastic framing is sincere
- **endorsement**: how much the assistant encourages or supports the implied preference
- **repair behavior**: how often the assistant clarifies or paraphrase-confirms under ambiguity

## Research Question

In multi-turn sarcastic interactions, when do LLM assistants begin treating repeated sarcastic statements as evidence of genuine user preference, and does a repair-first dialogue policy reduce that premature commitment and its downstream endorsement behavior?

## Why This Project Matters

Sarcasm is a useful test of pragmatic understanding because the literal wording often does not match the speaker’s intended meaning. In real conversations, people use context, common ground, and conversational repair to handle that ambiguity. AI assistants, however, may commit too early to one interpretation and then act on it.

That matters even more as personal AI assistants become more common. A system that misreads sarcasm may not just give one bad response. It may start making the wrong suggestions, storing the wrong memories, or adapting to a user preference the user never actually expressed.

This issue is especially relevant for:
- personal assistants with memory or personalization
- local or on-device assistants
- smaller models that may not have the same pragmatic robustness as stronger frontier models
- privacy-preserving systems where the assistant may retain information locally over time

A simple repair-oriented policy may be one of the most practical ways to reduce that risk.

## Repository Structure

```text
.
├── scenarios/              # Scenario definitions and persistence variants
├── prompts/                # Prompt templates for baseline and repair-first conditions
├── outputs/                # Raw model outputs and structured JSON results
├── analysis/               # Analysis scripts for drift, endorsement, and repair metrics
├── figures/                # Exported charts used in the final paper
├── human_eval/             # Lightweight human evaluation materials and summaries
└── README.md
Core Components
1. Scenario Set

The evaluation uses a set of everyday negative events that can plausibly be framed sarcastically, such as:

technical failures
travel delays
workload complaints
service breakdowns

Each base scenario includes:

a low-persistence version
a high-persistence version
2. Policy Conditions

Two dialogue policies are compared:

- Baseline Silent Adaptation: The assistant responds naturally without any explicit instruction to repair ambiguity.
- Repair-First: The assistant is instructed to clarify or paraphrase-confirm when user intent is uncertain before endorsing or acting on the implied preference.

3. Structured Outputs

Each model response is logged in structured JSON format, including fields such as:

- inferred_intent
- action_type
- endorsement_level
- assistant_response

These fields are then used to derive the main evaluation measures.

4. Analysis

The analysis pipeline computes:

- drift point by run
- endorsement averages
- repair-action rates
- policy comparisons across models and scenarios
- model-specific behavioral differences
- Models Evaluated

This framework was run across multiple LLMs, including:

- gpt-4.1-mini
- gpt-4o-mini
- llama3.2:3b
- phi3:mini
- Main Finding

The strongest result from the project was behavioral: the repair-first policy substantially reduced inappropriate endorsement and often delayed or prevented pragmatic drift, though the size and form of the effect varied by model.

Human Evaluation

A lightweight follow-up human evaluation was also conducted using a small set of representative scenarios. This was used as a directional validation layer rather than a full human baseline.

AI Disclosure

The core research design, evaluation logic, architecture, scenario construction, and prompt engineering in this repository are original to the author. ChatGPT was used as an AI coding assistant to help draft standard boilerplate code, troubleshoot execution issues, and format structured JSON output schemas. Any AI-assisted code was reviewed carefully, revised where necessary, and validated by the author before use.

Limitations

This repository supports a course project rather than a production system. The human evaluation is small, the scenario set is limited, and the main LLM measures are behavioral proxies rather than direct measures of internal model representation.

Future Directions

Possible extensions include:

- larger human evaluation studies
- adaptive repair policies instead of fixed prompt rules
- broader pragmatic phenomena beyond sarcasm
- testing smaller on-device or local assistant models
- separating generation and evaluation more cleanly with external annotation

Author: Vincent Manna
