# import requests

# API_URL = "http://localhost:5000/api"
# TOKEN = None

# def set_token(token):
#     global TOKEN
#     TOKEN = token

# def headers():
#     if TOKEN:
#         return {"Authorization": f"Bearer {TOKEN}"}
#     return {}

# # def login(username, password):
# #     r = requests.post(f"{API_URL}/auth/login", json={
# #         "username": username,
# #         "password": password
# #     })
# #     return r.json(), r.status_code

# # def get_catalog():
# #     r = requests.get(f"{API_URL}/catalog", headers=headers())
# #     return r.json()

# # def get_sales():
# #     r = requests.get(f"{API_URL}/sales", headers=headers())
# #     return r.json()

# # def get_users():
# #     r = requests.get(f"{API_URL}/users", headers=headers())
# #     return r.json()

# def login(username, password):
#     return {"access_token": "fake-token", "role": "admin"}, 200

# def get_catalog():
#     return [
#         {"artist": "Pink Floyd", "album": "The Dark Side of the Moon", "price": 1500},
#         {"artist": "The Beatles", "album": "Abbey Road", "price": 1200}
#     ]

# def get_sales():
#     return [{"album": "Abbey Road", "count": 42}]

# def get_users():
#     return [{"username": "admin", "role": "admin"},
#             {"username": "user1", "role": "employee"}]

import requests
import json
import os
from copy import deepcopy
from datetime import datetime
from typing import Tuple, Any, Dict, List, Optional

# Настройки
BASE_URL = os.getenv("VINYLPARC_API_URL", "http://localhost:5000/api")
ONLINE = True
AUTO_FALLBACK = True
TIMEOUT = 6
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".vinylparc_client.json")

# Начальные данные (офлайн)
_initial_users = [
    {"username": "employee1", "password": "pass", "role": "employee"},
    {"username": "admin", "password": "pass", "role": "admin"},
]
_initial_catalog = [
    {"id": 1, "artist": "Pink Floyd", "album": "The Dark Side of the Moon", "price": 1500, "stock": 5},
    {"id": 2, "artist": "The Beatles", "album": "Abbey Road", "price": 1200, "stock": 8},
    {"id": 3, "artist": "Radiohead", "album": "OK Computer", "price": 1300, "stock": 3},
]

_RUNTIME = {
    "token": None,
    "current_user": None,
    "users": deepcopy(_initial_users),
    "catalog": deepcopy(_initial_catalog),
    "last_sync": None
}


# --- persistence ---
def _save_config_blob(blob: dict):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(blob, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("api: save error", e)

def _load_config_blob() -> Optional[dict]:
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("api: load error", e)
        return None

def save_local_profile(profile: dict):
    blob = {
        "profile": profile,
        "catalog": _RUNTIME["catalog"],
        "users": _RUNTIME["users"],
        "last_sync": _RUNTIME.get("last_sync"),
    }
    _save_config_blob(blob)

def load_local_profile() -> Optional[dict]:
    blob = _load_config_blob()
    if not blob:
        return None
    try:
        if "catalog" in blob:
            _RUNTIME["catalog"] = blob["catalog"]
        if "users" in blob:
            _RUNTIME["users"] = blob["users"]
        _RUNTIME["last_sync"] = blob.get("last_sync")
        prof = blob.get("profile")
        if prof:
            _RUNTIME["token"] = prof.get("token")
            _RUNTIME["current_user"] = {"username": prof.get("username"), "role": prof.get("role")}
        return prof
    except Exception:
        return None


# --- config helpers ---
def set_base_url(url: str):
    global BASE_URL
    BASE_URL = url.rstrip("/")
    print(f"api: BASE_URL = {BASE_URL}")

def set_online(flag: bool):
    global ONLINE
    ONLINE = bool(flag)
    print(f"api: ONLINE = {ONLINE}")

def set_auto_fallback(flag: bool):
    global AUTO_FALLBACK
    AUTO_FALLBACK = bool(flag)
    print(f"api: AUTO_FALLBACK = {AUTO_FALLBACK}")


# --- http wrapper ---
def _http_request(method: str, path: str, **kwargs) -> Dict[str, Any]:
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    headers = kwargs.pop("headers", {})
    if _RUNTIME.get("token"):
        headers["Authorization"] = f"Bearer {_RUNTIME['token']}"
    try:
        resp = requests.request(method, url, headers=headers, timeout=TIMEOUT, **kwargs)
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        return {"ok": resp.status_code < 400, "status": resp.status_code, "data": data, "error": None}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "status": None, "data": None, "error": str(e)}


# --- auth ---
def _offline_login(username: str, password: str) -> Tuple[dict, int]:
    for u in _RUNTIME["users"]:
        if u["username"] == username and u["password"] == password:
            token = f"offline-token-{username}-{int(datetime.utcnow().timestamp())}"
            _RUNTIME["token"] = token
            _RUNTIME["current_user"] = {"username": username, "role": u["role"]}
            prof = {"username": username, "role": u["role"], "token": token}
            save_local_profile(prof)
            return {"access_token": token, "role": u["role"], "username": username}, 200
    return {"message": "Invalid credentials (offline)"}, 401

def login(username: str, password: str) -> Tuple[dict, int]:
    if ONLINE:
        resp = _http_request("POST", "/auth/login", json={"username": username, "password": password})
        if resp["ok"] and resp["status"] in (200, 201):
            data = resp["data"]
            token = data.get("access_token") or data.get("token")
            role = data.get("role", "employee")
            _RUNTIME["token"] = token
            _RUNTIME["current_user"] = {"username": username, "role": role}
            save_local_profile({"username": username, "role": role, "token": token})
            return data, resp["status"]
        else:
            if AUTO_FALLBACK:
                return _offline_login(username, password)
            return ({"message": resp.get("error") or resp.get("data") or "login failed"}, resp.get("status") or 503)
    else:
        return _offline_login(username, password)

def logout():
    _RUNTIME["token"] = None
    _RUNTIME["current_user"] = None
    try:
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
    except Exception:
        pass
    return True

def get_profile() -> Optional[dict]:
    return _RUNTIME.get("current_user")


# --- catalog CRUD ---
def get_catalog(force_online: bool = False) -> List[dict]:
    if (ONLINE or force_online):
        resp = _http_request("GET", "/catalog")
        if resp["ok"]:
            data = resp["data"]
            if isinstance(data, list):
                _RUNTIME["catalog"] = data
                _RUNTIME["last_sync"] = datetime.utcnow().isoformat()
                save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                    "role": _RUNTIME.get("current_user", {}).get("role"),
                                    "token": _RUNTIME.get("token")})
                return deepcopy(data)
    # fallback to local cache
    return deepcopy(_RUNTIME["catalog"])

def add_product(artist: str, album: str, price: int, stock: int, force_local: bool = False) -> dict:
    if ONLINE and not force_local:
        resp = _http_request("POST", "/catalog", json={"artist": artist, "album": album, "price": price, "stock": stock})
        if resp["ok"]:
            new = resp["data"]
            try:
                _RUNTIME["catalog"].append(new)
            except Exception:
                pass
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return deepcopy(new)
        else:
            if AUTO_FALLBACK:
                return _add_product_local(artist, album, price, stock)
            raise RuntimeError("Failed to add product online")
    else:
        return _add_product_local(artist, album, price, stock)

def _add_product_local(artist, album, price, stock):
    next_id = max([p["id"] for p in _RUNTIME["catalog"]], default=0) + 1
    new = {"id": next_id, "artist": artist, "album": album, "price": int(price), "stock": int(stock)}
    _RUNTIME["catalog"].append(new)
    save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                        "role": _RUNTIME.get("current_user", {}).get("role"),
                        "token": _RUNTIME.get("token")})
    return deepcopy(new)

def update_product(product_id: int, artist: str, album: str, price: int, stock: int, force_local: bool = False):
    if ONLINE and not force_local:
        resp = _http_request("PUT", f"/catalog/{product_id}", json={"artist": artist, "album": album, "price": price, "stock": stock})
        if resp["ok"]:
            updated = resp["data"]
            for p in _RUNTIME["catalog"]:
                if p["id"] == product_id:
                    p.update(updated)
                    break
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return deepcopy(updated)
        else:
            if AUTO_FALLBACK:
                return _update_product_local(product_id, artist, album, price, stock)
            raise RuntimeError("Failed to update product online")
    else:
        return _update_product_local(product_id, artist, album, price, stock)

def _update_product_local(product_id, artist, album, price, stock):
    for p in _RUNTIME["catalog"]:
        if p["id"] == product_id:
            p.update({"artist": artist, "album": album, "price": int(price), "stock": int(stock)})
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return deepcopy(p)
    raise ValueError("Product not found (local)")

def remove_product(product_id: int, force_local: bool = False):
    if ONLINE and not force_local:
        resp = _http_request("DELETE", f"/catalog/{product_id}")
        if resp["ok"]:
            _RUNTIME["catalog"] = [p for p in _RUNTIME["catalog"] if p["id"] != product_id]
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return True
        else:
            if AUTO_FALLBACK:
                return _remove_product_local(product_id)
            raise RuntimeError("Failed to remove product online")
    else:
        return _remove_product_local(product_id)

def _remove_product_local(product_id):
    _RUNTIME["catalog"] = [p for p in _RUNTIME["catalog"] if p["id"] != product_id]
    save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                        "role": _RUNTIME.get("current_user", {}).get("role"),
                        "token": _RUNTIME.get("token")})
    return True


# --- users (admin) ---
def get_users() -> List[dict]:
    if ONLINE:
        resp = _http_request("GET", "/users")
        if resp["ok"]:
            data = resp["data"]
            if isinstance(data, list):
                _RUNTIME["users"] = data
                save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                    "role": _RUNTIME.get("current_user", {}).get("role"),
                                    "token": _RUNTIME.get("token")})
                # hide passwords if any
                return [{"username": u.get("username"), "role": u.get("role")} for u in data]
    # fallback
    return [{"username": u["username"], "role": u["role"]} for u in _RUNTIME["users"]]

def add_user(username: str, password: str, role: str, force_local: bool = False):
    if ONLINE and not force_local:
        resp = _http_request("POST", "/users", json={"username": username, "password": password, "role": role})
        if resp["ok"]:
            _RUNTIME["users"].append(resp["data"])
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return True
        else:
            if AUTO_FALLBACK:
                return _add_user_local(username, password, role)
            raise RuntimeError("Failed to add user online")
    else:
        return _add_user_local(username, password, role)

def _add_user_local(username, password, role):
    if any(u["username"] == username for u in _RUNTIME["users"]):
        raise ValueError("User exists (local)")
    _RUNTIME["users"].append({"username": username, "password": password, "role": role})
    save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                        "role": _RUNTIME.get("current_user", {}).get("role"),
                        "token": _RUNTIME.get("token")})
    return True

def remove_user(username: str, force_local: bool = False):
    if ONLINE and not force_local:
        resp = _http_request("DELETE", f"/users/{username}")
        if resp["ok"]:
            _RUNTIME["users"] = [u for u in _RUNTIME["users"] if u["username"] != username]
            save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                                "role": _RUNTIME.get("current_user", {}).get("role"),
                                "token": _RUNTIME.get("token")})
            return True
        else:
            if AUTO_FALLBACK:
                return _remove_user_local(username)
            raise RuntimeError("Failed to remove user online")
    else:
        return _remove_user_local(username)

def _remove_user_local(username):
    _RUNTIME["users"] = [u for u in _RUNTIME["users"] if u["username"] != username]
    save_local_profile({"username": _RUNTIME.get("current_user", {}).get("username"),
                        "role": _RUNTIME.get("current_user", {}).get("role"),
                        "token": _RUNTIME.get("token")})
    return True
