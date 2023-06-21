from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://sparta1:test1@cluster0.kuoqp5o.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta0

@app.route('/')
def home():
    return render_template('index.html')

# 쇼핑몰 상세 페이지 leolego03
@app.route('/view')
def view():
    item_id = request.args.get('itemid')
    view_item = db.shop.find_one({'num': int(item_id)}, {'_id': False})

    return render_template('view.html', view_item = view_item)

# Khusan
@app.route("/shop", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    category_receive = request.form['category_give']
    price_receive = request.form['price_give']
    count_receive = request.form['count_give']
    area_receive = request.form['area_give']

    shop_list = list(db.shop.find({}))
    count = len(shop_list) + 1
    print(type(count))
    doc = {
        'num': count,
        'url':url_receive,
        'name':name_receive,
        'category':category_receive,
        'price':price_receive,
        'count':count_receive,
        'area':area_receive

    }
    db.shop.insert_one(doc)

    return jsonify({'msg':'상품 등록 완료!'})

# Khusan
@app.route("/shop/cards",methods = ["POST"])
def api_cards():
    num =  request.form["num"]
    # data =list( db.shop.find_one({"num":int(num)}))
    data = list(db.shop.find({'num':int(num)},{'_id':False}))
    
    for i in data:
        db.user.insert_one(i)
    
    return jsonify({"data":'장바구니에 담았습니다.'})

# Khusan
@app.route("/shop/cards",methods = ["GET"])
def api_get():
    user = list(db.user.find({},{'_id':False}))
    
    return jsonify({"status" : user})

# Khusan
@app.route("/shop", methods=["GET"])
def movie_get():
    all = list(db.shop.find({},{'_id':False}))
    
    return jsonify({'result':all})

# Khusan
@app.route('/card')
def start():
    return render_template('card.html')

# Khusan
@app.route('/pay', methods=["POST"])
def pay():
    name = request.form['name']
    val = request.form['val']
    address = request.form['address']

    doc = {
        'name':name,
        'val':val,
        'address':address
    }
    db.pay.insert_one(doc)
    db.user.delete_many({})

    return jsonify({'pay':'구매 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)