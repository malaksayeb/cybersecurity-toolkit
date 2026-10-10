import hashlib
import math
import requests


def calculate_entropy(password: str) -> float:
  """Calcule l'entropie d'un mot de passe en fonction du jeu de caractères."""
  if not password:
    return 0.0

  charset_size = 0
  has_lower = any(c.islower() for c in password)
  has_upper = any(c.isupper() for c in password)
  has_digit = any(c.isdigit() for c in password)
  has_special = any(not c.isalnum() for c in password)

  if has_lower:
    charset_size += 26
  if has_upper:
    charset_size += 26
  if has_digit:
    charset_size += 10
  if has_special:
    charset_size += 32

  entropy = len(password) * math.log2(charset_size if charset_size > 0 else 1)
  return round(entropy, 2)


def check_pwned_password(password: str) -> int:
  """Vérifie si le mot de passe apparaît dans des fuites de données (HIBP)."""
  sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
  prefix, suffix = sha1_password[:5], sha1_password[5:]

  url = f"https://api.pwnedpasswords.com/range/{prefix}"
  try:
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
      return -1

    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
      if h == suffix:
        return int(count)
    return 0
  except Exception:
    return -1