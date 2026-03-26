FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install numpy pydantic openenv

CMD ["python", "baseline.py"]