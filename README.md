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

