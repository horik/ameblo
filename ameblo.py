import requests
import json
from bs4 import BeautifulSoup


class Ameblo:
    def __init__(self, ameba_id, ameba_password):
        self.ameba_id = ameba_id
        self.ameba_password = ameba_password
        self.session = requests.session()
        self.login()

    def login(self):
        try:
            data = {
                "serviceId": "",
                "amebaId": self.ameba_id,
                "password": self.ameba_password,
                "Submit.x":	"",
                "Submit.y":	""}
            self.session.post("http://www.ameba.jp/login.do", data=data)
        except:
            print("ログインエラー")

    def new_article(self, data):
        try:
            resp = self.session.get("http://blog.ameba.jp/ucs/entry/srventryinsertinput.do")
            soup = BeautifulSoup(resp.text, "html.parser")
            token = soup.find('input', attrs={"name": "token"})
            base_data = {
                "token": token.get("value"),
                "entry_id": 0,
                "blog_name": "beauful",
                "editor_flg": 5,
                "prId": "",
                "netaFlg": "",
                "entry_created_datetime": "current",
                "publish_flg": 0,
                "hashtag": "",
                "entry_title": "hello",
                "theme_id": 10097115514,
                "theme_name": "",
                "entry_text": "<p>world</p>",
                "editMode": "source",
                "editorStyle": "white",
                "thumbnail": ""}
            base_data.update(data)
            resp = self.session.post("http://blog.ameba.jp/ucs/entry/srventryinsertend.do", data=base_data)
            soup = BeautifulSoup(resp.text, "html.parser")
            if soup.select("#subContentsArea > h1").__len__() > 0:
                return True
            else:
                result = soup.select("#entryCreate > span.error")
                if result.__len__() > 0:
                    print(result[0].text.strip())
            return False
        except:
            print("投稿エラー")
            return False

    def upload_image(self, url):
        try:
            file_name = url.split('/')[-1]
            resp = requests.get(url)
            files = {"file": (file_name, resp.content)}
            resp = self.session.post("http://blog.ameba.jp/api/editor/image/upload", files=files)
            return json.loads(resp.text)
        except:
            print("画像投稿エラー")
            return False
