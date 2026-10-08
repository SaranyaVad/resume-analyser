# Resume Analyser — Data Engineer

Checks a resume against the skills a **Data Engineer** needs. It shows bar charts
of skill demand (as a percentage), your match score, and a ranked list of the
skills to learn next.

## Features

- Reads **PDF, DOCX and TXT** resumes.
- Uses a catalog of **65 Data Engineer skills** in 14 categories, each with a
  job-market demand percentage and a tier (Must-have ≥ 40%, Important 20–39%,
  Nice-to-have < 20%).
- Gives a **demand-weighted match score**, overall and per category.
- `--job`: scores the resume only against the skills one job description asks for.
- `--market`: shows the **% of your saved job ads** that mention each skill, so the
  percentages come from real postings you collected (for example, UK roles).
- `--html`: writes a self-contained HTML report with bar charts (light and dark
  mode, works on phones).

## Usage

```bash
pip install -r requirements.txt

# Skills map only (no resume)
python -m resume_analyser --html skills_map.html

# Analyse your resume
python -m resume_analyser my_resume.pdf --html report.html

# Against one specific job ad
python -m resume_analyser my_resume.pdf --job samples/jobs/73strings_senior_data_engineer.txt

# Against every job ad you've saved in a folder
python -m resume_analyser my_resume.pdf --market samples/jobs --html report.html
```

Tip: to analyse your LinkedIn profile, go to your profile → **More → Save to PDF**,
then pass that PDF in as the resume.

Example terminal output:

```
Overall Data Engineer match: 51%  ███████████████░░░░░░░░░░░░░░░

Skills to learn next (highest demand first)
 1. Azure                               38%  Important     Cloud Platforms
 2. Databricks                          35%  Important     Data Warehouses & Lakehouses
 ...
```

## Data Engineer skills and demand

"% of postings" is the approximate share of Data Engineer job postings that mention
the skill. These are **rounded estimates** from public job-market analyses. Use them
as relative guidance, and use `--market` with your own saved ads for real numbers.
To change them, edit `resume_analyser/skills.py`.

### Programming

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| SQL | `█████████████████░░░` | 85% | Must-have |
| Python | `████████████████░░░░` | 78% | Must-have |
| Java | `████░░░░░░░░░░░░░░░░` | 22% | Important |
| Scala | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| Shell Scripting | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |

### Big Data Processing

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Apache Spark | `███████████░░░░░░░░░` | 55% | Must-have |
| Hadoop | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| Hive | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| Apache Flink | `██░░░░░░░░░░░░░░░░░░` | 10% | Nice-to-have |

### Streaming

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Apache Kafka | `██████░░░░░░░░░░░░░░` | 32% | Important |
| Change Data Capture (CDC) | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Spark Streaming | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| AWS Kinesis | `██░░░░░░░░░░░░░░░░░░` | 8% | Nice-to-have |
| Pub/Sub & Event Hubs | `██░░░░░░░░░░░░░░░░░░` | 8% | Nice-to-have |

### Cloud Platforms

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| AWS | `██████████░░░░░░░░░░` | 50% | Must-have |
| Azure | `████████░░░░░░░░░░░░` | 38% | Important |
| GCP | `█████░░░░░░░░░░░░░░░` | 25% | Important |

### Data Warehouses & Lakehouses

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Databricks | `███████░░░░░░░░░░░░░` | 35% | Important |
| Snowflake | `███████░░░░░░░░░░░░░` | 33% | Important |
| Amazon Redshift | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| BigQuery | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| Azure Synapse | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| Delta Lake / Iceberg | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| Delta Live Tables / Lakeflow | `██░░░░░░░░░░░░░░░░░░` | 8% | Nice-to-have |
| Snowpark / Streams & Tasks | `█░░░░░░░░░░░░░░░░░░░` | 6% | Nice-to-have |

### ETL & Orchestration

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| ETL / ELT Pipelines | `████████████░░░░░░░░` | 60% | Must-have |
| Apache Airflow | `████████░░░░░░░░░░░░` | 38% | Important |
| dbt | `██████░░░░░░░░░░░░░░` | 28% | Important |
| Azure Data Factory | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| AWS Glue | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Informatica / SSIS | `██░░░░░░░░░░░░░░░░░░` | 10% | Nice-to-have |
| Fivetran / Airbyte | `██░░░░░░░░░░░░░░░░░░` | 8% | Nice-to-have |

### Databases

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| PostgreSQL | `████░░░░░░░░░░░░░░░░` | 22% | Important |
| NoSQL | `████░░░░░░░░░░░░░░░░` | 20% | Important |
| MySQL | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| SQL Server / Oracle | `██░░░░░░░░░░░░░░░░░░` | 12% | Nice-to-have |
| Redis | `█░░░░░░░░░░░░░░░░░░░` | 6% | Nice-to-have |
| KDB+ / Time-Series DBs | `█░░░░░░░░░░░░░░░░░░░` | 4% | Nice-to-have |
| Graph Databases | `█░░░░░░░░░░░░░░░░░░░` | 4% | Nice-to-have |

### Data Modeling & Architecture

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Data Warehousing | `█████████░░░░░░░░░░░` | 45% | Must-have |
| Data Modeling | `████████░░░░░░░░░░░░` | 40% | Must-have |
| Data Lake / Lakehouse | `█████░░░░░░░░░░░░░░░` | 25% | Important |
| Distributed Systems | `████░░░░░░░░░░░░░░░░` | 20% | Important |
| Time-Series Data | `██░░░░░░░░░░░░░░░░░░` | 8% | Nice-to-have |

### DevOps & Infrastructure

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Git | `██████░░░░░░░░░░░░░░` | 30% | Important |
| CI/CD | `█████░░░░░░░░░░░░░░░` | 25% | Important |
| Docker | `████░░░░░░░░░░░░░░░░` | 22% | Important |
| Terraform / IaC | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Kubernetes | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |

### Data Quality & Governance

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Data Quality | `█████░░░░░░░░░░░░░░░` | 25% | Important |
| Data Security & Access Control | `████░░░░░░░░░░░░░░░░` | 20% | Important |
| Data Governance | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| Performance Tuning | `████░░░░░░░░░░░░░░░░` | 18% | Nice-to-have |
| Monitoring & Incident Response | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Data Contracts | `█░░░░░░░░░░░░░░░░░░░` | 6% | Nice-to-have |

### BI & Visualization

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Power BI | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Tableau | `███░░░░░░░░░░░░░░░░░` | 14% | Nice-to-have |
| Looker | `█░░░░░░░░░░░░░░░░░░░` | 6% | Nice-to-have |

### AI & Machine Learning

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| ML Pipelines & MLOps | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Generative AI & LLMs | `██░░░░░░░░░░░░░░░░░░` | 10% | Nice-to-have |

### Certifications

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Cloud Data Certification | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |
| Databricks Certification | `██░░░░░░░░░░░░░░░░░░` | 10% | Nice-to-have |

### Professional Skills

| Skill | Demand | % of postings | Tier |
|---|---|---:|---|
| Communication & Collaboration | `███████░░░░░░░░░░░░░` | 35% | Important |
| Agile / Scrum | `████░░░░░░░░░░░░░░░░` | 20% | Important |
| Technical Leadership & Mentoring | `███░░░░░░░░░░░░░░░░░` | 15% | Nice-to-have |

## What the 5 sample UK job ads ask for

From `python -m resume_analyser --market samples/jobs`. The ads are 4 senior or lead
Databricks/Azure roles (London/UK, permanent and contract) and 1 AI Data Engineer
role on KDB+:

| Skill | % of the 5 ads |
|---|---:|
| Communication & Collaboration | 100% |
| Databricks, Data Lake / Lakehouse | 80% |
| Python, Apache Spark, Azure, Technical Leadership | 60% |
| SQL, ETL/ELT, Airflow, dbt, Data Quality, Data Governance, Monitoring, Spark Streaming, Generative AI, Delta Live Tables | 40% |

## Tests

```bash
python -m pytest -q
```
