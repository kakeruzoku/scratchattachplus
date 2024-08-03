I use Google Translate and DeepL Translate.

# Building the Environment / 環境構築
- Download [python](https://www.python.org/downloads) / [python](https://www.python.org/downloads)をダウンロード
- install Scratchattachplus
command prompt or shell: コマンドプロンプトまたはシェルで:
```
pip install scratchattachplus
```

# Using scratchattach
Loading scratchattach at the same time. 同時にScratchAttachも利用可能です。
```python
import scratchattachplus as sp

sp.login("username","password") #ScratchAttach function
```
Click [here](https://github.com/TimMcCool/scratchattach) for more information on Scratch Attach

# Migration from scratchattach / ScratchAttachからの移行
Just rewrite the scratchattach import to scratchattachplus!

scratchattachのインポートをscratchattachplusに書き換えるだけです!
```
- import scratchattach as scratch3
+ import scratchattachplus as scratch3
```

# Comment
```python
c = comment(object:Project|Studio|User,comment_id:int)

c.type|str #"p" or "s" or "u"
c.location:Project|Studio|User
c.parent_id:int
c.commentee_id:int
c.content:str
c.id:int
c.datetime:datetime.datetime
c.author:User
c.reply_count:int
c.update_author()
c.update()
c.comment_report()
c.reply(content, commentee:User|str|int|None=None)
c.delete() # if c.type == studio, can't use it.
```

# report
the comments will be deleted after being reported by two accounts. コメントは2アカウントからの報告で削除されます。
```python
import scratchattachplus as sp

sp.user_report(session,username:str,types:int)
"""
session:Session
username:str
types:int
*0:username
*1:icon
*2:about me
*3:working on

return:bool
True:success
False:Failure
"""

sp.studio_report(session:Session,studioid:str,types:int)
"""
session:Session
username:str
types:int
*0:title
*1:description
*2:thumbnail

return:bool
True:success
False:Failure
"""
```

# create student account
There is no need to do a recaptcha to create a class account. クラスアカウントの作成にはリキャプチャをする必要はありません。
```python
import scratchattachplus as sp

sp.create_student_account(invite_id,username,password)
"""
invite_id:https://scratch.mit.edu/signup/[HERE]
ex. 35etndqk6
username:str
password:str

return:
str:success (sessionID)
None:Failure
"""
```