import decimal
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.chrome.service import Service
import json
from webdriver_manager.chrome import ChromeDriverManager

def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return myDriver

def getPage(driver: webdriver.Chrome, url) -> str:
    driver.get(url)
    time.sleep(10)
    p=driver.find_element(By.CLASS_NAME,'header__text')
    if p:
        try:
            logged=driver.find_element(By.XPATH, '//*[@class="header__text header__text--user header__text--loggedIn"]')
        except Exception:
            menu = driver.find_element(By.XPATH, '//*[@id="user-menu"]')
            menu.click()
            time.sleep(2)
        try:
            cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            cookies.click()
        except Exception:
            pass
        try:
            email_login = driver.find_element(By.XPATH,'//button[@class="ui-button ui-formButton social__button email"]')
            scroll_origin = ScrollOrigin.from_element(email_login)
            ActionChains(driver)\
                .scroll_from_origin(scroll_origin, 0, 50)\
                .perform()

            email_login.click()
            time.sleep(2)
            email = driver.find_element(By.XPATH,'//*[@id="email"]')
            password = driver.find_element(By.XPATH, '//*[@id="passwd"]')
            email.send_keys('princeguy01@gmail.com')
            password.send_keys('pr1ncet0wn.')
            time.sleep(2)
            login = driver.find_element(By.XPATH, '//*[@id="header__block--user-menu"]/div[2]/div/div/div/section/button')
            login.click()
            time.sleep(15)
        except Exception:
            print("already logged")

    oddbtn = driver.find_element(By.XPATH,'//*[@id="live-table"]/div[1]/div[1]/div[3]')
    oddbtn.click()
    time.sleep(5)

    def collectdata(date):
        html = driver.page_source
        time.sleep(5)

        soup = BeautifulSoup(html,'lxml')
        with open('x.html', 'w') as file:
            file.write(html)
        events = soup.find_all('div',class_='event__header')
        for event in events:
            event_type = event.find('span',class_='event__title--type').get_text()
            event_name = event.find('span',class_='event__title--name').get_text()
            

        with open('x.html','r') as html:
            print('fetching...')
            soup = BeautifulSoup(html,'lxml')
            content = soup.find('div',class_='sportName soccer')
            data=[]
            for child in content.children:
                game = {}
                try:

                    if 'event__header' in child.attrs['class']:
                        event_type=''
                        event_name=''
                        title = ''
                        try:
                            event_type = child.find('span',class_='event__title--type').get_text()
                            event_name = child.find('span',class_='event__title--name').get_text()
                            title = (event_type +': ' + event_name)

                        except:
                            pass            

                    elif 'event__match' in child.attrs['class']:
                        match_id = child.attrs['id']
                        home_team = child.find('div',class_='event__participant--home').get_text()
                        away_team = child.find('div',class_='event__participant--away').get_text()
                        home_score = None
                        away_score = None
                        stage = ''
                        event_time = ''
                        try:
                            home_odds = float(child.find('div',class_='event__odd--odd1').get_text().strip('-'))
                        except ValueError:
                            home_odds = None
                        try:
                            draw_odds = float(child.find('div',class_='event__odd--odd2').get_text().strip('-'))
                        except ValueError:
                            draw_odds = None
                        try:
                            away_odds = float(child.find('div',class_='event__odd--odd3').get_text().strip('-'))
                        except ValueError:
                            away_odds = None
                        if 'event__match--scheduled' in child.attrs['class']:
                            stage = 'sche'

                            event_time = f"{date} {child.find('div',class_='event__time').get_text()[:5]}:00.000000+03:00"
                        elif 'event__match--live' in child.attrs['class']:
                            stage = 'li'
                            home_score = int(child.find('div',class_='event__score--home').get_text())
                            away_score = int(child.find('div',class_='event__score--away').get_text())
                            event_time = str(timezone.now())
                        else:
                            event_time = str(timezone.now())
                            stage = child.find('div', class_='event__stage--block').get_text()
                            if stage == 'Finished':
                                stage = 'fin'
                                home_score = int(child.find('div',class_='event__score--home').get_text())
                                away_score = int(child.find('div',class_='event__score--away').get_text())
                                
                            #TODO: cancelled and postponed and after penalty and pending
                    
                        
                        game = {"match_id":match_id,"title":title,"home":home_team,"away":away_team,"time":event_time,"home_odds":home_odds,"draw_odds":draw_odds,"away_odds":away_odds,"stage":stage,"home_score":home_score,"away_score":away_score}
                except Exception:
                    pass

                if game != {}:
                    if game['home_odds'] and game['draw_odds']:
                        data.append(game)

        return data

    data=collectdata(datetime.datetime.today().date())



    return data

def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")