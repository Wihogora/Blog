from app.models import Comment,User,Pitch
from app import db
import unittest

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_wihogora = User(username = 'wihogora',password = '123', email = 'wwihogora@gmail.com')
        self.new_pitch = Pitch(id=1,pitch_title='Test',pitch_content='This is a pitch test',category="product",user = self.user_wihogora,likes=0,dislikes=0)
        self.new_comment = Comment(id=1,comment='Test comment',user=self.user_wihogora,pitch=self.new_pitch)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()