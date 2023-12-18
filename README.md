# fastapi1
run: uvicorn main:app --reload

# To run with IP in Local
> add this lines to "main.py"

app = FastAPI()
if _name_ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

know_your_IP:
windows: ipconfig
ubuntu: ifconfig

<run(IP): uvicorn main:app --host 0.0.0.0 --port 8000 --reload>

## access the fastapi app from others system:
<search: http://<your-local-ip>:8000>

# CREATE THE ".env" file and add the below details
>> Create at the root directory
# .env

DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_HOSTNAME="localhost"
DATABASE_PORT="3306"
DATABASE_NAME=

SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
