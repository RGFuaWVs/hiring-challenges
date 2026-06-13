# Use the minimal runtime image. It runs as nonroot by default.
FROM python:3.12-slim
WORKDIR /app
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY . .
RUN pip3 install -e .
EXPOSE 5000
CMD ["python3", "run.py", "--host", "0.0.0.0", "--port", "5000"]