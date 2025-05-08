# IH#3 Control     – user decides to register or log in
# IH#2 Cost        – up-front message tells the time/steps required
# IH#7 Accommodation – accepts Enter key alone to reuse previous inputs

import json, os, hashlib, getpass
from pathlib import Path

_USERS = Path("users.json")

def _hash(pw: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}{pw}".encode()).hexdigest()

class AuthManager:
    def __init__(self) -> None:
        self._db: dict[str, str] = {}
        if _USERS.exists():
            self._db = json.loads(_USERS.read_text())

    # ---------- public API ----------
    def register(self) -> str | None:
        print("Register – 2 short steps (≈30 sec)")        # IH#2 Cost
        user = input("Choose a username: ").strip()
        if user in self._db:
            print("That name exists, please log in instead.")  # IH#8 Protection
            return None
        pw = getpass.getpass("Choose a password: ")
        salt = os.urandom(8).hex()
        self._db[user] = f"{salt}${_hash(pw, salt)}"
        self._save()
        print("✓ Account created.  You can now log in.")
        return user

    def login(self) -> str | None:
        user = input("Username (blank = cancel): ").strip()    # IH#7 Accommodation
        if not user:
            return None
        record = self._db.get(user)
        if not record:
            print("No such user.")                            # IH#8 Protection
            return None
        salt, ref = record.split("$")
        pw = getpass.getpass("Password: ")
        if _hash(pw, salt) == ref:
            print("✓ Logged in")
            return user
        print("❌ Incorrect password")
        return None

    # ---------- helpers ----------
    def _save(self) -> None:
        _USERS.write_text(json.dumps(self._db, indent=2))