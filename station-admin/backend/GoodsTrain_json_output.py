from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ------------------- DATABASE CONFIG -------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sumuchamp@localhost/train2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- GOODS TRAINS MODEL -------------------
class GoodsTrains(db.Model):
    __tablename__ = 'GoodsTrains'
    Sl_No = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Train_Name = db.Column(db.String(50), nullable=False)
    Train_Status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'Sl_No': self.Sl_No,
            'Train_Name': self.Train_Name,
            'Train_Status': self.Train_Status
        }

# ------------------- ROUTE TO VIEW ALL GOODS TRAINS -------------------
@app.route('/goodstrains', methods=['GET'])
def get_goods_trains():
    trains = GoodsTrains.query.all()
    if not trains:
        return jsonify({'message': 'No goods trains found'}), 404
    return jsonify([train.to_dict() for train in trains])

# ------------------- MAIN -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the table if it doesn't exist
    app.run(debug=True)
