FROM python:3.10-alpine
LABEL maintainer="Hayk Davtyan <hayko5999@gmail.com>"
WORKDIR app
COPY . .
RUN python -m pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]