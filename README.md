# showface-back
ShowFace REST API backend

<details>
<summary><h2>First-time Setup</h2></summary>

1. Create an environment
```bash
python -m venv venv
```

2. On macOS/Linux:
```bash
source venv/bin/activate
```
2. On Windows:
```bash
venv\Scripts\activate
```

3. Install Flask and dependencies:
```bash
pip install -r requirements.txt
```

4. Turn .env.example into .env (configure .env file)

5. Setup flask SQLite database:
```bash
    flask db init
    flask db upgrade
```


6. Run the server
```bash
    python run.py
```

</details>

## Routes
### Authentication and User

- [POST] **/auth/login**

    Logins the user and returns a JWT token
    
    ```json
    {
        "username": "Example",
        "password": "12345678",

    }
    ```

- [POST] **/auth/register**
    
    Register new user and returns a JWT token
    
    ```json
    {
        "username": "Example",
        "password": "12345678",

    }
    ```
