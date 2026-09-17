import os, json, requests

def access_token():
    r = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type": "refresh_token",
        "client_id": os.environ["KAKAO_REST_API_KEY"],
        "refresh_token": os.environ["KAKAO_REFRESH_TOKEN"],
        "client_secret": os.environ["KAKAO_CLIENT_SECRET"],
    }, timeout=10)
    r.raise_for_status()
    d = r.json()
    if d.get("refresh_token"):
        print("⚠️ 새 refresh_token 발급됨 → Secret 갱신 필요:", d["refresh_token"])
    return d["access_token"]

def send(token, digest, url):
    tpl = {"object_type": "text", "text": digest[:200],
           "link": {"web_url": url, "mobile_web_url": url},
           "button_title": "전체 브리핑 보기"}
    r = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={"Authorization": f"Bearer {token}"},
        data={"template_object": json.dumps(tpl, ensure_ascii=False)}, timeout=10)
    r.raise_for_status()
    print("✅ 발송 완료")

if __name__ == "__main__":
    digest = open("digest.txt", encoding="utf-8").read()
    send(access_token(), digest, os.environ["FULL_PAGE_URL"])
