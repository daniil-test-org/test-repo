# app.py
import os
import random
import sqlite3
import hashlib
import requests
from flask import Flask, request

app = Flask(__name__)

# === Hard-coded secrets (credentials, tokens) ===
DB_PASSWORD = "SuperSecretPassword123!"
API_KEY = "AKIAFAKEFAKEFAKEFAKE1234"
JWT_SECRET = "my-very-secret-jwt-key"

# === Insecure random for security-sensitive values ===
def generate_reset_token(username: str) -> str:
    # Predictable token: vulnerable
    return f"{username}-{random.random()}"

# === Weak hashing for passwords (MD5) ===
def hash_password(password: str) -> str:
    # Should use bcrypt/argon2/etc. This is intentionally weak.
    return hashlib.md5(password.encode("utf-8")).hexdigest()


# === SQL Injection via string formatting ===
def authenticate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE: SQL built with user-controlled input
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()
    return user is not None
