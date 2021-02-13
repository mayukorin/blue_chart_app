# Name

青チャート管理システム（仮）  


# Features

画面設計が、Googleドライブのインターン生共有フォルダの「青チャートの画面設計（Django）」にある。 

# Requirement


* Django
* PostgreSQL
* psycopg2
* Pillow

# Installation

Requirementで列挙したライブラリのインストール方法

1. PostgreSQLをインストールする  
1. psycopg2をインストールする  
1. Pillowをインストールする  
1. インストール時に設定したパスワードを使い、コマンドプロンプト（ターミナル）で  PostgreSQLにログイン  
```psql -U postgres```  
1. データベースを所有するためのユーザを作成する
```create role （ユーザ名） with login password (パスワード);```
1. データベースを作成する（4で作成したユーザーを所有者にする）  
```create database （データベース名) with owner (4で作成したユーザ名);```
1. blue_chart_app/config/settings/の下にlocal.pyを作り、以下のように編集する
```
from .base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'データベース名',
        'USER':'4で作成したユーザ名',
        'PASSWORD': '4で作成したユーザのパスワード',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
1. blue_chartディレクトリで、     
```python manage.py makemigrations```  
```python manage.py migrate app1```  
```python manage.py migrate```  
を実行  

1. blue_chartディレクトリで、
```python manage.py loaddata dump.json(別途配布)```
を実行。これにより、4で作成したデータベースにデータをロードできる。

# 注意  
ローカル環境で動作させる場合は、answer_photo_viewの71行目あたりにある
```ret = cloudinary.uploader.destroy(public_id = str(photo.image))```
はコメントアウトしたままにしておくこと
# Usage

```python manage.py runserver```でhttp://127.0.0.1:8000/siteUser/login にアクセス  



