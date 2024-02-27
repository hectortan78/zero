import requests

url = "https://techassessment.blob.core.windows.net/aiap-preparatory-bootcamp/score.db"
r = requests.get(url)
with open('score.db', 'wb') as f:
    f.write(r.content)