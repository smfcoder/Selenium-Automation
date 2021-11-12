from flask import Flask,jsonify
from Modules.automate_web_page import perform_automation
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toolsqa.sqlite3'
app.config['SECRET_KEY'] = "QWERTYUIOP987654321ZXCVBNM"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class validation_records(db.Model):
    id = db.Column('validation_record_id', db.Integer, primary_key = True)
    application_name = db.Column(db.String())
    application_url = db.Column(db.String())
    status = db.Column(db.String()) 
    comment = db.Column(db.String())
    validation_time = db.Column(db.Integer())
    validated_at = db.Column(db.String())

    def __init__(self, application_name, application_url, status, comment, validation_time, validated_at):
        self.application_name = application_name
        self.application_url = application_url
        self.status = status
        self.comment = comment
        self.validation_time = validation_time
        self.validated_at = validated_at


@app.route('/')
def home():
    return(
        "<html><body><center><h1>Welcome to Automation</h1></center></body></html>"
    )


@app.route('/run')
def run():
    res = perform_automation()
    query = validation_records(application_name=res['Validated_page'],application_url = res['Application_url'],status = res['Status'],comment = res['Comment'],validation_time = res['Validation_time'],validated_at = res['Validated_at'])
    db.session.add(query)
    db.session.commit()
    return(jsonify(res))

@app.route('/data')
def data():
    records = validation_records.query.all()
    all_records = []
    for i in records:
        temp = {}
        temp["id"] = i.id
        temp["application_name"] = i.application_name
        temp["application_url"] = i.application_url
        temp["status"] = i.status
        temp["comment"] = i.comment
        temp["validation_time"] = i.validation_time
        temp["validated_at"] = i.validated_at
        all_records.append(temp)
    return(jsonify(all_records))



if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)  