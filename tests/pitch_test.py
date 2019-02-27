from app.models import Comment,User,Pitch
from app import db
import unittest

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_wihogora= User(username = 'wihogora',password = '123', email = 'wwihogora@gmail.com')
        self.new_pitch = Pitch(id=1,pitch_title='Test',pitch_content='This is a test pitch',category="product",user = self.user_wihogora,likes=0,dislikes=0)
