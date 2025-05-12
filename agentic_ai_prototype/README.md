
# Providence Agentic AI System

This is a working prototype of a **multi-agent LLM system** designed to support cybersecurity and governance/risk/compliance (GRC) needs in a healthcare organization.

---

## 🧠 Design Overview

**Purpose**:  
To provide a Streamlit-based front-end for querying Cybersecurity and GRC-focused AI agents that reason over Providence-specific policy, architecture diagrams, and risk inputs.

### Architecture Components
- **Cyber Agent**: Ingests threat intel, attack patterns, and internal architecture to offer risk insights.
- **GRC Agent**: Specializes in frameworks like HIPAA, NIST, HITRUST, and Providence internal policies.
- **Agent Router**: Directs queries based on keywords or intent to the appropriate agent.
- **RAG (Retrieval-Augmented Generation)**: All agents use vectorized document embeddings to enrich LLM responses.
- **Streamlit Front-End**: Matches Providence branding, enables file input, interactive query, and PDF/Word report generation.

---

## 🚀 Project Structure

```
agentic_ai_prototype/
│
├── app/                    # Streamlit application logic
│   ├── main.py
│   └── agent_router.py
│
├── agents/                 # LLM Agents
│   ├── cyber_agent.py
│   ├── grc_agent.py
│   └── shared_tools.py
│
├── config/
│   └── app_config.yaml
│
├── deployment/             # Azure K8s deployment manifests
│   ├── azure_k8s_deployment.yaml
│   └── README.md
│
├── .github/workflows/      # CI/CD pipeline
│   └── deploy.yml
│
├── Dockerfile              # For building the container image
└── README.md               # This file
```

---

## ☁️ Azure Deployment

1. Build and push your container to Azure Container Registry.
2. Deploy using the provided Kubernetes manifest.
3. Optional: use GitHub Actions CI/CD in `.github/workflows/deploy.yml`.

For full deployment instructions, refer to `deployment/README.md`.

---

## 🔒 Security Notes

- Use Azure Key Vault or K8s Secrets for managing OpenAI API keys.
- Follow Providence's internal guidelines for LLM data inputs and logging.

---

## 📞 Questions?

Contact Ryan Scott – Cybersecurity Architect & Risk Engineer
