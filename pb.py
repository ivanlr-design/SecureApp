import requests
def Download():
    s = requests.get("https://raw.githubusercontent.com/ivanlr-design/SecureApp/main/UI.ui?token=GHSAT0AAAAAACJK2D66NIQYBPYQGOYD52POZL7GBNA")
    if s.status_code == 200:
        return s.text
s = Download()
with open("UI.ui","w") as file:
    file.write(s)