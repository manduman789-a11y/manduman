# flask-board

로그인/회원가입/게시글/댓글이 되는 최소 Flask 보드.

## 빠른 시작 (개발)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env
FLASK_APP=app flask db_init

gunicorn -w 3 -b 0.0.0.0:8000 wsgi:app
```

## 배포
- Gunicorn systemd 유닛 예시는 인프라 레포를 참고하세요.
