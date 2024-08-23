FROM continuumio/miniconda3

WORKDIR /app/InfinityVision

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "InfinityVision", "/bin/bash", "-c"]

RUN pip install django gunicorn

COPY . .

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "InfinityVision", "gunicorn", "InfinityVision.wsgi:application", "--bind", "0.0.0.0:8000"]
