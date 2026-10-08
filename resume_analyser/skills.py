"""Data Engineer skill catalog.

Each skill has a ``demand`` value: the approximate share (%) of Data Engineer
job postings that mention it. These are rounded estimates compiled from public
job-market surveys and posting analyses; treat them as relative guidance, not
exact figures. Update them as the market shifts.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Skill:
    name: str
    category: str
    demand: int  # approx. % of Data Engineer job postings mentioning the skill
    aliases: tuple[str, ...] = field(default_factory=tuple)

    @property
    def tier(self) -> str:
        if self.demand >= 40:
            return "Must-have"
        if self.demand >= 20:
            return "Important"
        return "Nice-to-have"

    @property
    def patterns(self) -> tuple[str, ...]:
        return (self.name, *self.aliases)


def _s(category: str, name: str, demand: int, *aliases: str) -> Skill:
    return Skill(name=name, category=category, demand=demand, aliases=aliases)


PROGRAMMING = "Programming"
PROCESSING = "Big Data Processing"
STREAMING = "Streaming"
CLOUD = "Cloud Platforms"
WAREHOUSE = "Data Warehouses & Lakehouses"
ORCHESTRATION = "ETL & Orchestration"
DATABASES = "Databases"
MODELING = "Data Modeling & Architecture"
DEVOPS = "DevOps & Infrastructure"
QUALITY = "Data Quality & Governance"
BI = "BI & Visualization"
AI = "AI & Machine Learning"
CERTS = "Certifications"
SOFT = "Professional Skills"

SKILLS: tuple[Skill, ...] = (
    # Programming
    _s(PROGRAMMING, "SQL", 85, "t-sql", "pl/sql", "plsql", "tsql", "ansi sql"),
    _s(PROGRAMMING, "Python", 78, "pandas", "pyspark"),
    _s(PROGRAMMING, "Java", 22),
    _s(PROGRAMMING, "Scala", 18),
    _s(PROGRAMMING, "API Development", 12, "rest api", "fastapi", "flask", "api integration", "graphql"),
    _s(PROGRAMMING, "TypeScript / JavaScript", 5, "typescript", "javascript", "node.js", "nodejs"),
    _s(PROGRAMMING, "Shell Scripting", 15, "bash", "shell script", "unix shell", "linux"),
    # Big data processing
    _s(PROCESSING, "Apache Spark", 55, "spark", "pyspark", "spark sql"),
    _s(PROCESSING, "Hadoop", 18, "hdfs", "mapreduce", "yarn"),
    _s(PROCESSING, "Hive", 12, "apache hive", "hiveql"),
    _s(PROCESSING, "Apache Flink", 10, "flink"),
    # Streaming
    _s(STREAMING, "Apache Kafka", 32, "kafka", "confluent"),
    _s(STREAMING, "Spark Streaming", 12, "structured streaming"),
    _s(STREAMING, "Change Data Capture (CDC)", 15, "cdc", "change data capture", "debezium", "kafka connect",
       "auto cdc"),
    _s(STREAMING, "AWS Kinesis", 8, "kinesis"),
    _s(STREAMING, "Pub/Sub & Event Hubs", 8, "pub/sub", "pubsub", "event hubs", "eventhub"),
    # Cloud
    _s(CLOUD, "AWS", 50, "amazon web services", "s3", "emr", "redshift", "glue", "ecs", "rds"),
    _s(CLOUD, "Azure", 38, "microsoft azure", "adls", "data lake storage", "synapse"),
    _s(CLOUD, "GCP", 25, "google cloud", "bigquery", "dataflow", "dataproc"),
    # Warehouses & lakehouses
    _s(WAREHOUSE, "Databricks", 35),
    _s(WAREHOUSE, "Snowflake", 33),
    _s(WAREHOUSE, "Amazon Redshift", 18, "redshift"),
    _s(WAREHOUSE, "BigQuery", 18, "big query"),
    _s(WAREHOUSE, "Azure Synapse", 12, "synapse analytics", "synapse"),
    _s(WAREHOUSE, "Delta Lake / Iceberg", 12, "delta lake", "apache iceberg", "iceberg", "apache hudi", "hudi",
       "delta sharing"),
    _s(WAREHOUSE, "Delta Live Tables / Lakeflow", 8, "delta live tables", "dlt", "lakeflow",
       "declarative pipelines"),
    _s(WAREHOUSE, "Snowpark / Streams & Tasks", 6, "snowpark", "dynamic tables", "streams and tasks",
       "snowflake streams"),
    # ETL & orchestration
    _s(ORCHESTRATION, "ETL / ELT Pipelines", 60, "etl", "elt", "data pipeline", "data pipelines"),
    _s(ORCHESTRATION, "Apache Airflow", 38, "airflow", "mwaa", "cloud composer"),
    _s(ORCHESTRATION, "dbt", 28, "data build tool"),
    _s(ORCHESTRATION, "Azure Data Factory", 18, "adf", "data factory"),
    _s(ORCHESTRATION, "AWS Glue", 15, "glue"),
    _s(ORCHESTRATION, "Fivetran / Airbyte", 8, "fivetran", "airbyte", "stitch"),
    _s(ORCHESTRATION, "Informatica / SSIS", 10, "informatica", "ssis", "talend"),
    # Databases
    _s(DATABASES, "PostgreSQL", 22, "postgres", "postgresql"),
    _s(DATABASES, "NoSQL", 20, "mongodb", "cassandra", "dynamodb", "cosmos db", "cosmosdb", "hbase"),
    _s(DATABASES, "MySQL", 12),
    _s(DATABASES, "SQL Server / Oracle", 12, "sql server", "mssql", "oracle"),
    _s(DATABASES, "Redis", 6),
    _s(DATABASES, "KDB+ / Time-Series DBs", 4, "kdb+", "kdb", "q/kdb+", "timescaledb", "influxdb"),
    _s(DATABASES, "Graph Databases", 4, "neo4j", "graph database", "neptune"),
    # Modeling & architecture
    _s(MODELING, "Data Warehousing", 45, "data warehouse", "data warehousing", "dwh", "edw"),
    _s(MODELING, "Data Modeling", 40, "dimensional modeling", "dimensional modelling", "data modelling",
       "star schema", "snowflake schema", "kimball", "data vault", "slowly changing dimension",
       "slowly changing dimensions", "scd"),
    _s(MODELING, "Data Lake / Lakehouse", 25, "data lake", "lakehouse", "medallion", "bronze/silver/gold"),
    _s(MODELING, "Time-Series Data", 8, "timeseries", "time series", "time-series", "tick data",
       "market data"),
    _s(MODELING, "Distributed Systems", 20, "distributed computing", "distributed system"),
    # DevOps
    _s(DEVOPS, "Git", 30, "github", "gitlab", "bitbucket", "version control"),
    _s(DEVOPS, "CI/CD", 25, "ci/cd", "cicd", "jenkins", "github actions", "azure devops"),
    _s(DEVOPS, "Docker", 22, "containers", "containerization"),
    _s(DEVOPS, "Terraform / IaC", 15, "terraform", "infrastructure as code", "iac", "cloudformation"),
    _s(DEVOPS, "Kubernetes", 15, "k8s", "eks", "aks", "gke"),
    # Quality & governance
    _s(QUALITY, "Data Quality", 25, "data validation", "schema validation", "great expectations", "data testing",
       "reconciliation",
       "dqx", "data metric functions", "quarantine"),
    _s(QUALITY, "Data Contracts", 6, "data contract", "data contracts", "schema registry"),
    _s(QUALITY, "Data Security & Access Control", 20, "access control", "rbac", "row-level security",
       "tenant isolation", "multi-tenant", "encryption", "gdpr", "data protection", "pii", "iso 27001",
       "soc 2"),
    _s(QUALITY, "Monitoring & Incident Response", 15, "monitoring", "observability", "alerting",
       "incident response", "production support", "on-call"),
    _s(QUALITY, "Data Governance", 18, "unity catalog", "data catalog", "lineage", "collibra", "purview"),
    _s(QUALITY, "Performance Tuning", 18, "query optimization", "query optimisation", "partitioning",
       "performance optimization", "performance optimisation", "cost management", "cost optimisation",
       "cost optimization", "finops"),
    # BI
    _s(BI, "Power BI", 15, "powerbi"),
    _s(BI, "Tableau", 14),
    _s(BI, "Looker", 6, "lookml"),
    _s(BI, "Semantic Layer", 6, "semantic layer", "cube.dev", "cube", "lookml", "dbt metrics", "metricflow"),
    # AI & machine learning
    _s(AI, "ML Pipelines & MLOps", 15, "machine learning", "ml model", "mlops", "mlflow", "feature store",
       "scikit-learn", "sklearn"),
    _s(AI, "Generative AI & LLMs", 10, "ai", "genai", "generative ai", "llm", "large language model", "rag",
       "vector database", "embedding", "ai-ready", "ai agent", "cortex", "claude", "openai"),
    # Certifications
    _s(CERTS, "Cloud Data Certification", 15, "dp-203", "dp-700", "azure data engineer associate",
       "fabric data engineer", "aws certified", "google professional data engineer",
       "professional data engineer", "snowpro"),
    _s(CERTS, "Databricks Certification", 10, "databricks certified", "databricks certification",
       "databricks data engineer associate", "databricks data engineer professional"),
    # Professional
    _s(SOFT, "Communication & Collaboration", 35, "communication", "stakeholder", "collaboration", "collaborate", "collaborating",
       "collaborative",
       "cross-functional"),
    _s(SOFT, "Agile / Scrum", 20, "agile", "scrum", "jira", "kanban"),
    _s(SOFT, "Technical Leadership & Mentoring", 15, "mentoring", "mentor", "technical lead", "tech lead",
       "led a team", "leading a team", "lead a team", "technical leadership",
       "lead data engineer", "technical decision-making"),
)

CATEGORIES: tuple[str, ...] = tuple(dict.fromkeys(s.category for s in SKILLS))
