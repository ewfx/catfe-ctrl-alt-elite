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
📹 [Video Demo](#) : https://drive.google.com/file/d/1WxZ1D_3FeFZDLO_KFQO_di_XpHt9Fucs/view?usp=sharing  
🔗 [Presentation Link]: https://www.canva.com/design/DAGi0WiuLh8/uqHU-3BlUIUY8vlhjWtYQA/view?utm_content=DAGi0WiuLh8&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h0d0edc30c6
🖼️ Screenshots:

![Screenshot 1](link-to-image)


## 💡 Inspiration

The inspiration behind FINSURE stems from the increasing complexity of regulatory compliance and the challenges faced by financial institutions in ensuring their systems are robust, secure, and compliant. The project addresses the critical need for a solution that can automatically test financial systems for compliance with ever-evolving regulations, ensuring data security, fairness, and reliability. By leveraging agentic AI, FINSURE aims to simplify compliance processes while enhancing the robustness of financial systems.

## 💻 Architecture Diagrams
## RAG powered Context-Aware Test function and API requestor Generator and Executor Pipelines
![Regulation_Context_RAG_pipelines](https://github.com/user-attachments/assets/bfafd91c-4c6b-4407-9757-c21367168a6b)

## NLP instructed UI automation testing
![WhatsApp Image 2025-03-26 at 14 20 15](https://github.com/user-attachments/assets/b5523cf5-5cb0-44eb-9687-49b8313929bf)



## ⚙️ What It Does

FINSURE offers a comprehensive suite of features designed to streamline testing and compliance:
- **Regulations Knowledge Database and RAG Pipeline**: A repository for regulatory updates integrated with retrieval-augmented generation (RAG) for real-time compliance insights.
- **Context-Aware Test Generator and Executor Pipeline**: Automatically generates and executes tests tailored to specific regulatory contexts.
- **Context-Aware Test Request API**: API-agnostic pipeline for generating and executing test requests.
- **AI Agents for UI Automation**: Automates UI testing using natural language instructions.
- **Testing Payment API Compliance**: Generates test cases for payment systems, validating compliance with Fed, SWIFT, and ISO regulations by interacting with actual payment API endpoints.
- **Fraud Detection and Analysis**: Detects fraud patterns and analyzes them, providing resolutions for issues.
- **GenAI Testing Scenarios**: Simulates scenarios to test payment systems' robustness, providing stakeholder-friendly explanations for failures.
- **Loan Risk Model Testing**: Uses generative AI to simulate diverse personas for testing credit risk models for fairness and reliability.
- **Plug-and-Play Workflows**: Seamless integration with enterprise pipelines via GitHub Actions.
- **Multi-Format Solutions**: Available as a VSCode plugin, Python package, CLI tool, GitHub Workflow Generator, and Regulatory Compliance VectorDB.

  <img alt="Screenshot 2025-03-27 at 4 44 49 AM" src="https://github.com/user-attachments/assets/0f417c2b-9f90-4204-a5a0-024f46fb7b51" />

**These solution are Tachyon compliant and portably packaged ,facilitating easy integration with VS code plugin (Orchestra) and Artifactory(PIP - Python package manager)**


## 🛠️ How We Built It

The development of FINSURE involved a diverse tech stack tailored to its various components:

- **Regulations Knowledge Database and RAG Pipeline**: Built using Elasticsearch for efficient data retrieval.
- **Context-Aware Test function Generator and Executor Pipeline**:
    - *Codebase Defender*: Focused on SOX, KYC, AML tests using Java and Gradle.
- **Context-Aware Test API request Generator and Executor Pipelines**:
    - *PaymentAPI Defender*: Ensures compliance with Swift messaging standards using Trasanction gateway endpoints and Python,Now implemented with PayPal transaction API.
    - *CreditEngine Defender*: Tests ML models for credit risk using Python.
- **UI Automation Tester**: Employs Browseruse and Playwright for natural language-based UI testing.
- **Prompt Defender**: A UI test agent for testing chatbots with Prompt injection leveraging finance-aware prompts with Browseruse and Playwright.

# Command line interface(IDE and OS Agnostic)
  ![Command line interface](https://github.com/user-attachments/assets/cdb723ad-6c40-4af3-a57a-f93de1052174)
# VS Code Plugin (OS Agnostic) 
  ![VS Code plugin](https://github.com/user-attachments/assets/8e54c5dd-790a-4e84-97c8-f55940827b93)



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
   git clone https://github.com/ewfx/catfe-ctrl-alt-elite.git
   ```
2. CLI installation- navigate to code/src/Finsure\ CLI
   ```sh
   pip install . (for Python) # pip install finsure.whl(in build folder)
   ```
3.  VS code plugin installation - navigate to code/src/Finsure\ VS\ code\ plugin 
   ```sh
   code --install-extension finsure-0.0.1.vsix 
   ```

## 🏗️ Tech Stack
- 🔹 VS code plugin: Typescript,Javascript
- 🔹 Command Line interface: Python, Typer
- 🔹 RAG Database: Elasticsearch
- 🔹 Agentic AI: Browser Use
- 🔹 Frontend: HTML/Streamlit
- 🔹 Backend: FastAPI,PayPal API
- 🔹 Containerization: Docker
- 🔹 Testing instruments: Paypal Transaction Sandbox API,Credit Score Assesment ML(XG boost),Swift Transaction(Java Class)
  
## 👥 Team
- **Atiraj Kumar** 
- **Jyothikamalesh S**
- **Kaarthik Shankar** 
- **Kumar Saurav** 
- **Ayush Singh**
