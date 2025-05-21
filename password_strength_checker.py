"""
password_strength_checker.py

This module provides a function to check the strength of a password and provide feedback.

Functions:
    check_password_strength(password): Checks the strength of a password and returns a score, strength text, and feedback.

Usage:
    Import this module and use the check_password_strength function to evaluate password strength.

Example:
    from password_strength_checker import check_password_strength
    score, strength, feedback = check_password_strength("example_password")

Dependencies:
    re: Standard library for regular expression operations.
"""

import re

def check_password_strength(password):
    """
    Check the strength of a password and return a score and feedback.

    Score ranges from 0-100, with categories:
    0-25: Very Weak
    26-50: Weak
    51-75: Medium
    76-100: Strong

    Returns a tuple of (score, strength_text, feedback)
    """
    score = 0
    feedback = []

    # Length check
    if len(password) < 8:
        feedback.append("Password is too short (at least 8 characters recommended)")
    elif len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15

    # Character variety checks
    has_lowercase = any(c.islower() for c in password)
    has_uppercase = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    variety_score = 0
    if has_lowercase:
        variety_score += 10
    else:
        feedback.append("Add lowercase letters")

    if has_uppercase:
        variety_score += 10
    else:
        feedback.append("Add uppercase letters")

    if has_digits:
        variety_score += 10
    else:
        feedback.append("Add numbers")

    if has_special:
        variety_score += 10
    else:
        feedback.append("Add special characters")

    score += variety_score

    # Check for common patterns
    import re

    # Check for consecutive characters
    if re.search(r'(.)\\1{2,}', password):
        feedback.append("Avoid repeating characters")
        score -= 10

    # Check for sequential characters
    sequences = ['abcdefghijklmnopqrstuvwxyz', '0123456789']
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i + 3] in password.lower():
                feedback.append("Avoid sequential characters")
                score -= 10
                break

    # Bonus for longer passwords
    if len(password) > 16:
        score += 10

    # Bonus for high variety
    if has_lowercase and has_uppercase and has_digits and has_special:
        score += 15

    # Ensure score is within bounds
    score = max(0, min(100, score))

    # Determine strength text
    if score <= 25:
        strength_text = "Very Weak"
    elif score <= 50:
        strength_text = "Weak"
    elif score <= 75:
        strength_text = "Medium"
    else:
        strength_text = "Strong"

    return (score, strength_text, feedback)