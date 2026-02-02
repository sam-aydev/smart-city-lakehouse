# 🏙️ Smart City IoT Lakehouse (2026 Edition)


[![Databricks](https://img.shields.io/badge/Databricks-Serverless-orange)](https://databricks.com)
[![Infrastructure](https://img.shields.io/badge/Infra-DABs-blue)](https://docs.databricks.com/dev-tools/bundles/index.html)

A modern, production-grade Data Lakehouse built on **Databricks**, **Delta Live Tables (DLT)**, and **AWS**. This project simulates an IoT network for a Smart City, processing real-time telemetry from public transportation sensors to predict maintenance needs using AI.

## 🏗️ Architecture
**Sensors (Python Simulator)** → **AWS S3 (Raw)** → **Databricks Auto Loader** → **Delta Live Tables (Bronze/Silver/Gold)** → **AI Analysis (DBRX)**

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Ingestion** | Databricks Auto Loader | Schema inference & evolution on streaming JSON data. |
| **Processing** | Delta Live Tables (DLT) | ACID transactions, expectations (data quality), and lineage. |
| **Compute** | Serverless | Instant startup and autoscaling without managing clusters. |
| **Orchestration** | Databricks Asset Bundles (DABs) | CI/CD-driven deployment for Dev/Prod isolation. |
| **Governance** | Unity Catalog | Row-level security and centralized access control. |

---

## 📂 Project Structure

```text
smart-city-lakehouse/
├── .github/workflows/      
├── conf/                   
├── src/
│   ├── generator/          
│   ├── pipeline/           
├── tests/      
├── requirements.txt
├── neccessary_info.ipynb                       
├── databricks.yml          
└── README.md       
```

## 🚀 Getting Started

### 1. Prerequisites
* **Databricks Workspace** (Premium/Enterprise)
* **AWS S3 Bucket**
* **Python 3.10+**
* **Databricks CLI** (v0.200+)


### 2. 🧪 Testing Strategy
We use Pytest to verify business logic before deployment.

Unit Tests: Located in tests/. We test the pure transformation functions (e.g., Risk Score calculation) independently of the Spark engine.

Integration Tests: Handled by the DLT "Expectations" (Data Quality Rules) during runtime.


### 3. 🔐 Security & Governance
* Service Principals: Production jobs run as a Service Principal (sp_smart_city_prod_runner), not a human user.

* Unity Catalog: All data access is governed by UC Volumes and Tables. No direct S3 keys are used in code.

* Network: All storage access is routed through secure endpoints.


