from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'shopping_list'

mysql = MySQL(app)

@app.route("/")
def hello_world():
    shopping_list_id = 1
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT items.ItemID, items.ItemName, items.Quantity, items.Bought 
        FROM items
        JOIN listitem ON items.ItemID = listitem.ItemID
        WHERE listitem.ShoppingListID = %s
    """, (shopping_list_id,))
    items = cur.fetchall()
    cur.close()
    return render_template('index.html', items=items)

@app.route("/add_item", methods=["POST"])
def add_item():
    name = request.form['item_name']
    quantity = request.form['quantity']
    shopping_list_id = 1
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (ItemName, Quantity, Bought) VALUES (%s, %s, %s)", (name, quantity, 0))
    mysql.connection.commit()
    item_id = cur.lastrowid
    cur.execute("INSERT INTO listitem (ShoppingListID, ItemID) VALUES (%s, %s)", (shopping_list_id, item_id))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True, item={"ItemID": item_id, "ItemName": name, "Quantity": quantity, "Bought": 0})

@app.route("/update_bought/<int:item_id>", methods=["PUT"])
def update_bought(item_id):
    data = request.get_json()
    bought = 1 if data['bought'] else 0
    cur = mysql.connection.cursor()
    cur.execute("UPDATE items SET Bought = %s WHERE ItemID = %s", (bought, item_id))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)

@app.route("/delete_item/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    shopping_list_id = 1
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM listitem WHERE ShoppingListID = %s AND ItemID = %s", (shopping_list_id, item_id))
    mysql.connection.commit()
    cur.execute("DELETE FROM items WHERE ItemID = %s", (item_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)

