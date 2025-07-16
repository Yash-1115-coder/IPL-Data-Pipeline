# PHASE 5 - Looker Studio Visualization

## 🎯 Objective:
Build powerful dashboards using data from `BigQuery` → Present insights using **Looker Studio**.

---

## ⚙️ Tools Used:
- Looker Studio (previously Google Data Studio)
- Google BigQuery (as data source)

---

## 🛠️ Steps Followed:

### ✅ 1. Connected BigQuery to Looker Studio

- Opened: [https://lookerstudio.google.com](https://lookerstudio.google.com)
- Chose **BigQuery** as data source
- Selected:
  - Project: `ipl-streaming-project`
  - Dataset: `ipl_dbt_dataset`
  - Table: `stg_ipl_stats`

🧠 Pro Tip: Always use cleaned tables (via `dbt`) for visualization!

---

## ✅ 2. Created Visualizations (One Dashboard Page)

### 📊 Chart 1: Top 10 Run Scorers (Bar Chart)
- **Chart Type:** Bar chart (horizontal)
- **Dimension:** Player
- **Metric:** `TRuns`
- **Sort by:** `TRuns` (Descending)
- **Row Limit:** 10

---

### 📊 Chart 2: Top 10 Century Makers (Pie Chart)
- **Chart Type:** Pie Chart
- **Dimension:** Player
- **Metric:** `100s`
- **Filter:** Limit to Top 10 Century Scorers
- **Slice #11:** Others (auto-handled)

---

### 📊 Chart 3: Stack Bar - Most Ducks
- **Chart Type:** Stacked Bar Chart
- **Dimension:** Player
- **Metrics:**
  - `Inns`
  - `0s` (Ducks)
- **Sort by:** `0s` (Descending)
- **Row Limit:** Top 10 players

---

## ✅ 3. Added Filter Control (Dropdown)

- **Control Type:** Drop-down List
- **Field Used:** Player
- Used to dynamically filter all charts based on player selection.

---

## ✅ 4. Final Touches

- Organized all charts into a single page
- Gave chart titles
- Renamed dataset on canvas as “IPL 2024 Cleaned Stats”

---

## 🧠 Other Key Concepts (Used or Explored)

| Concept | Meaning |
|--------|---------|
| **Breakdown Dimension** | Split metric across multiple values (e.g., by TEAM or COUNTRY) |
| **Drill Down** | Hierarchical exploration (e.g., from Player → Team → Country) |
| **Filter Controls** | Used to dynamically slice the dataset |
| **Sorting** | Always sort descending for rankings |

---

## ✅ Result:
Clean & professional dashboard displaying:

- 🏏 Top Performers
- 🥶 Most Ducks
- 🧠 Custom filters for interactive exploration

---

## 🖼️ Presenting the Dashboard:
To reopen or share the dashboard:

1. Go to: [https://lookerstudio.google.com](https://lookerstudio.google.com)
2. Open: **Recent Reports** → Select your report
3. To share:
   - Click **“Share”**
   - Choose **“Anyone with link can view”**
   - Copy the link & give access to reviewers.

---

## 📌 Note on Data Accuracy:
The original CSV dataset (sourced from the course project repository) contained some inconsistencies, such as Runs being greater than TRuns for certain players. These were identified and documented during the pipeline build but were not corrected manually, as the project scope required using the dataset as provided.

---

# 💪 Final Looker Dashboard = ✅ READY 