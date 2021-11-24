import os

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

@app.route("/hello")
def hello():
    return "Hello world!"

@app.route('/<int:baz>', methods=['POST'])
def post_foobar(baz):
    return 'you posted {}\n'.format(baz)

@app.route('/analyze/test', methods=['GET'])
def get_json_from_dictionary():
    dic = {
        'foo': 'bar',
        'ほげ': 'ふが'
    }
    return jsonify(dic)  # JSONをレスポンス

@app.route('/analyze/test/post', methods=['POST'])
def post_json():
    jsonData = request.get_json(force=True)  # POSTされたJSONを取得
    return jsonify(jsonData)  # JSONをレスポンス


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)