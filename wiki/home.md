**このプロジェクトは趣味で作成しています。[timmccool](https://github.com/TimMcCool)やScratch teamからの承認、協力されていません。**

# 環境構築
- [python](https://www.python.org/downloads)をダウンロード
- Scratchattachplusのインストール

コマンドプロンプトまたはシェルで:
```
pip install scratchattachplus
```

# scratchattachも使用可能！
同時にScratchAttachも利用可能です。
```python
import scratchattachplus as sp

sp.login("username","password") #ScratchAttachの関数
```
ScratchAttachのコマンドリストは[こちら](https://github.com/TimMcCool/scratchattach)
私が作成した日本語まとめは[こちら](https://note.com/kakeruzoku/n/n3898a84187a8?magazine_key=m35df18cbe97d)

# ScratchAttachからの移行
ScratchAttachから移行しよう！

このプロジェクトではScratchattachを直接読み込んでいるのでバグの発生は起こりません。

scratchattachのインポートをscratchattachplusに書き換えるだけです!
```
- import scratchattach as scratch3
+ import scratchattachplus as scratch3
```

# コメント
コメントをオブジェクトとして作成できます。
```python
import scratchattachplus as sp

#コメントのタイプ
comment_type.project
comment_type.studio
comment_type.user

c = comment(object:Project|Studio|User,comment_id:int)
c = object.get_comment_object(comment_id:int) #objectはProject/Studio/User
#オブジェクトのリストとして
c = get_comments(objects:Project|Studio|User, limit:int|None=None, offset:int=0)
c = object.comments_object(comment_id:int) #objectはProject/Studio/User

c.type|comment_type #コメント元のタイプ
c.location:Project|Studio|User #コメント元のオブジェクト
c.parent_id:int #返信元ID
c.commentee_id:int #メンション先
c.content:str #内容
c.id:int #コメントID
c.datetime:datetime.datetime #送信時間
c.author:User #コメント送信者のオブジェクト(断片的,ログイン情報は引き継ぎます。)
c.reply_count:int #返信数
c.update_author() #c.authorのデータを完全にします。
c.update() #コメントオブジェクトのアップデート
c.reply(content, commentee:User|str|int|None=None) #返信する
c.delete() # もし c.type が comment_type.studio ならば使用できません。
c.report() #セッションが必要です。
c.get_dict() #Scratchの生APIデータ形式のdictを返します。
```

# 報告
正しく報告を実行してください。
```python
import scratchattachplus as sp

class User_report_type(Enum):
    username = 0
    icon = 1
    about_me = 2
    working_on = 3

sp.user_report(session,username:str,types:User_report_type)
#または
User.report(type:User_report_type)

class Studio_report_type(Enum):
    title = 0
    description = 1
    thumbnail = 2

sp.studio_report(session:Session,studioid:str,types:Studio_report_type)
#または
Studio.report(type:Studio_report_type)

comment.report()
```

# クラス
```python
import scratchattachplus as sp

scclass = sp.scratch_class(classid:int,session:Session|None=None,update:bool=True,_token:str|None=None)
#または
scclass = sp.scratch_class_from_token(token:str,session:Session|None=None)

scclass.id #クラスID
scclass.title #クラスのタイトル
scclass.about_class #クラスについて
scclass.working_on #今取り組んでいること
scclass.datetime #datetime.datetime 作成された時間
scclass.author #User クラスのオーナーのユーザー名
scclass.token #クラスのトークン(scratch_class_from_tokenから作成されたか、引数_tokenに入力された値)
scclass.update() #アップデート

scclass._update_from_dict(dict:dict) #dictからアップデート
scclass.get_dict() #dictを取得
scclass.create_student_account(username:str,password:str,country:str="Japan",year:int=2000,month:int=1) #アカウントを作成
create_student_account(invite_id:str,username:str,password:str,**dict) #代用可能
```

#クラウド変数
```py
scratchattach_reqests(conn:CloudConnection,content:str|list,**options) #ScrachAttachでリクエストを送信する(サーバーではありません！)
#または
conn.scratchattach_reqests(content:str|list,**options)
```

#エラー
```py
class ResponseError(requests.HTTPError):
    """
    サーバーからの返答で失敗した時に送出されます。
    """

class NoSessionError(Exception):
    """
    セッションが必要な関数で、セッションが登録されていないときに送出されます。
    """

class InvalidUsername(Exception):
    """
    ユーザー名が無効である(アカウント登録)
    """
```