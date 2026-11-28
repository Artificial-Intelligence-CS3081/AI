# AquaGent – CS3081 Artificial Intelligence

An explainable decision-support agent that chooses between a fog collector, a MOF-303 sorbent bed,
or no plan for collecting water from air, when weather evidence is uncertain and energy is limited.
It combines **Bayesian inference** (estimating fog from uncertain sensor readings) with a
**constraint satisfaction** search (keeping only plans that respect safety, time and energy limits).

| | |
|---|---|
| **University** | Effat University |
| **Course** | CS3081 Artificial Intelligence |
| **Semester** | Fall 2026 |
| **Instructor** | Dr. Naila Marir |

## Team Members

- Zainab Alameri
- Abubaker Baobaid

## Project Links

- **GitHub Repository (course copy):** https://github.com/Zalameri/CS3081AI/tree/main/Projects/AquaGent
- **Standalone Repository:** https://github.com/Zalameri/aquagent
- **Interactive Demo:** https://zalameri.github.io/aquagent/
- **Project Portfolio Page:** https://zalameri.github.io/project.html?p=aquagent

## Submission Contents

Files included in this submission folder:

| File | Description |
|---|---|
| `AquaGent_ACL_Report.pdf` | Technical Report (ACL Format) |
| `AquaGent final AI.pdf` | Final Presentation |
| `AquaGent_Poster2_A1.pdf` | A1 Research Poster |
| `AquaGent_Contribution_Declaration.pdf` | Contribution Declaration Form |
| `README.md` | This file: project information and links |

The source code and its 45 unit tests (Python, Streamlit) are on GitHub:
[Projects/AquaGent](https://github.com/Zalameri/CS3081AI/tree/main/Projects/AquaGent).

## Run It Locally

```bash
git clone https://github.com/Zalameri/aquagent.git
cd aquagent
pip install -r requirements.txt
streamlit run app.py
```
