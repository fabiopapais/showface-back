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

    Logins the user and returns a JWT token. Returns code 401 if invalid credentials.
    
    ```json
    {
        "email": "example@gmail.com",
        "password": "12345678",

    }
    ```

- [POST] **/auth/register**
    
    Register new user and returns a JWT token. Returns code 400 if email already exists.
    
    ```json
    {
        "name": "Example",
        "email": "example@gmail.com",
        "password": "12345678",

    }
    ```

### Events

- [GET] **/events**

    Returns an event properties

- [POST] **/events**
    
    Creates a new event and return its information.

- [POST] **/events**

    Edits an event properties

- [POST] **/events/images**

    Uploads images to a specific event.

### Recognition

- [POST] **/recognize**

    Receives an image and an event ID and performs face verification. Returns the matched images name/IDs. 