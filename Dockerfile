FROM python:3.12-slim

LABEL maintainer="Kalimu <lilkalimu-glitch@users.noreply.github.com>"
LABEL description="Intentionally vulnerable web application for security education"

# Install system utilities used by Command Injection lab
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        iputils-ping \
        dnsutils \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p db app/static/uploads

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["python", "run.py"]
