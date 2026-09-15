# Kubernetes GitOps Platform

A production-style Kubernetes delivery platform built on **Google Kubernetes Engine (GKE)** using **Helm, Argo CD, GitHub Actions, Artifact Registry, Workload Identity Federation, and GitOps**.

This project demonstrates how application code moves from a pull request to Dev, Staging, and Production using immutable container images, automated security checks, Git as the source of truth, and controlled production promotion.

## Architecture

```text
Developer
   |
   v
GitHub Pull Request
   |
   +--> pytest
   +--> Docker build
   +--> Trivy vulnerability scan
   |
   v
Merge to main
   |
   v
GitHub Actions
   |
   +--> Keyless OIDC authentication to GCP
   +--> Build immutable SHA-tagged image
   +--> Push to Artifact Registry
   +--> Update GitOps desired state
   |
   v
Git Repository
   |
   v
Argo CD
   |
   v
Helm
   |
   v
GKE
   |
   +--> Dev
   +--> Staging
   +--> Production
```

Production promotion:

```text
Build Once
   |
   v
Dev
   |
   v
Staging
   |
   v
Manual Production Approval
   |
   v
Production

Same immutable image SHA throughout
```

## Key Features

- Google Kubernetes Engine (GKE)
- Helm-based reusable Kubernetes deployments
- Argo CD automated sync, self-healing, and pruning
- GitOps-based delivery
- GitHub Actions CI/CD
- Python / Flask / Gunicorn application
- pytest automated testing
- Docker image build and validation
- Trivy CRITICAL vulnerability gate
- Google Artifact Registry
- Keyless GitHub-to-GCP authentication using Workload Identity Federation / OIDC
- Immutable Git SHA image tags
- Dev, Staging, and Production environments
- Same-artifact promotion between environments
- GitHub Environment approval for Production
- Kubernetes resource requests and limits
- Readiness and liveness probes
- Non-root application container

## Technology Stack

| Layer | Technology |
|---|---|
| Cloud | Google Cloud Platform |
| Kubernetes | Google Kubernetes Engine |
| Container | Docker |
| Application | Python / Flask / Gunicorn |
| Package Management | Helm |
| GitOps | Argo CD |
| CI/CD | GitHub Actions |
| Registry | Google Artifact Registry |
| Authentication | Workload Identity Federation / OIDC |
| Security | Trivy |
| Testing | pytest |
| Source Control | Git / GitHub |

## Repository Structure

```text
kubernetes-gitops-platform/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── promote-prod.yml
├── app/
│   ├── app.py
│   ├── test_app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── argocd/
│   ├── dev-application.yaml
│   ├── staging-application.yaml
│   └── prod-application.yaml
├── web-app-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   └── templates/
└── README.md
```

## CI Pipeline

Pull requests run:

```text
pytest
   |
   v
Docker build
   |
   v
Trivy scan
```

After merge to `main`:

```text
Tests
   |
   v
Build
   |
   v
Security Scan
   |
   v
OIDC Authentication
   |
   v
Artifact Registry
```

No long-lived GCP service-account JSON key is stored in GitHub.

## GitOps Delivery

GitHub Actions does **not** deploy directly to the Kubernetes API.

Instead:

```text
CI builds image
   |
   v
CI updates image SHA in Git
   |
   v
Argo CD detects Git change
   |
   v
Helm renders desired state
   |
   v
GKE reconciles application
```

Argo CD is configured with automated sync, pruning, and self-healing.

## Environment Strategy

Three environments are deployed:

```text
dev
staging
prod
```

Each environment uses a dedicated Helm values file:

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

And a dedicated Argo CD Application:

```text
web-app-dev
web-app-staging
web-app-prod
```

Final state:

```text
web-app-dev       Synced   Healthy
web-app-staging   Synced   Healthy
web-app-prod      Synced   Healthy
```

## Immutable Image Promotion

Container images are tagged with the Git commit SHA:

```text
europe-west2-docker.pkg.dev/<project>/<repository>/web-app:<git-sha>
```

The exact same immutable image is promoted between environments instead of being rebuilt.

Benefits:

- reproducibility
- artifact traceability
- easier rollback
- confidence that Production runs the same artifact tested in lower environments

## Production Promotion

Production deployment is separated from normal CI.

The `Promote to Production` workflow:

1. Reads the current Staging image SHA
2. Validates the SHA format
3. Authenticates to GCP using OIDC
4. Verifies the immutable image exists in Artifact Registry
5. Updates the Production GitOps value
6. Commits the change to Git
7. Allows Argo CD to reconcile Production

A GitHub `production` Environment provides the approval gate.

## Reliability and Security

Implemented controls include:

- CPU and memory requests
- CPU and memory limits
- readiness probes
- liveness probes
- rolling updates
- non-root container execution
- Trivy vulnerability scanning
- immutable SHA image tags
- OIDC instead of static cloud credentials
- Artifact Registry IAM
- production approval controls
- Git as the source of truth

## Troubleshooting and Lessons Learned

During the project I worked through several real operational issues:

- `ImagePullBackOff` caused by an incorrect image repository
- insufficient CPU scheduling on a small GKE cluster
- readiness and liveness probe failures
- a missing Argo CD ApplicationSet CRD
- fixable CRITICAL vulnerabilities detected by Trivy
- environment-specific Helm configuration issues

These issues were diagnosed and resolved without bypassing the security or GitOps controls.

## What This Project Demonstrates

This project demonstrates practical experience with:

- Kubernetes
- GKE
- Helm
- Argo CD
- GitOps
- CI/CD
- Docker
- cloud IAM
- container security
- immutable artifact promotion
- multi-environment delivery
- production approval controls
- Kubernetes troubleshooting
- cloud cost awareness

## Project Status

**Completed**

## Author

**Lawal Oladele Sulaiman**

DevOps / Cloud Engineering Portfolio Project
