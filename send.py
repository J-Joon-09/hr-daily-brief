import os, json, requests

def send(webhook_url, digest, full):
    text = f"{digest}\n\n─────────────\n\n{full}"
    r = requests.post(webhook_url,
        data=json.dumps({"text": text}),
        headers={"Content-Type": "application/json"}, timeout=10)
    r.raise_for_status()
    print("✅ 슬랙 발송 완료")

if __name__ == "__main__":
    digest = open("digest.txt", encoding="utf-8").read()
    full = open("full.txt", encoding="utf-8").read()
    send(os.environ["SLACK_WEBHOOK_URL"], digest, full)
