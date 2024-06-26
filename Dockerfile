
FROM python:3.12.3-slim


WORKDIR /engagementscore


ENV HOST 0.0.0.0


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


EXPOSE 8080


CMD [ "python", "-m", "uvicorn", "engagementdata:app", "--host", "0.0.0.0", "--port", "8080"]
