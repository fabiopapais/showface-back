![logo](./logo.png)
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

- [GET] **/event**

    Returns an event's properties through the event id.

    ```json
    {
        "id": "1",

    }
    ```

- [POST] **/event/new**
    
    Creates a new event and returns the event's properties.
    A .zip file containing the images is **necessary** and should be uploaded in the process along with the JSON for event creation.

    ```json
    {
	"name": "Example Event",
	"photographer": "User",
	"photographerLink": "user.com",
    "userId": 1,
    "userName": "User1"

    }
    ```

- [PUT] **/event/edit**

    Edits an event properties by receiving its ID.

    ```json
    {
	"id": 1,
	"name": "Oscar",
	"photographer": "user2",
	"photographerLink": "user.com"
    }
    ```


- [POST] **/event/images**

    Uploads images to a specific event.

### Recognition

- [POST] **/recognize**

    Receives a single image (.jpg or .png) and an event ID to perform face verification. Returns the matched images links.