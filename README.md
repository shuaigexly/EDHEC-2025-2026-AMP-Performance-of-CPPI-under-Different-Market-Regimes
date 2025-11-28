# CPPI Dynamic Portfolio Strategy Analysis (2015–2024)

A complete quantitative finance research pipeline including:

- Data acquisition (SP500, CSI300, T-Bill)
- Market regime identification
- Descriptive statistics & visualizations
- CPPI strategy implementation
- Buy & Hold benchmark
- Block bootstrap simulation (1,000 runs)
- Excel export of results
- CI automation with GitHub Actions
- Optional Docker deployment

---

## 📦 Installation

### Option A — pip

```bash
pip install -r requirements.txt
```

### Option B — conda environment

```bash
conda env create -f environment.yml
conda activate cppi
```

---

## ▶️ Run the full analysis

```bash
python src/main.py
```

All outputs (plots + Excel reports) will be generated in the project root directory.

---

## 📁 Project Structure

```
src/
│── data_fetch.py       # Module 1 - Download & clean data
│── regimes.py          # Module 2 - Identify market regimes
│── statistics.py       # Module 3 - Stats + Visualization + Excel output
│── cppi.py             # Module 4 - CPPI strategy
│── buy_hold.py         # Module 5 - Buy & Hold benchmark
│── bootstrap.py        # Module 6 - Block bootstrap simulation
│── main.py             # Master script
```

---

## 🐳 Optional: Run via Docker

```bash
docker build -t cppi .
docker run cppi
```

---

## 🤖 Continuous Integration (CI)

GitHub Actions workflow is included in:

```
.github/workflows/ci.yml
```

Every push automatically executes the entire analysis pipeline.

---

## © Author

Quantitative Research Project for CPPI Strategy  
Generated via ChatGPT Project Template Tool.
