##쿠산님 코드 시작

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi


ca = certifi.where()
client = MongoClient('mongodb+srv://sparta1:test1@cluster0.kuoqp5o.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta0

# from flask import Flask, render_template, request, jsonify
# app = Flask(__name__)

# from pymongo import MongoClient
# client = MongoClient()
# db = client.dbleolego

@app.route('/')
def home():
    return render_template('index.html')

# 쇼핑몰 상세 페이지 leolego03 ->머지되어 이제 사용안함
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

# 임시 상품 등록 leolego03 -> 머지되어 이제 사용 안함
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

#######
@app.route("/itemdetails", methods=["GET"])   # 아이템 하나 상세정보 모두 불러오기
def item_details():
    itemid_receive = int(request.args.get('itemid_give', False))

    # 아이템 정보 찾기
    item_details = db.shop.find_one({'num': itemid_receive}, {'_id': False})

    if item_details:
        return jsonify({'result': item_details, 'msg': '아이템 정보가 불러와졌습니다'})
    else:
        return jsonify({'msg': '아이템을 찾을 수 없습니다.'})




############################아래가 쿠산님 위에가 성민님
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

    return jsonify({'msg':'succsess'})

@app.route("/shop/cards",methods = ["POST"])
def api_cards():

    num =  request.form["num"]
    # data =list( db.shop.find_one({"num":int(num)}))
    data = list(db.shop.find({'num':int(num)},{'_id':False}))
    
    for i in data:
         db.user.insert_one(i)
    
    
    
    return jsonify({"data":'장바구니에 담았습니다.'})
    
            

@app.route("/shop/cards",methods = ["GET"])
def api_get():
        
        
        user = list(db.user.find({},{'_id':False}))
        

        return jsonify({"status" : user})

@app.route("/shop", methods=["GET"])
def movie_get():

    all = list(db.shop.find({},{'_id':False}))
    
    
    return jsonify({'result':all})

@app.route('/card')
def start():
    return render_template('card.html')

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

    
     return jsonify({'pay':'sucsess'})






if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
