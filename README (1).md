# 🔐 Multi-User Authentication System

**Python Developer Internship Program**  
Hasnain Karimain Educational Academy — Software House & Training Center

---

## 📌 Project Overview

A CLI-based multi-user authentication system built in Python that allows users to register, login, and manage their accounts securely using JSON-based data storage.

---

## ✅ Features

### Core Features
- User Registration (Username, Email, Password)
- User Login with Username or Email
- Secure Password Hashing (SHA-256)
- JSON File Storage (auto-created)

### Advanced Features
- Input validation & error handling
- Case-sensitive authentication
- Email format validation using Regex
- Strong password rules enforcement
- Prevent duplicate username/email
- Modular functions (separate logic per module)

### Bonus Features
- 🔒 Login attempt limit (locks after 3 failed tries)
- 🔑 Password reset functionality
- 🗑️ Account deletion
- 👤 Role-based access (Admin / User)
- 🛡️ Admin Panel (view users, delete users, unlock accounts)

---

## 🚀 How to Run

### Requirements
- Python 3.x (no extra libraries needed)

### Steps

```bash
# Step 1: Go to project folder
cd Desktop\Multi-User Authenticati

# Step 2: Run the program
python auth_system.py
```

---

## 📁 Project Structure

```
Multi-User Authenticati/
│
├── auth_system.py     ← Main Python file
├── users.json         ← Auto-created when first user registers
└── README.md          ← This file
```

---

## 🧠 Code Modules

| Module | Function | Description |
|--------|----------|-------------|
| 1 | `load_users()` / `save_users()` | JSON data storage |
| 2 | `hash_password()` / `is_valid_email()` / `is_strong_password()` | Security & validation |
| 3 | `register()` | New user registration |
| 4 | `login()` | Login with attempt limit |
| 5 | `reset_password()` | Password reset & account unlock |
| 6 | `delete_account()` | Account deletion |
| 7 | `view_all_users()` | Display all users |
| 8 | `admin_panel()` | Admin-only controls |

---

## 🔐 Password Rules

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)
- At least one special character (!@#$ etc.)

**Example valid password:** `Hello@123`

---

## 👤 Role-Based Access

| Feature | User | Admin |
|---------|------|-------|
| Register | ✅ | ✅ |
| Login | ✅ | ✅ |
| Reset Password | ✅ | ✅ |
| Delete Own Account | ✅ | ✅ |
| View All Users | ✅ | ✅ |
| Delete Any User | ❌ | ✅ |
| Unlock Accounts | ❌ | ✅ |

---

## 🛡️ Security

- Passwords are **never stored as plain text**
- SHA-256 hashing is applied before saving
- Account locks after **3 failed login attempts**
- Password reset requires **email verification**

---

## 📦 Deliverables

- ✅ `auth_system.py` — Source code
- ✅ `users.json` — JSON database (auto-generated)
- ✅ `README.md` — Documentation

---

*Built with ❤️ using Python — No external libraries required*
   "Demo vedio"
    https://drive.google.com/file/d/1RUmpbwiBuRr5RlRewSPNYnhxYA2MhJsC/view?usp=sharing