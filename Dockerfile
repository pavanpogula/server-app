# 
FROM python:3.9

# 
WORKDIR /code
# Define build-time argument
ARG AWS_SECRET_ACCESS_KEY=pavanreddy

# Set environment variable with the build-time argument
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000
# 
COPY ./app /code/app

# 
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
