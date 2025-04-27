# CVE-2023-1389 PoC
TP-Link Archer AX21 Remote Command Injection  

---

## 취약점 개요

- CVE ID : CVE-2023-1389
- 취약 제품 : TP-Link Archer AX21 공유기
- 취약점 종류 : 원격 명령어 삽입 (Remote Command Injection)
- 취약점 설명 : 인증되지 않은 공격자가 웹 관리 인터페이스의 `country` 파라미터를 악용하여 루트 권한으로 임의의 명령어를 실행할 수 있는 취약점

---

## 환경 구성
- 운영체제 : Windows 11 + WSL2 (Ubuntu)
- 주요 도구 : Docker, Docker Compose
- 서버 : Flask 기반 웹 애플리케이션 (Docker container로 실행)

### 디렉토리 구조
```
cve-2023-1389-poc/
 ├── Dockerfile
 ├── docker-compose.yml
 └── app/
     └── server.py
```

### 주요 취약 서버 파일 (app/server.py)
```
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/ddns', methods=['POST'])
def ddns():
    hostname = request.form.get('hostname', '')
    os.system(f"echo Updating DDNS for {hostname}")
    return "DDNS Updated\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

```
사용자 입력값을 필터링 없이 os.system() 함수에 전달하여 명령어 삽입이 가능하다

---

## Poc 실행 흐름

### 1) 공격
![Image](https://github.com/user-attachments/assets/6fda17c9-1b70-448d-8824-41d62d5fbd80)
1. /ddns 경로에 POST 요청을 전송한다
2. hostname 값에 명령어를 삽입한다 [example.com](http://example.com); id 로 기존 명령어를 끝내고 id (현재 사용자 정보)를 출력하는 명령을 실행한다
→ 호스트 네임을 등록하다가 슬쩍 원하는 명령어를 실행하는 것

### 2) 결과 (서버 터미널 로그)
![image](https://github.com/user-attachments/assets/db7c9479-28a4-47e5-8d1f-227f9803fabd)
id 명령어가 정상적으로 실행되었다
이는 명령어 삽입이 성공했음을 의미한다

---

## 대응 방안
TP-Link는 이 취약점을 수정한 펌웨어 버전 1.1.4 Build 20230219를 출시하였다

### 패치 전 서버 코드
```
char cmd[256];
snprintf(cmd, sizeof(cmd), "uci set system.@system[0].country=%s", country);
popen(cmd, "r");
```
/cgi-bin/luci/;stok=/locale 엔드포인트의 country 파라미터가 사용자 입력값으로 받아들여져
popen() 함수에 직접 전달되었고, 이로 인해 공격자가 명령어를 삽입하여 루트 권한으로 실행할 수 있었다

### 패치 후 서버 코드 
```
if (is_valid_country(country)) {
    set_country_config(country);
}
```
is_valid_country() 함수는 입력값이 허용된 국가 코드인지 확인하며
set_country_config() 함수는 안전한 방식으로 설정을 적용한다



## 실행 방법

1) 저장소 클론
```
git clone https://github.com/ohnahee/CVE_2023_1389_poc.git
cd CVE_2023_1389_poc
```  

2) 도커 이미지 빌드 및 컨테이너 실행
```
docker-compose up --build
```

3) 서버가 정상적으로 실행 시, 터미널에 다음과 같은 메시지 출력
```
* Running on http://0.0.0.0:8080
```


---

## 참고 자료 
https://www.cybersecuritydive.com/news/-botnet-exploits-tp-link-router/742319/  
https://nvd.nist.gov/vuln/detail/cve-2023-1389  
https://www.exploit-db.com/exploits/51677  
https://voyag3r-security.medium.com/exploring-cve-2023-1389-rce-in-tp-link-archer-ax21-d7a60f259e94  
https://www.tp-link.com/us/support/download/archer-ax21/  
https://es-la.tenable.com/security/research/tra-2023-11

