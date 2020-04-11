from flask import Flask, render_template, redirect, request
from wtforms import Form, StringField, DecimalField, validators 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<%r, %d>' % (self.name, self.quantity)

class WarehouseForm(Form):
    name = StringField('Name', [validators.required()])
    quantity = DecimalField('Quantity', [validators.required()])

@app.route("/")
def index():
    print(Warehouse.query.all())
    return render_template('index.html', warehouseForm=WarehouseForm(), items=Warehouse.query.all())

@app.route("/deleteItem", methods=('GET', 'POST'))
def deleteItem():
    if request.method == 'POST': 
        req_name = request.values["name"]
        
        record = Warehouse.query.filter_by(name=req_name).first()
        db.session.delete(record)
        db.session.commit()
        
    return redirect('/')

@app.route('/addItem', methods=('GET', 'POST'))
def addItem():
    if request.method == 'POST': 
        # print(request.values)
        req_name = request.values["name"]
        req_quantity = int(request.values["quantity"])
        
        record = Warehouse.query.filter_by(name=req_name).first()
        if record is None:
            db.session.add((Warehouse(name=req_name, quantity=req_quantity)))
        else:
            record.quantity = record.quantity + req_quantity

        db.session.commit()
        
    return redirect('/')

db.create_all()
app.run(debug=True) # run server, debug is set to True