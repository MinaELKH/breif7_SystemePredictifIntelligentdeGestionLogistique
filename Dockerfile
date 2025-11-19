FROM jupyter/pyspark-notebook:spark-3.5.0

USER root
# Installer wget, curl et streamlit
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer Streamlit
RUN pip install streamlit

# Revenir à l'utilisateur jovyan
USER $NB_UID

# Définir le répertoire de travail
WORKDIR /home/jovyan/work

# Copier le projet
COPY --chown=$NB_UID:$NB_GID . .

# Exposer les ports
EXPOSE 8888
EXPOSE 4040
EXPOSE 8501
# Commande par défaut : Jupyter + Streamlit
CMD ["bash", "-c", "start-notebook.sh --NotebookApp.token='' --NotebookApp.password='' & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
