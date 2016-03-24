import unittest
from fwsdemo.database import init_db
from fwsdemo.database import db_session
from fwsdemo.models import User

def prep_data():
    try:
        u1 = User('person1', 'p1@example.tld')
        u2 = User('person2', 'p2@example.tld')
        db_session.bulk_save_objects([u1,u2])
        db_session.commit()
        users = User.query.all()
        print(users)
    except:
        db_session.rollback()
        print("WARNING: Couldn't create new test data.")

def delete_all_data():
    try:
        num_rows_deleted = db_session.query(Model).delete()
        db_session.commit()
    except:
        db_session.rollback()

def setUpModule():
    print("setUpModule")
    init_db()

def tearDownModule():
    print("tearDownModule")


class Class1Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("  setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("  tearDownClass")

    def setUp(self):
        print("       setUp")
        prep_data()

    def tearDown(self):
        print("       tearDown")
        delete_all_data()

    def test_1(self):
        print("  class 1 test 1")
        record = db_session.query(User).filter(User.name == 'person1').first()
        self.assertEqual(record.email, 'p1@example.tld', 'Matching the correct email to the correct person')


    def test_2(self):
        print("  class 1 test 2")
        record = db_session.query(User).filter(User.name == 'person2').first()
        self.assertEqual(record.email, 'p2@example.tld', 'Matching the correct email to the correct person')
