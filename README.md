## The financial chatbot will be running properly on phi

## Go through this : https://docs.phidata.com/agent-ui
## Utilized AlphaVantage API, Hugging face Access Token, NewsApiKey, Groq Api Key, Phi API key to generate sentiment analysis, and market data based on a symbol(AAPL)

![Screenshot (179)](https://github.com/user-attachments/assets/516f1499-f2af-4317-a8fc-058547ae730e)

![Screenshot (177)](https://github.com/user-attachments/assets/b58f255c-8250-4581-b48b-a76809b46442)


![Screenshot (174)](https://github.com/user-attachments/assets/74175615-7919-46aa-a542-3daf0a0b88fa)


![Screenshot (175)](https://github.com/user-attachments/assets/9f737785-0c35-46ec-9f81-3cc2c99a4cdb)


![Screenshot (178)](https://github.com/user-attachments/assets/f542b62b-88ff-4e13-993e-6e4309fec4d5)


![Screenshot 2025-03-27 155436](https://github.com/user-attachments/assets/1bc61297-0fdc-4c08-b298-9f4b86117cd9)


![Screenshot 2025-03-27 155507](https://github.com/user-attachments/assets/e2f0857d-1170-4f5f-ad18-875d3e89df4d)


![Screenshot 2025-03-27 155543](https://github.com/user-attachments/assets/1f95ba83-15bd-4404-804b-ef32def2282a)


![Screenshot 2025-03-27 155555](https://github.com/user-attachments/assets/5834af2b-da07-4a1f-9d84-5ce2067d74e6)


If you want to dockerize container, then use the following files
## docker-compose.yml

version: '3.8'
services:
  app:
    build: .
    container_name: financial_ai_app
    restart: always
    env_file: .env
    ports:
      - "5000:5000"
    networks:
      - app_network
  nginx:
    image: nginx:latest
    container_name: "financial_ai_nginx"
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    networks:
      - app_network
networks:
  app_network:

  
  ## Dockerfile

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn","-c","gunicorn_config.py","playground:app"]

## gunicorn_config.py

bind="0.0.0.0:5000"
workers=4
threads=2
timeout=120

##  ngnix.conf
server{
    listen:80;
    server_name localhost;

    location / {
        proxy_pass http://playground:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
Use this commands: 

docker build -t CONTAINER_NAME .

docker ps

## Or Manually set up gunicorn
 pip install gunicorn

 gunicorn -w 4 -b 0.0.0.0:5000 playground:app






