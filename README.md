#### shop-mini
```
쇼핑몰 웹 애플리케이션
```

+ 주요기능
  + 상품 관리
  + 상품 주문
  + 장바구니
  + 사용자 인증

+ 스택
  + Python
  + Flask
  + MongoDB Atlas

+ 배포
  + AWS Elastic Beanstalk

+ 팀원
  + [Khusan](https://github.com/khu107)
  + [Taehyun Kim](https://github.com/taehyunkim3)
  + [kangsinbeom](https://github.com/kangsinbeom)

#### 시작하기
1. 가상환경 설정  
VScode로 폴더를 오픈한 후 가상환경을 세팅하고 필요한 패키지를 설치하세요.

```
가상환경 세팅 명령어:
  python3 -m venv venv

Flask, MongoDB 설치 명령어:
  pip3 install flask pymongo dnspython
```

2. MongoDB 설정  
루트 폴더에 있는 app.py에 MongoDB 클러스터 URL을 입력하세요.

```
app.py 5번 라인:
  client = MongoClient("MongoDB 클러스터 URL")
```

---


#### Wire Frame


![Untitled](https://github.com/webmini-team8/shop-mini/assets/83047601/df6063cf-4d05-4354-bcd1-7ab0c4ecc862)


---


#### Use Case


![Untitled (2)](https://github.com/webmini-team8/shop-mini/assets/83047601/3a8dd56a-ecb9-4b33-9fc6-6ec4968c3268)

