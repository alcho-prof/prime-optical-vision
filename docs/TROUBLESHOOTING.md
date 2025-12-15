# Troubleshooting Guide: Running on a Local Network

If you are trying to access the Admin Panel or the website from another device (like a team member's laptop) on the same network, follow these steps.

## 1. Ensure Dependencies are Installed
On the machine where the code is running:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate # Windows

# Install dependencies
pip install -r requirements.txt
```

## 2. Prepare the Database (If new)
If you "pulled from GitHub" and do not have the `db.sqlite3` file (or want to ensure it is up to date):
```bash
cd backend
python manage.py migrate
```

## 3. Create an Admin User
If you haven't created a login yet:
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username (e.g., `admin`) and password.

## 4. Run the Server for Network Access
By default, `runserver` only allows access from the same computer (`localhost`). To allow access from other laptops:

```bash
python manage.py runserver 0.0.0.0:8000
```
**Important:** You must use `0.0.0.0:8000`.

## 5. Access from Team Member's Laptop
1. Find the **Local IP Address** of the computer running the server:
   * **macOS:** System Settings > Network > Wi-Fi > Details (e.g., `192.168.1.5`)
   * **Windows:** Run `ipconfig` in terminal.
   
2. On the team member's laptop, open the browser and go to:
   `http://<YOUR_IP_ADDRESS>:8000/admin/`
   
   Example: `http://192.168.1.5:8000/admin/`

## Common Issues
* **"Site can't be reached":** 
    * Ensure both laptops are on the **same Wi-Fi**.
    * Check if a **Firewall** is blocking port 8000.
* **"Server Error (500)":** Check the terminal where `runserver` is running for error messages.
* **"CSRF Failed":** We have updated the settings to allow local network requests. Restart the server if you haven't.
