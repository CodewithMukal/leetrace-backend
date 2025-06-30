from flask import Flask,jsonify
from flask_cors import CORS
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)
CORS(app)

def getData(user):
    url = f'https://leetcode.com/u/{user}'
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/115 Safari/537.36")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--enable-javascript")

    driver = webdriver.Chrome(options=options)

    data = {
        "status": "error",
        "error": "cant fetch data"
    }
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    questionsDiv = soup.find('div',class_="lc-xl:h-[180px]")
    
    if(questionsDiv):
        print("Got the div!")
        div = questionsDiv.findAll('div',class_=["h-full",'w-[90px]'])
        if(div):
            divs = div[0].find_all('div',class_=["text-sd-foreground", "text-xs", "font-medium"])
            diffdiv = div[1]
            div2 = diffdiv.find_all('div',class_=["text-sd-foreground", "text-xs", "font-medium"])
            allSpans = soup.find_all('span')
            for span in allSpans:
                if(span.text=="Rank"):
                    reqSpan = span.find_next_sibling('span')
                    ranking = reqSpan.text.replace(",","")
                    break
            if(divs):
                totalDiv = divs[0].text
                totalSolved = (totalDiv.split('/'))[0]
                totalQuestions = ((totalDiv.split('/'))[1]).replace('Solved',"")
                totalSubmissions = (divs[6].text).replace(' submission',"")
                acceptanceRate = (divs[1].text).replace("%Acceptance","")
                easy,med,hard = div2[1].text,div2[3].text,div2[5].text
                easySolved,totalEasy = easy.split('/')
                mediumSolved,totalMedium = med.split('/')
                hardSolved,totalHard = hard.split('/')
                data = {
                    'status': 'success',
                    'totalSolved': totalSolved,
                    'totalQuestions': totalQuestions,
                    'easySolved':easySolved,
                    'totalEasy': totalEasy,
                    'mediumSolved': mediumSolved,
                    "totalMedium" : totalMedium,
                    'hardSolved': hardSolved,
                    "totalHard" : totalHard,
                    "acceptanceRate": acceptanceRate,
                    "totalSubmissions": totalSubmissions,
                    'ranking':ranking
                }
    driver.quit()
    return data

@app.route('/api/user/<username>')
def get_user(username):
    data = getData(username)
    return jsonify(data)

if(__name__=="__main__"):
    app.run(debug=True)