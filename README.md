# DirectAdmin Bulk Email Creator with Python
Bulk emails can be created by using the DirectAdmin admin account and password and the accounts.csv

## How to use
Just set `config` variables inside `main.py` and add email accounts to `accounts.csv` and start the code with:
```
python main.py
```

## DirectAdmin Token
You can get access-token by leaving `token` variable blank inside `main.py` or just copy the session token from your saved cookies by logging in to your DirectAdmin panel.
