from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/ddns', methods=['POST'])
def ddns():
    hostname = request.form.get('hostname', '')
    # ⚠️ 취약: 사용자 입력을 필터링 없이 시스템 명령어로 실행
    os.system(f"echo Updating DDNS for {hostname}")
    return "DDNS Updated\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

