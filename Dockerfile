# 
FROM python:3.9

# 
WORKDIR /code

# Define multiple build-time arguments
ARG ARGUMENT1=default
ARG ARGUMENT2=default
ARG ARGUMENT3=default
# Set environment variables using the build-time arguments
ENV AWS_SECRET_ACCESS_KEY=$ARGUMENT1 \
    AWS_SECRET_ACCESS_KEY_ID=$ARGUMENT2 \
    REGION_NAME=$ARGUMENT3 \
    JWT_SECRET=$ARGUMENT4 \
    JWT_ALGORITHM=$ARGUMENT5
# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000
# 
COPY ./app /code/app

# 
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
