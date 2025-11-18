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
    - **Body:** `{ "username": "alice", "password": "secret123" }`
    - **Returns:** Success/failure message.

- **POST `/login`**
    - Logs user in. Sets a JWT token cookie named `jwt` (HttpOnly).
    - **Body:** `{ "username": "alice", "password": "secret123" }`
    - **Returns:** Success/failure. The response includes a `Set-Cookie: jwt=...` header.

- **POST `/logout`**
    - Logs out the user by deleting the jwt cookie.
    - **Returns:** `{ "message": "Logged out" }`

### Blog

- **POST `/blog/new`**
    - Create a new blog post. Requires JWT in cookie from login.
    - **Body:** `{ "content": "Your blog content here." }`
    - **Returns:** Success/failure message (201 created).

- **GET `/blogs`**
    - Returns all blog posts from all users. Requires JWT cookie.
    - **Returns:** List of blogs:
      ```
      {
        "blogs": [
          { "id": int, "author": "username", "content": "post content", "created_at": "timestamp" },
          ...
        ]
      }
      ```

- **PUT/PATCH `/blog/<blog_id>`**
    - Edit a blog post. Only the author (owner) can edit their own blog.
    - **URL example:** `PUT http://localhost:5000/blog/1`
    - **Headers:** `Content-Type: application/json`
    - **Body:** `{ "content": "Updated content for my blog post" }`
    - **Responses:**
      - `200 OK` — blog updated; returns:
        ```
        {
          "message": "Blog post updated",
          "blog": {
            "id": 1,
            "author_id": 2,
            "content": "Updated content...",
            "created_at": "2025-11-18 09:30:07"
          }
        }
        ```
      - `400 Bad Request` — missing or null `content` field.
      - `403 Forbidden` — you are not the owner of the post.
      - `404 Not Found` — blog with the given id doesn't exist.

## How authentication works in this app

- After successful login, the server sets an HttpOnly cookie named `jwt` (contains the JWT).  
- Protected endpoints read the token from `request.cookies.get('jwt')`.
- In Postman, login will populate the cookie jar automatically. Subsequent requests to the same host will include the `jwt` cookie.

## Postman examples

1. Signup
   - POST `http://localhost:5000/signup`
   - Body (JSON):
     ```
     {
       "username": "alice",
       "password": "secret123"
     }
     ```

2. Login
   - POST `http://localhost:5000/login`
   - Body (JSON):
     ```
     {
       "username": "alice",
       "password": "secret123"
     }
     ```
   - Postman saves the `jwt` cookie automatically.

3. Create blog
   - POST `http://localhost:5000/blog/new`
   - Body (JSON):
     ```
     {
       "content": "Alice's first blog post"
     }
     ```

4. Edit blog (only owner)
   - PUT `http://localhost:5000/blog/1`
   - Body (JSON):
     ```
     {
       "content": "Updated content for my blog post"
     }
     ```
   - Ensure Postman has the `jwt` cookie for localhost.

5. Get blogs
   - GET `http://localhost:5000/blogs`

## Security notes

- JWTs are stored in HttpOnly cookies for this demo (not in Authorization header).
- In production, use HTTPS, secure cookie flags, and consider token revocation strategies if needed.

## Project Structure

```
├── app.py
├── .env.example
├── .gitignore
├── README.md
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

- For the edit route, only the blog owner can update the `content`. Attempting to edit another user's blog returns 403 Forbidden.
- Consider adding `updated_at` if you want to track edits.