#import
import datetime
from scratchattach import *
import requests



#ver
__version__ = '0.0.1'

def user_report(session:Session,username:str,types:int):
    """
    types:
    0:username
    1:icon
    2:about me
    3:working on
    """
    t = ["username","icon","about_me","working_on"]
    if types > 4:
        return False
    res = requests.post(
        f"https://scratch.mit.edu/site-api/users/all/{username}/report/?selected_field={t[types]}",
        headers = session._headers,
        cookies = session._cookies,
    )
    if res.status_code == 200:
        return True
    return False

def studio_report(session:Session,studioid:str,types:int):
    """
    types:
    0:title
    1:description
    2:thumbnail
    """
    t = ["title","description","thumbnail"]
    res = requests.post(
        f"https://scratch.mit.edu/site-api/galleries/all/{studioid}/report/?selected_field={t[types]}",
        headers = session._headers,
        cookies = session._cookies,
    )
    if res.status_code == 200:
        return True
    return False

def create_student_account(invite_id:str,username:str,password:str) -> Session:
    cla = requests.get(f"https://api.scratch.mit.edu/classtoken/{invite_id}").json()
    token = requests.get("https://scratch.mit.edu/csrf_token/").headers["set-cookie"].split(";")[3][len(" Path=/, scratchcsrftoken="):]
    kekka = requests.post(f"https://scratch.mit.edu/classes/register_new_student/"
                          f"?username={username}&password={password}&birth_month=1&birth_year=2000&gender=male&country=Japan&is_robot=false&"
                          f"classroom_id={cla["id"]}&classroom_token={invite_id}",
                          headers={'Referer': f'https://scratch.mit.edu/signup/{invite_id}',"x-csrftoken":token,"cookie":f"scratchcsrftoken={token}"})
    if kekka.status_code == 200:
        if kekka.json()[0]["success"]:
            return Session(kekka.json()["token"],username=username)
    else:
        raise ResponseError

"""
class forum:
    def __init__(self,ids:int,session=None,pages:int=1):
        self._response = requests.get(f"https://scratch.mit.edu/discuss/{ids}?page={pages}")
        self.topic_list = re.findall('/discuss/topic/[1234567890]*/',self._response.text)
        self.topic_list = [self.topic_list[num][15:-1] for num in range(len(self.topic_list-1))]
        self.session = session
        return
    def get_topic(self,ids:int,pages:int=1):
        return topic(ids,self.session,pages)

class topic:
    def __init__(self,ids:int,session=None,pages:int=1):
        self._response = requests.get(f"https://scratch.mit.edu/discuss/topic/{ids}?page={pages}")
        self.__find1 = self._response.text.find("/discuss/feeds/topic/")
        self.__find2 = self._response.text[:self.__find1-18].rfind("&raquo;")
        self.title = self._response.text[self.__find2+8:self.__find1-18]
        self.session = session
        return
"""

class comment:
    def __init__(self,object:Project|Studio|User,comment_id:int):
        if type(object) == Project:
            self.type = "p"
        elif type(object) == Studio:
            self.type = "s"
        elif type(object) == User:
            self.type = "u"
        else:
            raise TypeError
        self.location = object
        self.id = comment_id
        if self.update() == "429":
            raise ResponseError
        return

    def update(self) -> bool:
        self._json = self.location.get_comment(self.id)
        if self._json is None:
            return "429"
        try:
            self.id = self._json["id"]
            self.parent_id = self._json["parent_id"]
            self._reply_to = self.id if self.parent_id is None else self.parent_id
            self.commentee_id = self._json["commentee_id"]
            self.content = self._json["content"]
            self.datetime = datetime.datetime.fromisoformat(self._json["datetime_created"])
            self.author = User(username=self._json["author"]["username"])
            self.author._update_from_dict(
                dict(history={"joined":None},profile={
                    "bio":None,"status":None,"country":None,"images":{"90x90":self._json["author"]["image"][:-9] + "90x90.png"}
                    },**self._json["author"]))
            self.reply_count = self._json["reply_count"]
        except:
            return "429"
        return
    
    def update_author(self):
        if self.author.update() == "429":
            raise ResponseError
        return
    
    def report(self):
        """
        ST IS CRAZY!
        Why does the user page have a different link?

        argument:
        object: scratchattach.Project / scratchattach.Studio / scratchattach.User
        need sessionID

        retuen:
        None:reported
        False:failed
        """
        headers = self.location._headers.copy()
        headers["cookie"] = self.location._cookies
        headers["x-csrftoken"] = get_csrf_token()
        if self.location._session is None:
            raise NoSessionError
        if self.type == "p":
            urls = f"https://api.scratch.mit.edu/proxy/project/{self.location.id}/comment/{self.id}/report"
        elif self.type == "s":
            urls = f"https://api.scratch.mit.edu/proxy/studio/{self.location.id}/comment/{self.id}/report"
        elif self.type == "u":
            urls = f"https://scratch.mit.edu/site-api/comments/user/{self.location.username}/rep?id={self.id}"
        else:
            return False
        posts = requests.post(
            urls,
            headers=headers,
            cookies=self.location._cookies
        )
        if posts.status_code == 200:
            return
        else:
            raise ResponseError
        
    def reply(self, content, commentee:User|str|int|None=None):
        """
        commentee:mention user
        str:username
        int:userID
        scratchattach.User
        """
        if type(commentee) == User:
            commentee = commentee.id
        elif type(commentee) == str:
            try:
                commentee = get_user(commentee).id
            except:
                raise NoData
        elif type(commentee) == int:
            pass
        elif commentee is None:
            commentee = ""
        else:
            raise TypeError
        if self.location._session is None:
            raise NoSessionError
        self.location.reply_comment(content,parent_id=self._reply_to,commentee_id=commentee)
        return
    
    def delete(self):
        if self.location._session is None:
            raise NoSessionError
        if self.type == "s":
            raise TypeError
        self.location.delete_comment(comment_id=self.id)


class ResponseError(Exception):
    pass

class NoSessionError(Exception):
    pass

class NoData(Exception):
    pass