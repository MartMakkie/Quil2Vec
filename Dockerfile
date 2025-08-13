FROM python:3.12
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libpotrace-dev \
    potrace \
    && rm -rf /var/lib/apt/lists/*

RUN pip install git+https://github.com/wntrblm/potracecffi.git
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app 

CMD ["python", "./app/__main__.py"]
# RUN conda 
