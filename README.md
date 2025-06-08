# Website-to-telegramsavedmessages
____________________________________
How to Deploy

| pip install flask telethon python-dotenv
| python -c "import secrets; print(secrets.token_hex(32))" {--- to get FLASK_SECRET}
| Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process {if terminal or cmd is not giving permission for dotenv}
| python3 -m venv ./venv
| python app.py


<details>
  <summary><b>Deploy Locally :</b></summary>
<br>
```sh
pip install flask telethon python-dotenv
python -c "import secrets; print(secrets.token_hex(32))"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
python3 -m venv ./venv
./venv/Scripts/activate
python app.py
```
</details>
