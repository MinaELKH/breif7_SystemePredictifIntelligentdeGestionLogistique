FROM jupyter/pyspark-notebook:spark-3.5.0

USER root
# Install MongoDB tools and other dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER $NB_UID

# Set working directory
WORKDIR /home/jovyan/work

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=$NB_UID:$NB_GID . .

# Expose Jupyter port
EXPOSE 8888

# Expose Spark UI port
EXPOSE 4040

CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]