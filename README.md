# Website-to-telegramsavedmessages
____________________________________
How to Deploy

| pip install flask telethon python-dotenv<br>
| python -c "import secrets; print(secrets.token_hex(32))" {--- to get FLASK_SECRET}<br>
| Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process {if terminal or cmd is not giving permission for dotenv}<br>
| python3 -m venv ./venv<br>
| python app.py<br>


<details>
  <summary><b>Deploy Locally :</b></summary>
<br>
  
```sh
python -c "import secrets; print(secrets.token_hex(32))"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
python3 -m venv ./venv
./venv/Scripts/activate
pip install flask telethon python-dotenv
python app.py
```
</details>
