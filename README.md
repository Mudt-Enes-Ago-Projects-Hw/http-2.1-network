# Flask Blog API

A simple Flask REST API with user signup and login (using bcrypt and JWT), and blog posting features.  
Built with SQLAlchemy ORM, environment-based config, and clean project structure.

## Setup

1. Create a Python virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate         # On macOS/Linux
    venv\Scripts\activate            # On Windows (CMD)
    venv\Scripts\Activate.ps1        # On Windows (PowerShell)
    ```
2. Install dependencies:
    ```
    pip install flask sqlalchemy flask_sqlalchemy python-dotenv bcrypt pyjwt
    ```
3. Copy `.env.example` to `.env` and fill your secrets.

4. Run:
    ```
    python app.py
    ```

## Environment Variables

| Name         | Description           | Example                |
|--------------|-----------------------|------------------------|
| JWT_SECRET   | JWT signing secret    | your_super_secret_key  |
| PORT         | API port              | 5000                   |
| SQLITE_DB    | SQLite DB file path   | app.db                 |

## Endpoints

### Auth

- **POST `/signup`**
    - Registers a new user.
    - **Body:** `{ "username": "...", "password": "..." }`
    - **Returns:** Success/failure message.

- **POST `/login`**
    - Logs user in. Sets a JWT token cookie.
    - **Body:** `{ "username": "...", "password": "..." }`
    - **Returns:** Success/failure, JWT as HttpOnly cookie.

### Blog

- **POST `/blog/new`**
    - Create a new blog post. Requires JWT in cookie from login.
    - **Body:** `{ "content": "Your blog content here." }`
    - **Returns:** Success/failure message.

- **GET `/blogs`**
    - Returns all blog posts from all users. Requires JWT in cookie.
    - **Returns:** List of blogs: `{ "blogs": [ ... ] }`
    - Each blog:  
      ```
      {
        "id": int,
        "author": "username",
        "content": "post content",
        "created_at": "timestamp"
      }
      ```

## Project Structure

```
├── app.py
├── .env.example
├── .gitignore
├── src
│   ├── config
│   │   └── settings.py
│   ├── controllers
│   │   ├── auth_controller.py
│   │   └── blog_controller.py
│   └── models
│       ├── db.py
│       ├── user.py
│       └── blog.py
```

## Notes

- JWT tokens are set as HttpOnly cookies for API security.
- Use Postman or similar clients to test all endpoints.
- For production, review proper secret management and HTTPS setup.
