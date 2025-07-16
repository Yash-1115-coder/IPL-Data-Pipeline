# PHASE 4 - Loading to BigQuery & Modeling with dbt

## 🎯 Objective:
Take the data from GCS (CSV format) → Load into BigQuery → Perform data transformations using `dbt` (Data Build Tool).

---

## ⚙️ Tools Used:
- Google BigQuery
- dbt-core (`dbt-bigquery`)
- Python venv (for managing dbt safely)

---

## 🛠️ Steps Followed:

### ✅ 1. Loaded CSV to BigQuery

- Dataset created: `ipl_dataset`
- Table created: `raw_ipl_stats`
- Format: CSV
- Loaded the GCS file (`gs://ipl-stream-output/ipl_stream_output/*.csv`) into BigQuery manually using the UI.

---

### ✅ 2. Set Up dbt Locally (WSL)

```bash
cd airflow_project
python3 -m venv dbt_venv
source dbt_venv/bin/activate
pip install dbt-bigquery
```

---

### ✅ 3. Initialized dbt Project

```bash
dbt init ipl_dbt_project
```

Filled in:
- **Auth Method:** `service_account`
- **Keyfile Path:** `/home/yash/airflow_project/ipl-streaming-project-xxxx.json`
- **GCP Project ID:** `ipl-streaming-project`
- **Dataset:** `ipl_dbt_dataset`
- **Location:** `US`
- **Threads:** `4`

---

### ✅ 4. Verified dbt Connection

```bash
cd ipl_dbt_project
dbt debug
```

✅ All checks passed.

---

### ✅ 5. Configured `dbt_project.yml`  
Generated automatically. Ensured:
```yaml
name: 'ipl_dbt_project'
version: '1.0.0'
profile: 'ipl_dbt_project'
model-paths: ["models"]
```

---

### ✅ 6. Added Models

Created model file:
```
models/staging_ipl/stg_ipl_stats.sql
```

📌 Contains cleaned & selected columns from `raw_ipl_stats`.  
📌 All fields matched the headers from the original CSV.  
📌 Example:

```sql
select
    Player,
    COUNTRY,
    TEAM,
    AGE,
    Runs,
    TRuns,
    4s,
    6s,
    0s,
    100s,
    50s,
    B_Wkts,
    B_TWkts
from {{ source('ipl_dbt_dataset', 'raw_ipl_stats') }}
```

---

### ✅ 7. Created `schema.yml` for Metadata

At:
```
models/staging_ipl/schema.yml
```

Defines:
- Source table: `raw_ipl_stats`
- Model: `stg_ipl_stats`

---

### ✅ 8. Ran dbt Models

```bash
dbt run
```

🔹 Output:
- View: `stg_ipl_stats`
- Table: `my_first_dbt_model`
- View: `my_second_dbt_model`

---

## ✅ Verification:

- View `ipl_dbt_dataset.stg_ipl_stats` created on BigQuery
- Confirmed all rows and columns exist

---

### 🚨 Common Errors Faced:
| Problem | Fix |
|--------|-----|
| `Unrecognized name` | Misspelled column in `.sql` |
| `dbt_project.yml not found` | Ensured `cd` into correct directory |
| `Access Denied` | Fixed IAM permissions for service account |

---

## 💡 Outcome:
Raw data → Cleaned view using `dbt` → Ready for BI tool (Looker Studio).

---
