#!flask/bin/python
import os
import unittest
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
from app import app, db
from app.sections.models import Sections
from app.authentication.models import User
from app.authentication.constants import ReadRole, CommentRole, WriteRole

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class CreateAndViewSectionsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        self.app = app.test_client()
        db.create_all()
        ctx = app.app_context()
        ctx.push()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    #if you need a test_user use this in your function, for this case we need diferents types of user
    #so i'm adding the parameter role
    def initialize_test_user(self,role_parameter):
        user_test = User.query.filter(User.username == 'Testuser').first()
        if user_test==None:
            print 'im inserting'
            user = User(username='testuser',
                   email='is2testcms@gmail.com',
                   password='test',
                   role=role_parameter,
                   status=1
            )   
            db.session.add(user)
            db.session.commit()
        else:
            print 'nothing to do'
        return user_test
    #testing view sections
    def test_view_sections(self):
        user_test = self.initialize_test_user(1)
        tester = app.test_client(self)
        response = tester.get('/sec/views_sections/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        with app.test_request_context():
            self.assertTrue(User.verify_token(session['token'])!=None)
            self.assertGreaterEqual(session.get('role'),1)
    
    #testing create sections
    def test_get_create_sections(self):
        user_test = self.initialize_test_user(1<<2)
        tester = app.test_client(self)
        #first verify the user role
        with app.test_request_context():
            self.assertTrue(User.verify_token(session['token'])!=None)
            self.assertGreaterEqual(session.get('role'),1<<2)
        #now check if the redirect of form its ok
        response = tester.get('/sec/create_sections/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    #now testing the post method to create sections    
    #assuming that the users role its ok (by the previous test)
    def test_get_create_sections(self):
        user_test = self.initialize_test_user(1<<2)
        self.initialize_test_user()
        tester = app.test_client(self)
        data = {'section': 'example of test section', 'description': 'example of description'}
        response = tester.post(
            '/sec/create_sections/',
            data= data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 302)
    
if __name__ == '__main__':
    unittest.main()