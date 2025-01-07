# showface-back
ShowFace REST API backend

### Setup

```bash
python -m venv venv
```

- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

- Install Flask and dependencies:
```bash
pip install -r requirements.txt
```

- Setup flask SQLite database:
```bash
    flask db init
    flask db upgrade
```