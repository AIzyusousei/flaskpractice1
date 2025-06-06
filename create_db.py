#新たにテーブルを作成するたびに実行するファイル（これにより既存テーブルはいじられない）

from plana import app, db
from plana.models import Employee

with app.app_context():
    db.create_all()