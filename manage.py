from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)


def create_app():
    from app.App import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


# DATABASE
def create():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Init db
    db = SQLAlchemy(app)
    db.init_app(app)
    return db


# MARSHMALLOW Init ma
def marsh():
    ma = Marshmallow(app)
    return ma


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)







# create
# curl -i -X GET http://127.0.0.1:5000/api/create
# curl -i -X POST -H 'Content-Type:application/json' -d '{"instancecount":"3","imageid":"ami-06e441c14766d8bb7","instancetype":"t3.nano","keyname":"ec2-keypair","securitygroup":"default","spotprice":"0.0020","tvalue":"rest-api-test"}' http://127.0.0.1:5000/api/create
# curl -i -X DELETE -H "Content-Type: application/json" -d '{"instanceid":"i-0cc6f29fe2466fcdf"}' http://127.0.0.1:5000/api/create

# volume
# curl -i -X GET http://127.0.0.1:5000/api/volume
# curl -i -X POST -H 'Content-Type: application/json' -d '{"tvalue": "rest-api-vol1"}' http://127.0.0.1:5000/api/volume
# curl -i -X PUT -H "Content-Type: application/json" -d '{"volumeid":"vol-0632869f1e7380dce","instanceid":"i-02b963d6c931a9328"}' http://127.0.0.1:5000/api/volume
# curl -i -X DELETE -H "Content-Type: application/json" -d '{"volumeid":"vol-0632869f1e7380dce"}' http://127.0.0.1:5000/api/volume

# keypair
# curl -i -X GET http://127.0.0.1:5000/api/keypair
# curl -i -X POST -H 'Content-Type: application/json' -d '{"keypair": "my-key-pair"}' http://127.0.0.1:5000/api/keypair
# curl -i -X DELETE -H "Content-Type: application/json" -d '{"keypair":"my-key-pair"}' http://127.0.0.1:5000/api/keypair


# netstat -tulpn
# fuser -k 5000/tcp
# aws ec2 terminate-instances --instance-ids i-0eaf09a668921ad3c i-004f7c10bec0908e3 i-0487529bf8b27fe01
