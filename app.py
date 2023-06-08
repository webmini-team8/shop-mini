
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)




client = MongoClient(
    'mongodb://sparta:1234@ac-uixemuf-shard-00-00.hhp4n7w.mongodb.net:27017,ac-uixemuf-shard-00-01.hhp4n7w.mongodb.net:27017,ac-uixemuf-shard-00-02.hhp4n7w.mongodb.net:27017/?ssl=true&replicaSet=atlas-1q63nz-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.shoppingmall8


@app.route('/')
def home():
    return render_template('cart.html')


@app.route("/itemsave", methods=["POST"])
def item_save():  #상품 저장

    userid_receive = request.form.get('userid_give', False)
    name_receive = request.form.get('name_give', False)
    quantity_receive = int(request.form.get('quantity_give', False))
    catetory_receive = request.form.get('category_give', False)
    price_receive = int(request.form.get('price_give', False))
    imageurl_receive = request.form.get('imageurl_give', False)
    description_receive = request.form.get('description_give, False')
    
    item_list = list(db.items.find({}, {'_id': False}))
    count = len(item_list) + 1

    doc = {
        'itemid': count,  # 등록 시, db에서 특정 상품을 찾기 위해 'num' 이라는 고유 값 부여
        'userid': userid_receive,
        'name': name_receive,
        'quantity' : quantity_receive,
        'category': catetory_receive,
        'price': price_receive,
        'imageurl': imageurl_receive,
        'description': description_receive
    }
    db.items.insert_one(doc)

    return jsonify({'msg': '상품 등록이 완료되었습니다!'})



@app.route("/itemshow", methods=["GET"]) # 아이템 모두 불러오기
def item_get():
    all_items = list(db.items.find({}, {'_id': False}))
    return jsonify({'result': all_items})


@app.route("/itemdetails", methods=["GET"])   # 아이템 하나 상세정보 모두 불러오기
def item_details():
    itemid_receive = request.form.get('itemid_give', False)

    # 아이템 정보 찾기
    item_details = db.items.find_one({'itemid': itemid_receive}, {'_id': False})

    if item_details:
        return jsonify({'result': item_details, 'msg': '아이템 정보가 불러와졌습니다'})
    else:
        return jsonify({'msg': '아이템을 찾을 수 없습니다.'})



@app.route("/itembycategory", methods=["GET"]) #아이템 카테고리별로 불러오기
def items_by_category():
    category_receive = request.form.get('category_give', False)

    # 해당 카테고리의 아이템 불러오기
    items_in_category = list(db.items.find({'category': category_receive}, {'_id': False}))

    return jsonify({'result': items_in_category, 'msg': '아이템 불러오기 성공'})

#/itemsbycategory?category_give=<category>와 같이 URL의 매개변수로 category를 사용하여 이 경로를 호출해야 합니다.





@app.route("/cartupdate", methods=["POST"]) #카트 업데이트 하기(수량 변동)
def cart_change():
    userid_receive = request.form.get('userid_give', False)
    itemid_receive = request.form.get('itemid_give', False)
    quantity_receive = int(request.form.get('quantity_give', False))
    

    #먼저 해당 아이디의 카트를 찾음
    # user_cart = db.carts.find({'userid' : userid_receive}, {'_id': False})

    #해당 아이템의 수량을 바꿈
    #https://stackoverflow.com/questions/63132280/update-single-array-item-with-matching-id-and-one-of-the-array-element-using-pym
    db.carts.update_one({'userid': userid_receive, 'cart': {'$elemMatch': { 'itemid':  itemid_receive }}}, {'$set': {'cart.$.quantity': quantity_receive}})
    return jsonify({'msg': 'update 완료'})



@app.route("/cartdelete", methods=["POST"]) #카트 아이템 삭제하기
def cart_delete():
    userid_receive = request.form.get('userid_give', False)
    itemid_receive = request.form.get('itemid_give', False)

    db.carts.update({'userid': userid_receive}, { '$pull' :{ 'cart': { 'itemid':  itemid_receive }}} )
    return jsonify({'msg': '상품이 장바구니에서 삭제되었습니다.'})


@app.route("/cartadd", methods=["POST"]) #카트 아이템 추가하기(수량추가 포함)
def cart_add():
    userid_receive = request.form.get('userid_give', False)
    itemid_receive = request.form.get('itemid_give', False)
    quantity_receive = int(request.form.get('quantity_give', False))

    # 사용자의 카트 찾기
    user_cart = db.carts.find_one({'userid': userid_receive})

    # 사용자의 카트가 없으면 새로 생성하기.
    if user_cart is None:
        user_cart = {
            'userid': userid_receive,
            'cart': []
        }
        db.carts.insert_one(user_cart)

    # 사용자의 카트에 추가하려는 아이템이 있나 확인
    if db.carts.find_one({'userid': userid_receive, 'cart.itemid': itemid_receive}):
        # 만약 있으면 수량만 추가
        db.carts.update_one({'userid': userid_receive, 'cart.itemid': itemid_receive}, {'$inc': {'cart.$.quantity': quantity_receive}})
    else:
        # 만약 없으면 새로 추가
        item_info = db.items.find_one({'itemid': itemid_receive}, {'_id': False})  # assuming the items collection has an item document with an 'itemid' field
        item_info['quantity'] = quantity_receive
        db.carts.update_one({'userid': userid_receive}, {'$push': {'cart': item_info}})

    return jsonify({'msg': '상품이 장바구니에 담겼습니다.'})


@app.route("/cartinfo", methods=["GET"])  #카트 정보 불러오기
def cart_info():
    userid_receive = request.form.get('userid_give', False)

    # 사용자의 카트 찾기
    user_cart = db.carts.find_one({'userid': userid_receive}, {'_id': False})

    # 혹시 카트가 없으면 새로 생성하기.
    if user_cart is None:
        user_cart = {
            'userid': userid_receive,
            'cart': []
        }
        db.carts.insert_one(user_cart)

    return jsonify({'result': user_cart, 'msg': '카트 불러오기 성공'})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
