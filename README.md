
# Website-to-TelegramSavedMessages

A simple web application that allows you to send content directly from a website to your **Telegram Saved Messages** using the [Telethon](https://github.com/LonamiWebs/Telethon) library and a lightweight Flask backend.

---

## 🚀 How to Deploy

### 📦 Installation

1. **Clone the repository** (if applicable)

2. **Install required packages:**

```bash
pip install flask telethon python-dotenv
```

3. **Generate a secure Flask secret key:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

4. **Fix dotenv execution permission (Windows PowerShell only, if needed):**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

5. **Create a virtual environment:**

```bash
python3 -m venv ./venv
```

6. **Activate the virtual environment:**

- On Windows:

  ```bash
  .\venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

7. **Run the app:**

```bash
python app.py
```

---

<details>
  <summary><strong>📍 Deploy Locally (Quick Command Line Guide)</strong></summary>

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
```bash
python3 -m venv ./venv
```
```bash
./venv/Scripts/activate
```
```bash
pip install flask telethon python-dotenv
```
```bash
python app.py
```

</details>

## Creator
Mysticmovies  
Website: [Link](https://mysticmovies.site)<br>
Contact: [Telegram](https://telegram.me/imrankhan95)<br>
Website Contact: [Contact Us](https://mysticmovies.site/contact)
