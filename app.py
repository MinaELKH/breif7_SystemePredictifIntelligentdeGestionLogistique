import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
import pandas as pd

# ---------- Spark session ----------
spark = SparkSession.builder.appName("ML_Models_Streaming").getOrCreate()

# ---------- Charger le pipeline ----------
model_path = "models/logistic_regression_pipeline"
pipeline_model = PipelineModel.load(model_path)

# ---------- Définir les colonnes ----------
feature_numeric_cols = [
    "Days for shipment (scheduled)", "Benefit per order", "Sales per customer",
    "Order Item Discount", "Order Item Discount Rate", "Order Item Product Price",
    "Order Item Profit Ratio", "Order Item Quantity", "Sales", "Order Profit Per Order"
]

feature_categorical_cols = [
    "Type", "Shipping Mode", "Market", "Customer Segment",
    "Order Region", "Category Name"
]

# ---------- Valeurs par défaut réalistes (extraites de tes lignes) ----------
default_numeric = {
    "Days for shipment (scheduled)": 4,
    "Benefit per order": 91.25,
    "Sales per customer": 314.64,
    "Order Item Discount": 13.11,
    "Order Item Discount Rate": 0.04,
    "Order Item Product Price": 327.75,
    "Order Item Profit Ratio": 0.29,
    "Order Item Quantity": 1,
    "Sales": 327.75,
    "Order Profit Per Order": 91.25
}

default_categorical = {
    "Type": "DEBIT",
    "Shipping Mode": "Standard Class",
    "Market": "Pacific Asia",
    "Customer Segment": "Consumer",
    "Order Region": "Southeast Asia",
    "Category Name": "Sporting Goods"
}

# ---------- Streamlit UI ----------
st.title("Prédiction du risque de retard de livraison")
st.subheader("Remplissez les informations de la commande :")

# Stocker les inputs
input_data = {}

# Champs numériques avec valeurs par défaut
for col in feature_numeric_cols:
    input_data[col] = st.number_input(col, value=default_numeric.get(col, 0.0))

# Champs catégoriels avec selectbox et valeurs par défaut
for col in feature_categorical_cols:
    if col == "Shipping Mode":
        input_data[col] = st.selectbox(col, ["Standard Class", "First Class", "Second Class", "Same Day"],
                                       index=["Standard Class", "First Class", "Second Class", "Same Day"].index(default_categorical[col]))
    elif col == "Market":
        input_data[col] = st.selectbox(col, ["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"],
                                       index=["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"].index(default_categorical[col]))
    elif col == "Customer Segment":
        input_data[col] = st.selectbox(col, ["Consumer", "Corporate", "Home Office"],
                                       index=["Consumer", "Corporate", "Home Office"].index(default_categorical[col]))
    elif col == "Order Region":
        regions = ["East of USA", "West of USA", "Southern Europe", "Northern Europe",
                   "Central Asia", "South America", "Canada", "East Africa", "West Africa", "Southeast Asia"]
        input_data[col] = st.selectbox(col, regions, index=regions.index(default_categorical[col]))
    elif col == "Category Name":
        categories = ["Furniture", "Technology", "Office Supplies", "Binders", "Art", "Sporting Goods"]
        input_data[col] = st.selectbox(col, categories, index=categories.index(default_categorical[col]))
    else:
        input_data[col] = st.text_input(col, value=default_categorical.get(col, ""))

# Bouton de prédiction
if st.button("Prédire le risque de retard"):
    # Convertir en DataFrame Spark
    pdf = pd.DataFrame([input_data])
    sdf = spark.createDataFrame(pdf)

    # Appliquer le pipeline
    prediction = pipeline_model.transform(sdf).select("prediction").toPandas().iloc[0,0]

    # Afficher le résultat
    st.write(f"⚠️ Risque de retard prédit : {prediction}")
