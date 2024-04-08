# server-app

1. Created env  using command :  python3 -m venv venv 
2. Activate env  : source venv/bin/activate 
3. install : pip install fastapi
4. install : pip install "uvicorn[standard]"
5. add main.py
6. setup git remote and add git required files
7. add Dockerfile


## Steps to run application from docker 

Open Docker applictaion :

###  Run the following commands in terminal : 

### `docker pull pavanpogula/server-app-pep:latest`

### You can verify the image has been downloaded by below command:  

### `docker images pavanpogula/server-app-pep`

### To run the application locally in background :

### `docker container run -d -p 8000:8000 --platform linux/amd64 pavanpogula/server-app-pep:latest`

Application running  [http://localhost:8000](http://localhost:8000) 


### To View Running container :

### `docker container ls`

**Note down CONTAINER ID**

### To Stop Container :

### `docker stop <Continer-ID>`



## `Steps to Run Application locaaly directly :`

### To start Container :

### `docker-compose up`

### To Stop Container :

### `docker-compose down`