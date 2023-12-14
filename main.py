from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os


SECRET = os.getenv("SECRET")

#
app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")

async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/homepage")
async def demo_get():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    homepage = driver.get("https://www.flashscore.com").page_source
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    


