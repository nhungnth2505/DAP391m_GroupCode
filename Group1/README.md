# CVD_Project — Heart Disease Prediction

Machine learning project predicting cardiovascular disease risk from the
[CVD_cleaned](https://www.kaggle.com/) dataset (BRFSS-derived, 308,854 records).
Built for the DAP391m course at FPT University, Can Tho.

**Live demo:** [uhuhihihehe.streamlit.app](https://uhuhihihehe.streamlit.app/)
*(Educational demo only — please do not enter real personal health information.)*

## What's in this repo

| File / Folder | Description |
|---|---|
| `CVD_ana.ipynb` | Full analysis notebook: encoding, EDA, feature engineering, class-imbalance handling, 9-model benchmark across 3 seeds, confusion matrix / ROC-AUC, feature importance, advanced visualizations (Waffle, Area, Pie, Scatter, Word Cloud, Choropleth). |
| `CVD_Research_Paper.docx` | IMRaD-format research paper summarizing the project (Introduction, Related Work, Methods, Results, Discussion, Limitations, References). |
| `streamlit_app/app.py` | Streamlit web app: heart disease risk prediction form + a TF-IDF/cosine-similarity chatbot answering questions about risk factors and the model. |
| `streamlit_app/requirements.txt` | Python dependencies for the app. |
| `streamlit_app/xgb_heart_disease_model.pkl` | Trained XGBoost model (balanced strategy, `scale_pos_weight`). |
| `streamlit_app/model_feature_columns.pkl` | Exact feature column order expected by the model. |

## Key result

XGBoost trained with `scale_pos_weight` to correct for severe class imbalance
(91.9% negative / 8.1% positive) achieves **ROC-AUC = 0.817**, recall = 71% for
the Heart Disease class. Accuracy alone (~0.77) looks worse than an
unbalanced model (~0.92 accuracy), but the unbalanced model misses the vast
majority of true positive cases — see the notebook's Step 8/9 for a controlled
comparison of both strategies.

## Running the Streamlit app

```bash
cd streamlit_app
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Running the notebook

Open `CVD_ana.ipynb` in Jupyter or VS Code. The `CVD_cleaned.csv` source file
(not included here — download from Kaggle) should sit in the same folder
before re-running the notebook from scratch.

## Disclaimer

This model is a screening/educational demonstration, not a diagnostic tool.
It should not be used as a substitute for professional medical evaluation.
