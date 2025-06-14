Building a Simple Authentication System with Python and Flask
# 🔐 Simple Authentication System

A basic web-based authentication system built using **Python**, **Flask**, **SQLite**, and **JWT (JSON Web Tokens)**.  
Users can register, log in, and access a protected page using session-based JWT authentication.

---

## 🚀 Features

- User registration with hashed password storage
- Secure login with JWT token creation
- Route protection using JWT verification
- Flash messages for user feedback
- Basic HTML templates for UI

---

## 📁 Project Structure

```
auth_lab/
├── app.py
├── users.db
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── protected.html
```

---

## ⚙️ Technologies Used

- Python 3
- Flask
- SQLite
- PyJWT
- HTML/CSS (basic)
- hashlib

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/raveenjk/Simple-Authentication-System.git
cd Simple-Authentication-System
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# Activate
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install Flask PyJWT
```

### 4. Run the Application

```bash
python app.py
```

Visit: [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

## 🔐 Routes Overview

| Route        | Description                      | Method |
|--------------|----------------------------------|--------|
| `/`          | Home page                        | GET    |
| `/register`  | User registration page           | GET/POST |
| `/login`     | User login page                  | GET/POST |
| `/protected` | Protected page (JWT required)    | GET    |

---

## 🧪 Testing

- Try registering with an existing username → should see **"Username already exists"**
- Login with wrong credentials → should see **"Invalid username or password"**
- Access `/protected` without logging in → redirected to login with a message
- Wait 30 minutes after login and refresh `/protected` → session expires

---

## ✍️ Author
- [Raveen Madhawa](https://github.com/raveenjk)
![Screenshot 2025-06-14 174556](https://github.com/user-attachments/assets/eae668c8-742c-43bd-8cec-2b158637d7f9)
