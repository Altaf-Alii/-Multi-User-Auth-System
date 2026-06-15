"""
╔══════════════════════════════════════════════════════════╗
║       MULTI-USER AUTHENTICATION SYSTEM                   ║
║       Python Developer Internship Program                ║
║       Hasnain Karimain Educational Academy               ║
╚══════════════════════════════════════════════════════════╝

Features:
  - User Registration (username, email, password)
  - User Login with login attempt limit (3 attempts)
  - Password hashing using SHA-256
  - Email format validation using regex
  - Case-sensitive authentication
  - Role-based access (Admin / User)
  - Password reset functionality
  - Account deletion
  - Prevent duplicate accounts
  - JSON-based data storage
  - Modular functions (separate logic)
"""

import json
import hashlib
import os
import re

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
USERS_FILE      = "users.json"
MAX_ATTEMPTS    = 3          # login attempt limit


# ══════════════════════════════════════════════
#  MODULE 1 — DATA STORAGE
# ══════════════════════════════════════════════

def load_users() -> dict:
    """Load all users from JSON file. Return empty dict if file missing."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users: dict):
    """Save users dictionary back to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# ══════════════════════════════════════════════
#  MODULE 2 — SECURITY
# ══════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hash password using SHA-256 algorithm. Never store plain text."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None


def is_strong_password(password: str) -> bool:
    """
    Password strength rules:
      - Minimum 8 characters
      - At least one uppercase letter (A-Z)
      - At least one lowercase letter (a-z)
      - At least one digit (0-9)
      - At least one special character (!@#$ etc.)
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


# ══════════════════════════════════════════════
#  MODULE 3 — USER REGISTRATION
# ══════════════════════════════════════════════

def register():
    """Register a new user with username, email, password, and role."""
    print("\n╔══════════════════════════════╗")
    print("║       USER REGISTRATION      ║")
    print("╚══════════════════════════════╝")

    users = load_users()

    # ── Username ──────────────────────────────
    username = input("Enter username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return
    if username in users:
        print(f"❌ Username '{username}' already exists. Choose another.")
        return

    # ── Email ─────────────────────────────────
    email = input("Enter email: ").strip()
    if not is_valid_email(email):
        print("❌ Invalid email format. Example: user@gmail.com")
        return
    for data in users.values():
        if data["email"].lower() == email.lower():
            print("❌ This email is already registered.")
            return

    # ── Password ──────────────────────────────
    password = input("Enter password: ").strip()
    if not is_strong_password(password):
        print("❌ Weak password! Password must have:")
        print("   • At least 8 characters")
        print("   • At least one uppercase letter (A-Z)")
        print("   • At least one lowercase letter (a-z)")
        print("   • At least one digit (0-9)")
        print("   • At least one special character (!@#$ etc.)")
        return

    confirm = input("Confirm password: ").strip()
    if password != confirm:
        print("❌ Passwords do not match.")
        return

    # ── Role ──────────────────────────────────
    print("\nSelect role:")
    print("  1. User  (normal access)")
    print("  2. Admin (full access)")
    role_choice = input("Enter choice (1/2): ").strip()
    role = "admin" if role_choice == "2" else "user"

    # ── Save user ─────────────────────────────
    users[username] = {
        "email"          : email,
        "password"       : hash_password(password),
        "role"           : role,
        "login_attempts" : 0,
        "locked"         : False
    }
    save_users(users)
    print(f"\n✅ Account created! Welcome, {username} ({role.upper()})!")


# ══════════════════════════════════════════════
#  MODULE 4 — USER LOGIN
# ══════════════════════════════════════════════

def login():
    """Login with username/email + password. Locks after 3 failed attempts."""
    print("\n╔══════════════════════════════╗")
    print("║          USER LOGIN          ║")
    print("╚══════════════════════════════╝")

    users = load_users()
    if not users:
        print("⚠️  No users registered yet. Please register first.")
        return

    identifier = input("Enter username or email: ").strip()
    password   = input("Enter password: ").strip()

    # Find user by username OR email (case-sensitive for username)
    matched_user = None
    for uname, data in users.items():
        if uname == identifier or data["email"].lower() == identifier.lower():
            matched_user = (uname, data)
            break

    if matched_user is None:
        print("❌ User not found.")
        return

    uname, data = matched_user

    # ── Check if account is locked ────────────
    if data.get("locked", False):
        print(f"🔒 Account '{uname}' is locked due to too many failed attempts.")
        print("   Use 'Reset Password' option to unlock your account.")
        return

    # ── Verify password (case-sensitive) ──────
    if data["password"] == hash_password(password):
        # Reset attempts on success
        users[uname]["login_attempts"] = 0
        save_users(users)
        print(f"\n✅ Login successful! Welcome back, {uname}!")
        print(f"   Role: {data['role'].upper()}")

        # Admin gets extra menu
        if data["role"] == "admin":
            admin_panel(uname)
    else:
        # Increment failed attempts
        users[uname]["login_attempts"] = data.get("login_attempts", 0) + 1
        attempts_left = MAX_ATTEMPTS - users[uname]["login_attempts"]

        if attempts_left <= 0:
            users[uname]["locked"] = True
            save_users(users)
            print(f"🔒 Account locked! Too many failed login attempts.")
            print("   Use 'Reset Password' to unlock.")
        else:
            save_users(users)
            print(f"❌ Incorrect password. {attempts_left} attempt(s) remaining.")


# ══════════════════════════════════════════════
#  MODULE 5 — PASSWORD RESET
# ══════════════════════════════════════════════

def reset_password():
    """Reset password by verifying username and email."""
    print("\n╔══════════════════════════════╗")
    print("║       PASSWORD RESET         ║")
    print("╚══════════════════════════════╝")

    users = load_users()

    username = input("Enter your username: ").strip()
    if username not in users:
        print("❌ Username not found.")
        return

    email = input("Enter your registered email: ").strip()
    if users[username]["email"].lower() != email.lower():
        print("❌ Email does not match our records.")
        return

    # ── Set new password ──────────────────────
    new_password = input("Enter new password: ").strip()
    if not is_strong_password(new_password):
        print("❌ Weak password! Must have 8+ chars, uppercase, lowercase, digit, special char.")
        return

    confirm = input("Confirm new password: ").strip()
    if new_password != confirm:
        print("❌ Passwords do not match.")
        return

    # Update and unlock account
    users[username]["password"]       = hash_password(new_password)
    users[username]["login_attempts"] = 0
    users[username]["locked"]         = False
    save_users(users)
    print("✅ Password reset successful! You can now login.")


# ══════════════════════════════════════════════
#  MODULE 6 — ACCOUNT DELETION
# ══════════════════════════════════════════════

def delete_account():
    """Delete user account after verifying credentials."""
    print("\n╔══════════════════════════════╗")
    print("║       DELETE ACCOUNT         ║")
    print("╚══════════════════════════════╝")

    users = load_users()

    username = input("Enter your username: ").strip()
    if username not in users:
        print("❌ Username not found.")
        return

    password = input("Enter your password: ").strip()
    if users[username]["password"] != hash_password(password):
        print("❌ Incorrect password.")
        return

    confirm = input(f"⚠️  Are you sure you want to delete '{username}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        del users[username]
        save_users(users)
        print("✅ Account deleted successfully.")
    else:
        print("❎ Deletion cancelled.")


# ══════════════════════════════════════════════
#  MODULE 7 — VIEW ALL USERS
# ══════════════════════════════════════════════

def view_all_users():
    """Display all registered users (passwords hidden)."""
    print("\n╔══════════════════════════════╗")
    print("║      REGISTERED USERS        ║")
    print("╚══════════════════════════════╝")

    users = load_users()
    if not users:
        print("No users found.")
        return

    print(f"\n{'#':<4} {'Username':<18} {'Email':<28} {'Role':<8} {'Status'}")
    print("─" * 70)
    for i, (uname, data) in enumerate(users.items(), 1):
        status = "🔒 Locked" if data.get("locked") else "✅ Active"
        print(f"{i:<4} {uname:<18} {data['email']:<28} {data['role']:<8} {status}")


# ══════════════════════════════════════════════
#  MODULE 8 — ADMIN PANEL
# ══════════════════════════════════════════════

def admin_panel(admin_username: str):
    """Special admin panel shown after admin login."""
    while True:
        print(f"\n╔══════════════════════════════╗")
        print(f"║     ADMIN PANEL ({admin_username[:8]})     ║")
        print(f"╚══════════════════════════════╝")
        print("1. View All Users")
        print("2. Delete Any User")
        print("3. Unlock Locked Account")
        print("4. Back to Main Menu")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            view_all_users()

        elif choice == "2":
            users = load_users()
            view_all_users()
            target = input("\nEnter username to delete: ").strip()
            if target not in users:
                print("❌ User not found.")
            elif target == admin_username:
                print("❌ You cannot delete your own account here.")
            else:
                confirm = input(f"Delete '{target}'? (yes/no): ").strip().lower()
                if confirm == "yes":
                    del users[target]
                    save_users(users)
                    print(f"✅ User '{target}' deleted.")

        elif choice == "3":
            users = load_users()
            target = input("Enter username to unlock: ").strip()
            if target not in users:
                print("❌ User not found.")
            else:
                users[target]["locked"]         = False
                users[target]["login_attempts"] = 0
                save_users(users)
                print(f"✅ Account '{target}' unlocked.")

        elif choice == "4":
            break
        else:
            print("⚠️  Invalid choice.")


# ══════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════

def main():
    print("\n" + "═" * 45)
    print("   🔐  MULTI-USER AUTH SYSTEM  🔐")
    print("   Hasnain Karimain Educational Academy")
    print("═" * 45)

    while True:
        print("\n─── MAIN MENU ───")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. View All Users")
        print("5. Delete Account")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if   choice == "1": register()
        elif choice == "2": login()
        elif choice == "3": reset_password()
        elif choice == "4": view_all_users()
        elif choice == "5": delete_account()
        elif choice == "6":
            print("\n👋 Goodbye! Stay secure.")
            break
        else:
            print("⚠️  Invalid choice. Enter 1-6.")


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
