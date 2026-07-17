"""
Heart Disease Risk Screening App
---------------------------------
A Streamlit application built on top of the CVD_ana.ipynb analysis.

Two tabs:
1. Risk Prediction - enters health indicators, gets a risk estimate from the
   trained XGBoost model (Step 6/10 of the notebook, balanced strategy).
2. Chatbot - a simple TF-IDF + cosine-similarity retrieval chatbot that answers
   common questions about heart disease risk factors and how to read the
   prediction (same technique used in an earlier retrieval-based chatbot
   project, applied here to a small heart-health FAQ).
"""

import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Heart Disease Risk Screening", page_icon="\U0001FAC0", layout="wide")

# ----------------------------------------------------------------------
# Load model
# ----------------------------------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("xgb_heart_disease_model.pkl")
    feature_columns = joblib.load("model_feature_columns.pkl")
    return model, feature_columns

model, feature_columns = load_model()

# ----------------------------------------------------------------------
# Encoding helpers (must match CVD_ana.ipynb Step 1 and Step 3 exactly)
# ----------------------------------------------------------------------
HEALTH_ORDER = {"Poor": 0, "Fair": 1, "Good": 2, "Very Good": 3, "Excellent": 4}
CHECKUP_ORDER = {
    "Never": 0,
    "5 or more years ago": 1,
    "Within the past 5 years": 2,
    "Within the past 2 years": 3,
    "Within the past year": 4,
}
DIABETES_ORDER = {
    "No": 0,
    "No, pre-diabetes or borderline diabetes": 1,
    "Yes, but female told only during pregnancy": 2,
    "Yes": 3,
}
AGE_ORDER = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
             "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
AGE_MAP = {age: i for i, age in enumerate(AGE_ORDER)}


def bmi_category(bmi):
    if bmi < 18.5:
        return 0  # Underweight
    elif bmi < 25:
        return 1  # Normal
    elif bmi < 30:
        return 2  # Overweight
    else:
        return 3  # Obese


def build_feature_row(inputs: dict) -> pd.DataFrame:
    """Encode raw form inputs into the exact feature row the model expects."""
    height_m = inputs["height_cm"] / 100
    bmi = inputs["weight_kg"] / (height_m ** 2)

    row = {
        "General_Health": HEALTH_ORDER[inputs["general_health"]],
        "Checkup": CHECKUP_ORDER[inputs["checkup"]],
        "Exercise": int(inputs["exercise"]),
        "Skin_Cancer": int(inputs["skin_cancer"]),
        "Other_Cancer": int(inputs["other_cancer"]),
        "Depression": int(inputs["depression"]),
        "Diabetes": DIABETES_ORDER[inputs["diabetes"]],
        "Arthritis": int(inputs["arthritis"]),
        "Sex": int(inputs["sex"] == "Male"),
        "Age_Category": AGE_MAP[inputs["age_category"]],
        "Height_(cm)": inputs["height_cm"],
        "Weight_(kg)": inputs["weight_kg"],
        "BMI": bmi,
        "Smoking_History": int(inputs["smoking_history"]),
        "Alcohol_Consumption": inputs["alcohol_consumption"],
        "Fruit_Consumption": inputs["fruit_consumption"],
        "Green_Vegetables_Consumption": inputs["green_veg_consumption"],
        "FriedPotato_Consumption": inputs["fried_potato_consumption"],
    }
    row["BMI_Category"] = bmi_category(bmi)
    row["Comorbidity_Count"] = (
        row["Skin_Cancer"] + row["Other_Cancer"] + row["Depression"]
        + row["Arthritis"] + int(row["Diabetes"] >= 1)
    )
    row["Unhealthy_Diet_Score"] = row["FriedPotato_Consumption"] - (
        row["Fruit_Consumption"] + row["Green_Vegetables_Consumption"]
    )

    df_row = pd.DataFrame([row])
    return df_row[feature_columns]  # enforce exact training column order


# ----------------------------------------------------------------------
# Chatbot: small FAQ + TF-IDF retrieval
# ----------------------------------------------------------------------
FAQ = [
    ("What is cardiovascular disease?",
     "Cardiovascular disease (CVD) refers to conditions affecting the heart and blood vessels, "
     "including coronary heart disease, heart attack, and stroke. It is the leading cause of "
     "death worldwide."),
    ("What are the main risk factors for heart disease?",
     "Common risk factors include high blood pressure, high cholesterol, smoking, diabetes, "
     "obesity, physical inactivity, an unhealthy diet, excessive alcohol use, and older age."),
    ("What does BMI mean and why does it matter?",
     "BMI (Body Mass Index) estimates body fat using height and weight. Higher BMI, especially "
     "in the Overweight or Obese range, is associated with higher cardiovascular risk."),
    ("What is General_Health in this app?",
     "General_Health is a self-reported rating of overall health from Poor to Excellent. Lower "
     "self-rated health is one of the strongest predictors in this project's model."),
    ("What is Comorbidity_Count?",
     "Comorbidity_Count is an engineered feature counting how many of the following conditions "
     "a person has: skin cancer, other cancer, depression, arthritis, and diabetes. It was one "
     "of the more important engineered features in the model."),
    ("How accurate is this model?",
     "The underlying XGBoost model has an ROC-AUC of about 0.82 and misses roughly 29% of true "
     "heart disease cases (recall about 71%). It is intended as a screening aid, not a diagnosis."),
    ("Can this app diagnose heart disease?",
     "No. This app estimates statistical risk based on survey-style inputs. It cannot replace a "
     "doctor, an ECG, blood tests, or other clinical evaluation. If you are concerned about your "
     "heart health, please consult a healthcare professional."),
    ("Why does the model sometimes give a high risk score for a healthy-seeming profile?",
     "The model was deliberately trained to be sensitive to heart disease (high recall) rather "
     "than to maximize plain accuracy, so it flags borderline profiles more readily than it "
     "would if it were tuned only for accuracy."),
    ("How can I lower my risk of heart disease?",
     "General public health guidance includes not smoking, staying physically active, eating "
     "more fruits and vegetables, limiting fried and processed foods, managing blood pressure, "
     "cholesterol and blood sugar, and having regular checkups. This is general information, "
     "not personalized medical advice."),
    ("What dataset was this model trained on?",
     "The model was trained on CVD_cleaned, a dataset derived from the CDC's Behavioral Risk "
     "Factor Surveillance System (BRFSS), containing about 308,000 self-reported health records."),
    ("Why is heart disease hard to predict from survey data?",
     "BRFSS-style data is self-reported, not clinically measured, which introduces noise. It is "
     "also heavily imbalanced (about 8% positive cases), which makes accurate detection of the "
     "positive class inherently harder."),
    ("What does the risk percentage mean?",
     "The percentage is the model's estimated probability that the entered profile matches "
     "patterns associated with heart disease in the training data, not a certainty or a "
     "clinical probability for any individual."),
]

faq_questions = [q for q, _ in FAQ]
faq_answers = [a for _, a in FAQ]

@st.cache_resource
def build_chatbot():
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(faq_questions)
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = build_chatbot()


def chatbot_answer(user_question: str, threshold: float = 0.15):
    user_vec = vectorizer.transform([user_question])
    sims = cosine_similarity(user_vec, tfidf_matrix)[0]
    best_idx = sims.argmax()
    if sims[best_idx] < threshold:
        return ("I'm not sure about that one. Try asking about risk factors, BMI, "
                "General_Health, model accuracy, or how to lower heart disease risk."), sims[best_idx]
    return faq_answers[best_idx], sims[best_idx]


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------
st.title("\U0001FAC0 Heart Disease Risk Screening")
st.caption("Built on the CVD_cleaned analysis (XGBoost, balanced strategy, ROC-AUC 0.817). "
           "For education and screening demonstration only \u2014 not a medical diagnosis.")

tab_predict, tab_chat = st.tabs(["\U0001F4CA Risk Prediction", "\U0001F4AC Chatbot"])

with tab_predict:
    st.subheader("Enter health indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        general_health = st.selectbox("General health", list(HEALTH_ORDER.keys()), index=2)
        checkup = st.selectbox("Last checkup", list(CHECKUP_ORDER.keys()), index=4)
        age_category = st.selectbox("Age category", AGE_ORDER, index=5)
        sex = st.radio("Sex", ["Male", "Female"], horizontal=True)
        exercise = st.checkbox("Exercised in the past 30 days")

    with col2:
        height_cm = st.number_input("Height (cm)", 100.0, 230.0, 165.0, step=0.5)
        weight_kg = st.number_input("Weight (kg)", 30.0, 250.0, 65.0, step=0.5)
        smoking_history = st.checkbox("Smoking history")
        diabetes = st.selectbox("Diabetes status", list(DIABETES_ORDER.keys()))
        arthritis = st.checkbox("Diagnosed with arthritis")

    with col3:
        skin_cancer = st.checkbox("Diagnosed with skin cancer")
        other_cancer = st.checkbox("Diagnosed with other cancer")
        depression = st.checkbox("Diagnosed with depression")
        alcohol_consumption = st.number_input("Alcohol consumption (times/month)", 0, 30, 2)
        fruit_consumption = st.number_input("Fruit consumption (times/month)", 0, 120, 30)
        green_veg_consumption = st.number_input("Green vegetable consumption (times/month)", 0, 120, 20)
        fried_potato_consumption = st.number_input("Fried potato consumption (times/month)", 0, 120, 8)

    if st.button("Predict risk", type="primary"):
        inputs = dict(
            general_health=general_health, checkup=checkup, exercise=exercise,
            skin_cancer=skin_cancer, other_cancer=other_cancer, depression=depression,
            diabetes=diabetes, arthritis=arthritis, sex=sex, age_category=age_category,
            height_cm=height_cm, weight_kg=weight_kg, smoking_history=smoking_history,
            alcohol_consumption=alcohol_consumption, fruit_consumption=fruit_consumption,
            green_veg_consumption=green_veg_consumption,
            fried_potato_consumption=fried_potato_consumption,
        )
        X_row = build_feature_row(inputs)
        proba = float(model.predict_proba(X_row)[0, 1])

        st.divider()
        left, right = st.columns([1, 2])
        with left:
            st.metric("Estimated risk", f"{proba:.1%}")
            if proba < 0.30:
                st.success("Lower estimated risk")
            elif proba < 0.60:
                st.warning("Moderate estimated risk")
            else:
                st.error("Higher estimated risk")
        with right:
            st.progress(min(proba, 1.0))
            st.caption(
                "This is a statistical estimate from a screening model (recall \u2248 71%, "
                "ROC-AUC \u2248 0.82), not a diagnosis. Consult a healthcare professional for "
                "medical evaluation."
            )
            bmi_val = weight_kg / ((height_cm / 100) ** 2)
            st.write(f"Computed BMI: **{bmi_val:.1f}**")

with tab_chat:
    st.subheader("Ask about heart disease risk factors or this app")
    user_q = st.text_input("Your question", placeholder="e.g. What are the main risk factors for heart disease?")
    if user_q:
        answer, score = chatbot_answer(user_q)
        st.write(answer)
        st.caption(f"(match confidence: {score:.2f})")

    with st.expander("Example questions"):
        for q in faq_questions:
            st.write(f"- {q}")
