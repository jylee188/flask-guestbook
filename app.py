from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 메모리에 방명록 데이터 저장 (재시작 시 초기화)
guestbook_entries = [
    {"name": "애플실리콘", "message": "맥북 M시리즈에서 작성한 방명록입니다! 🚀"},
    {"name": "깃허브액션", "message": "인텔 우분투 가상머신에서 빌드 완료되었습니다. 🛠️"}
]

@app.route('/')
def index():
    return render_template('index.html', entries=guestbook_entries)

@app.route('/post', methods=['POST'])
def post_message():
    name = request.form.get('name')
    message = request.form.get('message')
    if name and message:
        guestbook_entries.append({"name": name, "message": message})
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 도커 환경에서 외부 접근이 가능하도록 0.0.0.0 포트로 실행
    app.run(host='0.0.0.0', port=5000)