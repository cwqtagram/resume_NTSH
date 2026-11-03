from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# 建立中韓題庫
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "감사합니다": "謝謝",
    "對不起": "죄송합니다",
    "죄송합니다": "對不起",
    "早安": "좋은 아침",
    "좋은 아침": "早安",
    "晚安": "안녕히 주무세요",
    "안녕히 주무세요": "晚安",
    "老師": "선생님",
    "선생님": "老師",
    "學生": "학생",
    "학생": "學生",
    "朋友": "친구",
    "친구": "朋友",
    "家人": "가족",
    "가족": "家人",
    "愛": "사랑",
    "사랑": "愛"
}

# 建立中日題庫
zh_ja_dict = {
    "你好": "こんにちは",
    "こんにちは": "你好",
    "謝謝": "ありがとう",
    "ありがとう": "謝謝",
    "對不起": "ごめんなさい",
    "ごめんなさい": "對不起",
    "早安": "おはようございます",
    "おはようございます": "早安",
    "晚安": "おやすみなさい",
    "おやすみなさい": "晚安",
    "老師": "先生",
    "先生": "老師",
    "學生": "学生",
    "学生": "學生",
    "朋友": "友達",
    "友達": "朋友",
    "家人": "家族",
    "家族": "家人",
    "愛": "愛"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/competition')
def competition():
    return render_template('competition.html')


# 中翻韓
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個詞的韓文對應。")

        return render_template('ask.html', question=question, answer=answer)

    return render_template('ask.html', question="", answer="")


# 中翻日
@app.route('/ask2', methods=['GET', 'POST'])
def ask2():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = zh_ja_dict.get(question, "抱歉，我目前沒有這個詞的日文對應。")

        return render_template('ask2.html', question=question, answer=answer)

    return render_template('ask2.html', question="", answer="")


# 課外活動
@app.route('/activities', methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        answer = "抱歉，我目前沒有這個詞的對應答案。"

        return render_template('activities.html', question=question, answer=answer)

    return render_template('activities.html', question="", answer="")


# 股票查詢
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        try:
            url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo={question}"

            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()

            if data["stat"] == "OK" and data.get("data"):
                answer = data["data"][-1][6]
            else:
                answer = "查無資料，請確認股票代號。"

        except requests.RequestException:
            answer = "目前無法連接股票查詢服務，請稍後再試。"
        except (ValueError, KeyError, IndexError):
            answer = "資料讀取失敗，請稍後再試。"

        return render_template('stock.html', question=question, answer=answer)

    return render_template('stock.html', question="", answer="")


@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


@app.route('/club')
def club():
    return render_template('club.html')


@app.route('/electives')
def electives():
    return render_template('electives.html')


@app.route('/ai')
def ai():
    return render_template('ai.html')


if __name__ == '__main__':
    app.run(debug=True)
