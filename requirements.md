# User Requirements Document (URD)

**Project Name:** Multilingual CSV Sentiment Miner
**Version:** 1.1
**Date:** December 30, 2025

## 1. Introduction

The system is an AI-powered data processing pipeline designed to ingest raw, multilingual customer feedback from CSV files, normalize the language, and output a structured analysis table containing sentiment and standardized topics.

### 1.1 Purpose

To validate the accuracy of AI-driven sentiment analysis and topic extraction before moving to visualization.

## 2. User Personas

* **The Analyst (Primary User):** Wants to see line-by-line analysis to verify if the AI correctly understood the "mixed language" comments.
* **The Engineer (Secondary User):** Uses this output to debug the DSPy logic.

---

## 3. Functional Requirements (FR)

*These define "What the system must do."*

### FR-01: Data Ingestion

* **FR-01.1:** The system MUST accept a standard CSV file as input.
* **FR-01.2:** The system MUST allow the user to specify the target column (e.g., "Comment").
* **FR-01.3:** The system MUST handle mixed encoding (UTF-8) for multilingual support.

### FR-02: AI Processing (The "Brain")

* **FR-02.1 - Sentiment Classification:** The system MUST classify each row into: `Positive`, `Negative`, or `Neutral`.
* **FR-02.2 - English Normalization:** The system MUST translate all extracted concepts into **Standard English** regardless of the input language.
* *Example:* Input "Giao hàng chậm"  Output Tag `Slow Shipping`.


* **FR-02.3 - Topic Extraction:** The system MUST extract 1-3 tags per row.
* *Constraint:* Tags must follow the format **Aspect + Sentiment** (e.g., "Expensive Price").



### FR-03: Data Output (Updated)

* **FR-03.1:** The system MUST output a **Structured Table** (displayed in Console or saved as a new `_analyzed.csv`).
* **FR-03.2:** The output table MUST contain exactly these columns:
1. `Original Text` (The raw input)
2. `Sentiment` (Positive/Negative/Neutral)
3. `Extracted Topics` (The list of English tags)


* **FR-03.3:** The system MUST NOT generate any images/charts in this version.

---

## 4. Non-Functional Requirements (NFR)

* **NFR-01: Accuracy:** Translation and Classification logic should hold up against "Code-Switching" (mixed VN/EN sentences, mixed JP/EN sentences).
* **NFR-02: Visibility:** The process should show a progress bar (e.g., "Processing row 10/50") because LLM calls are slow.



## 5. Technical Constraints (TC)

*These are strict engineering constraints for learning purposes.*

* **TC-01: Logic Orchestration (DSPy):** The application logic MUST be implemented using the **DSPy** framework. Standard OpenAI API calls or LangChain are **not** permitted for the core logic.
* **TC-02: Type Safety:** The system MUST use DSPy `Signatures` to enforce that the "Extracted Topics" return a valid Python List `['Tag A', 'Tag B']`, not a string.
* **TC-03: LLM Backend:** The system defaults to **GPT-4o-mini** (for cost/performance balance) but must be modular enough to switch to **Ollama (Llama 3)** by changing one line of code.

---

## 6. Technical Notes (Why we made these changes)

### Note A: Why Table instead of Word Cloud? (FR-03)

**Rationale:** "Trust but Verify."

* If you generate a Word Cloud immediately, you hide the AI's mistakes. If you see a big word "Shipping", you don't know if it came from a Positive review ("Fast Shipping") or a Negative one ("Slow Shipping").
* A **Table** allows you to audit the specific row:
* *Input:* "Hàng ok but ship hơi lâu."
* *AI Output:* `Sentiment: Neutral`, `Topic: ['Good Product', 'Slow Shipping']`.


* You need to see this explicit mapping to confirm the DSPy signature is working correctly before you aggregate it into a cloud.

### Note B: Why "Aspect + Sentiment" Tags? (FR-02.3)

**Rationale:**

* Standard Noun extraction gives you tags like "Price" and "Quality". This is useless data. (Is the price high? Is the quality good?).
* By forcing **Aspect + Sentiment** (e.g., "High Price"), the table becomes actionable immediately.

### Note C: Why is DSPy a Requirement? (TC-01)

**Rationale:**

* Usually, requirements shouldn't dictate the library. However, since the *goal* of this project is **Skill Acquisition**, using DSPy is a functional requirement for the *learning process*. It forces the developer (you) to think in "Signatures" and "Modules" rather than "Prompts".