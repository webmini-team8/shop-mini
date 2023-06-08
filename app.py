from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient()
db = client.dbleolego

@app.route('/')
def home():
    return render_template('index.html')

# 쇼핑몰 상세 페이지 leolego03
@app.route('/view')
def view():
    item_id = request.args.get('itemid')
    temp_item = db.shop.find_one({'itemId': int(item_id)})

    return render_template('view.html', temp_item = temp_item)

# 쇼핑몰 상세 페이지 상품 leolego03
@app.route('/view/item', methods=["GET"])
def view_get_item():
    temp_item = db.shop.find_one({'itemId': 2})

    return jsonify({'temp_item' : temp_item})

# 쇼핑몰 상세 페이지 상품 저장 leolego03
@app.route('/view/item', methods=["POST"])
def view_post_item():
    item_count = request.form['item_count']

    return jsonify({'msg': item_count + '개 추가 완료!'})

# 임시 상품 등록 leolego03
@app.route('/temp/item', methods=['GET'])
def temp_post_item():
    temp_item = {
        'itemId' : 2,
        'itemImgUrl' : 'https://cdn.pixabay.com/photo/2020/07/15/18/32/sneakers-5408674_1280.png',
        'itemName' : '운동화',
        'itemPrice' : 10000,
        'itemStock' : 99,
        'itemSubTitle': '멋있는 운동화!',
        'itemDescription': '운동화 상세 설명입니다.'
    }

    db.shop.insert_one(temp_item)
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)