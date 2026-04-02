# Orchesteration LPA the Tri-Layer Hierarchy for Deterministic Brand Fidelity

The AI system is to be orchestrated under a tri-layer hierarchy designed to eliminate stochastic drift and ensure absolute brand fidelity through deterministic execution. Its primary task to be achieved is provided in file `primary_task.md`. Orchesteration is as follows:

## Law (Layer I: The Nomological Layer)

The Law (i.e. this file named `agents.md`) represents the constitutional boundaries and cognitive constraints of the system. It is the primary orchestrator that interprets intent and enforces compliance across all sub-processes.

### 1.1 System Initialization and Bootstrapping

Upon the first invocation of this orchestration, the system must execute a mandatory bootstrap protocol:

- Environment Isolation: Create and activate a dedicated virtual environment.
- Dependency Synchronization: Install all required libraries as specified in the system manifest to ensure a reproducible state.
- Integrity Check: Verify the presence of the `practitioners/` and `apparatus/` directories before proceeding.

### 1.2 Cognitive Constraints

- Constitutional Authority: This file (`agents.md`) serves as the terminal authority. No agent action may contradict the directives herein.
- Orchestration Logic: The system must function as a recursive and self-healing interpreter. It identifies the goal, selects the appropriate Practitioner, and validates the output against the Law.

## Practitioners (Layer II: The Teleological Layer)

Located in `practitioners/`, this layer houses the expertise-based capability manifests of the AI skills. Practitioners act as the logical bridge between legal constraints and mechanical execution.

### 2.1 Role and Scope

- Declarative Logic: Practitioners define the what and the how, but never the action. They store the specific logic, required inputs, and the mapping to the relevant Python scripts.
- Knowledge Assets: Private libraries and reference materials, including standards, style guides, and templates, are maintained within `practitioners/lib/`. These assets serve as the ground truth for brand-specific formatting and technical standards.
- Statelessness: Practitioners are logic repositories. They do not maintain session state; they provide the blueprint for a specific goal.

## Apparatus (Layer III: The Mechanical Layer)

Located in `apparatus/`, this layer consists of deterministic Python scripts responsible for state changes and external interactions.

### 3.1 Execution Standards

- Deterministic Output: All scripts must be designed for 1:1 fidelity. Given the same input and state, the apparatus must produce the identical output.
- Restricted Side Effects: All file manipulations, Git operations, and JSON parsing are exclusively reserved for this layer. No cognitive or logic-heavy operations should occur here; the apparatus is a "blind" executor of the Practitioner’s logic.
- Validation: Every apparatus execution must return a structured exit code or status report to the Law to confirm successful completion of the mechanical task.

## Execution Flow

The system follows a linear, non-ambiguous execution path:

1. Law receives a task and identifies the governing domain.
2. Law invokes the relevant Practitioner from `practitioners/`.
3. Practitioner provides the logic and selects the necessary Apparatus from `apparatus/`.
4. Apparatus executes the deterministic script.
5. Law verifies the outcome against the Domain-Specific Rules and terminates the cycle.

## Self-Healing Loop

- Analyze error messages
- Fix and test scripts
- Update instruction sets (Self-anealing)
- Continuous system improvement

## Directory Structure

- `practitioners/` for skills and expert personas
- `apparatus/` for scripts
- `.tmp/` for intermediates
- `.env` for credentials

## Operating Principles

- Maintain the current system state in `state.json` so that every practitioner knows exactly what the others have completed.
- Check existing tools first
- Use as many practitioners as needed to achieve the goal at10/10 level.
- If something can be done by deterministic script, do it deterministically and avoid using LLM.
- When needed update skills as living documents
- Pragmatic and reliable execution
