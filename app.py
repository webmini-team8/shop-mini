from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient("")
db = client.dbleolego


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/mainpage", methods=["POST"])
def guestbook_post():
    name_receive = request.form["name_give"]
    image_receive = request.form["image_give"]
    price_receive = request.form["price_give"]
    num_receive = request.form["num_give"]

    doc = {
        "name": name_receive,
        "image": image_receive,
        "price": price_receive,
        "num": num_receive,
    }

    db.products.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})


@app.route("/mainpage", methods=["GET"])
def guestbook_get():
    all_product = list(db.products.find({}, {"_id": False}))
    return jsonify({"result": all_product})


@app.route("/")
def more_info():
    return render_template("index.html")  # 여기에 상세 페이지 html 넣어야 함


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
