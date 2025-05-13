# Azure Kubernetes Deployment for Cyber GRC Agentic AI

## Instructions

1. **Build and Push Docker Image**
   ```bash
   docker build -t agentic-ai:latest .
   az acr login --name yourregistry
   docker tag agentic-ai:latest yourregistry.azurecr.io/agentic-ai:latest
   docker push yourregistry.azurecr.io/agentic-ai:latest
   ```

2. **Apply Kubernetes Resources**
   ```bash
   kubectl apply -f azure_k8s_deployment.yaml
   ```

3. **Access**
   The app will be available via the LoadBalancer public IP.

## Notes
- Use Azure Key Vault or K8s secrets to manage your OpenAI API keys securely.
- Ensure outbound access for your pods to call OpenAI's API.
