# Use the base image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app/InfinityVision/InfinityVision

# Copy environment.yml and install dependencies
COPY environment.yml ./
RUN conda env create -f environment.yml

# Install additional packages and spaCy model within the same environment
RUN conda run --name InfinityVision pip install gunicorn faiss-cpu PyMuPDF transformers spacy && \
    conda run --name InfinityVision python -m spacy download en_core_web_lg

RUN conda run --name InfinityVision python -c "from transformers import pipeline; pipeline('question-answering', model='deepset/roberta-base-squad2')"


# Copy the entire project
COPY . .

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run the entrypoint script
CMD ["./entrypoint.sh"]
