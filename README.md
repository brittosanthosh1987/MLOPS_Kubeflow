# MLOPS_Kubeflow
AML Detection MLOps Project - End-to-End Implementation Steps
Key Learnings
•	Building multi-stage Kubeflow Pipelines
•	Kubernetes PVC management
•	Model persistence and versioning
•	Data drift simulation
•	MLOps workflow orchestration
•	Kubeflow on Kubernetes
•	Troubleshooting namespace-specific PVCs
________________________________________
Future Enhancements
•	MLflow Integration
•	Model Registry
•	Automated Drift Detection
•	FastAPI Model Deployment
•	Monitoring and Alerting
•	Automated Retraining Pipeline
________________________________________

Prerequisites
## Prerequisites

- AWS EC2 (Ubuntu)
- Docker
- KIND Kubernetes Cluster
- Kubeflow Pipelines
- Python 3.11
- kubectl
________________________________________

Create PVC
## Create Persistent Volume Claim

```bash
kubectl apply -f aml-pvc.yaml

---

### Upload AML Dataset

```markdown
## Upload Dataset to PVC

Copy datasets to the Kubernetes PVC:

```bash
kubectl cp data/aml_train.csv kubeflow/aml-data-loader:/data/aml_train.csv

kubectl cp data/aml_test.csv kubeflow/aml-data-loader:/data/aml_test.csv

---

### Create Drift Dataset

```markdown
## Create Data Drift Dataset

Generate a drifted evaluation dataset:

```bash
python create_drift_dataset.py
This creates:
aml_drift.csv

---

### Compile Kubeflow Pipeline

```markdown
## Compile Pipeline

```bash
python aml_kubeflow_pipeline.py
Output:
aml_kubeflow_pipeline.yaml

---

### Access Kubeflow UI

```markdown
## Access Kubeflow UI

Port forward Kubeflow Pipelines:

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
Open:
http://localhost:8080

---

### Upload Pipeline

```markdown
## Upload Pipeline

1. Open Kubeflow UI
2. Navigate to Pipelines
3. Upload Pipeline  with "aml_kubeflow_pipeline.yaml"
4. select experiement and run tab then create it
5. you can see a pipeline build and you can validate the accuracy in evalaute pipeline logs. 



