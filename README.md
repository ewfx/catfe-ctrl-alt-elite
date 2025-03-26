# FINSURE

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Finsure is a regulation and context-aware testing solution made with agentic AI. We leverage LLMs to add the missing heretofore human element to the modern testing workflow, and VectorDBs to add unerring domain knowledge of regulations and compliance requirements. 

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)


## 💡 Inspiration

The inspiration behind FINSURE stems from the increasing complexity of regulatory compliance and the challenges faced by financial institutions in ensuring their systems are robust, secure, and compliant. The project addresses the critical need for a solution that can automatically test financial systems for compliance with ever-evolving regulations, ensuring data security, fairness, and reliability. By leveraging agentic AI, FINSURE aims to simplify compliance processes while enhancing the robustness of financial systems.

## ⚙️ What It Does

FINSURE offers a comprehensive suite of features designed to streamline testing and compliance:

- **Regulations Knowledge Database and RAG Pipeline**: A repository for regulatory updates integrated with retrieval-augmented generation (RAG) for real-time compliance insights.
- **Context-Aware Test Generator and Executor Pipeline**: Automatically generates and executes tests tailored to specific regulatory contexts.
- **Context-Aware Test Request API**: API-agnostic pipeline for generating and executing test requests.
- **AI Agents for UI Automation**: Automates UI testing using natural language instructions.
- **GenAI Testing Scenarios**: Simulates scenarios to test payment systems' robustness, providing stakeholder-friendly explanations for failures.
- **Loan Risk Model Testing**: Uses generative AI to simulate diverse personas for testing credit risk models for fairness and reliability.
- **Plug-and-Play Workflows**: Seamless integration with enterprise pipelines via GitHub Actions.
- **Multi-Format Solutions**: Available as a VSCode plugin, Python package, CLI tool, GitHub Workflow Generator, and Regulatory Compliance VectorDB.


## 🛠️ How We Built It

The development of FINSURE involved a diverse tech stack tailored to its various components:

- **Regulations Knowledge Database and RAG Pipeline**: Built using Elasticsearch for efficient data retrieval.
- **Context-Aware Test Generator and Executor Pipeline**:
    - *Codebase Defender*: Focused on SOX, KYC, AML tests using Java and Gradle.
    - *Prompt Defender*: A UI test agent leveraging finance-aware prompts with Browseruse and Playwright.
- **PaymentAPI Defender**: Ensures compliance with Swift messaging standards using PayPal Sandbox API and Python.
- **CreditEngine Defender**: Tests ML models for credit risk using Python.
- **UI Automation Tester**: Employs Browseruse and Playwright for natural language-based UI testing.


## 🚧 Challenges We Faced

The team encountered several technical and non-technical challenges during development:

1. **Regulatory Complexity**: Keeping up with constantly changing global regulations required a robust system for real-time updates.
2. **Context Variability in Testing**: Designing a context-aware testing framework that could adapt to diverse financial environments was a significant hurdle.
3. **Scalability of AI Agents**: Ensuring the AI agents could handle complex UI automation tasks while maintaining accuracy and efficiency.
4. **Integration with Enterprise Pipelines**: Developing plug-and-play workflows that seamlessly integrate with existing enterprise systems posed technical challenges.
5. **Stakeholder Communication**: Creating failure explanations understandable by both technical and non-technical stakeholders required careful design of GenAI outputs.
## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: HTML/Streamlit
- 🔹 Backend: FastAPI
- 🔹 Database: Elasticsearch
- 🔹 Other: Gemini API, Python

## 👥 Team
- **** - [GitHub](#) | [LinkedIn](#)
- **** - [GitHub](#) | [LinkedIn](#)
