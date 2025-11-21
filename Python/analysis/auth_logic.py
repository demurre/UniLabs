import hashlib
import math
from typing import Dict
from vigenere_cipher import VigenereCipher


def encrypt_password_lg(pw: str, a: float = 2.0) -> str:
    """
    Password encryption using the formula: lg(a*x), where a is the coefficient, x is the symbol value.
    Returns a hash for secure storage.
    """
    encrypted_values = []
    for char in pw:
        x = ord(char)
        try:
            encrypted = math.log10(a * x) if (a * x) > 0 else 0
            encrypted_values.append(str(encrypted))
        except ValueError:
            encrypted_values.append("0")

    combined = "|".join(encrypted_values)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def hash_pw(pw: str) -> str:
    """SHA-256 hash of password (for demonstration, compatibility with existing code)."""
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def check_variant2_letters(pw: str) -> bool:
    """
    Check variant 2: at least one lowercase and at least one uppercase letter.
    Supports unicode (Latin + Cyrillic).
    """
    has_lower = any(ch.islower() for ch in pw)
    has_upper = any(ch.isupper() for ch in pw)
    return has_lower and has_upper


def check_password_strength(pw: str) -> tuple:
    """
    Analyzes password strength.
    Returns (is_strong, message)
    """
    if len(pw) < 8:
        return False, "Password must be at least 8 characters"

    has_lower = any(ch.islower() for ch in pw)
    has_upper = any(ch.isupper() for ch in pw)
    has_digit = any(ch.isdigit() for ch in pw)
    has_special = any(ch in "!@#$%^&*()_+-=[]{}|;:',.<>?" for ch in pw)

    strength_items = sum([has_lower, has_upper, has_digit, has_special])

    if strength_items >= 3 and has_lower and has_upper:
        return True, "Strong password"
    elif strength_items >= 2:
        return True, "Medium password"
    else:
        return False, "Weak password"


def verify_password(stored_hash: str, provided_pw: str) -> bool:
    """Check hashes (empty stored_hash means password is not set)."""
    if stored_hash == "":
        return False
    return hash_pw(provided_pw) == stored_hash


def check_access_level(user_level: int, required_level: int) -> bool:
    """Check access: user_level must be >= required_level"""
    return user_level >= required_level


def encrypt_vigenere(plaintext: str, password: str) -> str:
    """
    Encrypts text using Vigenere cipher based on password.

    Args:
        plaintext: text to encrypt
        password: password (key)

    Returns:
        encrypted text
    """
    try:
        key = VigenereCipher.generate_key_from_password(password)
        cipher = VigenereCipher(key)
        return cipher.encrypt(plaintext)
    except ValueError as e:
        raise ValueError(f"Encryption error: {str(e)}")


def decrypt_vigenere(ciphertext: str, password: str) -> str:
    """
    Decrypts text encrypted with Vigenere cipher.

    Args:
        ciphertext: encrypted text
        password: password (key)

    Returns:
        decrypted text
    """
    try:
        key = VigenereCipher.generate_key_from_password(password)
        cipher = VigenereCipher(key)
        return cipher.decrypt(ciphertext)
    except ValueError as e:
        raise ValueError(f"Decryption error: {str(e)}")
