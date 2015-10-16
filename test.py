from app import app
from app import db
from app.authentication.models import User
import unittest
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

class FlaskTestCase(unittest.TestCase):
   
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False  
        app.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.client = app.test_client()
        ctx = app.app_context()
        ctx.push()
        db.create_all()
        return app
    
    #if you need a test_user use this in your function
    def initialize_test_user(self):
        usertest = User.query.filter(User.username == 'Testuser').first()
        if usertest==None:
            print 'im inserting'
            user = User(username='testuser',
                   email='is2testcms@gmail.com',
                   password='test',
                   role=1,
                   status=1
            )   
            db.session.add(user)
            db.session.commit()
        else:
            print 'nothing to do'
    
    #in this pull request this team haven't a index page       
    def test_index(self):
        #self.initialize_test_user()
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)
    
    #Testing initialization of form recover password
    def test_init_recover_pass(self):
        tester = app.test_client(self)
        response = tester.get('/auth/recover_pass', content_type='html/text,',follow_redirects=True)
        self.assertIn(b'Recuperar Cuenta', response.data)
        
    #Testing the correct function of recover password
    def test_recover_pass(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        data = {'email': 'is2testcms@gmail.com'}
        response = tester.post(
            '/auth/recover_pass/',
            data= data,
            follow_redirects=True
        )
        self.assertIn(b'Se ha enviado un correo a la direccion',response.data)
    
    def test_change_password_recover(self):
        self.initialize_test_user()
        tester = app.test_client(self)
        usertest = User.query.filter(User.username == 'Testuser').first()
        token = usertest.get_token()
        old_password = usertest.password
        
        #test initialization of form Change Password
        url = '/auth/change_pass/?token='+str(token)
        response = tester.get(
            url,
            content_type='html/text,',follow_redirects=True)
        self.assertIn(b'Change Password',response.data)
        
        #Test functionality of Change Password
        data = {'password': 'new_test','confirm': 'new_test'}
        response_post = tester.post(
             url,
             data=data
        )
        self.assertIn(b'password updated successfully',response_post.data)
        self.assertIsNot(usertest.password,old_password)
        # print response_post.data

if __name__ == '__main__':
    unittest.main()