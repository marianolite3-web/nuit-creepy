# -*- coding: utf-8 -*-
"""Publication TikTok via l'API Zernio (https://zernio.com/api) : upload de la vidéo puis publication directe."""
import os, sys, json, requests
API = os.environ.get("ZERNIO_API", "https://zernio.com/api")
KEY = os.environ.get("ZERNIO_API_KEY", "").strip()
H = {"Authorization": "Bearer " + KEY}

def tiktok_account_id():
    acc = os.environ.get("ZERNIO_ACCOUNT_ID", "").strip()
    if acc: return acc
    r = requests.get(f"{API}/v1/accounts", headers=H, timeout=60); r.raise_for_status(); d = r.json()
    lst = d.get("accounts", d.get("data", [])) if isinstance(d, dict) else d
    for a in lst:
        if str(a.get("platform", "")).lower() == "tiktok": return a.get("_id") or a.get("id") or a.get("accountId")
    raise SystemExit("Aucun compte TikTok lié dans Zernio : connecte-le dans le tableau de bord Zernio.")

def upload(path):
    r = requests.post(f"{API}/v1/media/presign", headers={**H, "Content-Type": "application/json"},
                      json={"filename": os.path.basename(path), "contentType": "video/mp4"}, timeout=60)
    r.raise_for_status(); d = r.json()
    with open(path, "rb") as f:
        p = requests.put(d["uploadUrl"], data=f, headers={"Content-Type": "video/mp4"}, timeout=900)
    p.raise_for_status(); return d["publicUrl"]

def statuses(o):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "status" and isinstance(v, str): out.append(v.lower())
            else: out += statuses(v)
    elif isinstance(o, list):
        for v in o: out += statuses(v)
    return out

def publish(video, caption, ai_label=True):
    url = upload(video); aid = tiktok_account_id()
    body = {"content": caption, "mediaItems": [{"type": "video", "url": url}],
            "platforms": [{"platform": "tiktok", "accountId": aid, "platformSpecificData": {
                "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": True, "allowDuet": True, "allowStitch": True,
                "contentPreviewConfirmed": True, "expressConsentGiven": True, "videoMadeWithAi": bool(ai_label), "draft": False}}],
            "publishNow": True}
    r = requests.post(f"{API}/v1/posts", headers={**H, "Content-Type": "application/json"}, json=body, timeout=600)
    print("HTTP", r.status_code); print(r.text[:2000])
    try: js = r.json()
    except Exception: js = {}
    st = statuses(js)
    ok = r.status_code in (200, 201) and "failed" not in st and "error" not in st
    if not ok: raise SystemExit("Publication échouée (voir réponse ci-dessus).")
    if any(s in ("draft", "inbox") for s in st): print("ATTENTION : TikTok a reçu un brouillon, pas une publication publique.")
    return js
