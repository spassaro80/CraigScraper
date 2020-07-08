from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread,Message

# Create your tests here.

class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1=User.objects.create_user('User1', None, 'test1234')
        self.user2=User.objects.create_user('User2', None, 'test1234')
        self.user3=User.objects.create_user('User3', None, 'test1234')


        self.thread = Thread.objects.create()
    
    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()),2)

    def test_filter_thread_by_user(self):
        self.thread.users.add(self.user1, self.user2)
        thread=Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread,thread[0])
    
    def test_filter_no_existent_thread(self):
        thread=Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(thread),0)
    
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1=Message.objects.create(user=self.user1, content="Hola")
        message2=Message.objects.create(user=self.user2, content="Que pasa")
        self.thread.messages.add(message1,message2)
        self.assertEqual(len(self.thread.messages.all()),2)

        for message in self.thread.messages.all():
            print("({}) says: {} ".format(message.user, message.content))

    def test_check_unknown_user_adding_message(self):
        self.thread.users.add(self.user1, self.user2)
        message1=Message.objects.create(user=self.user1, content="Hola")
        message2=Message.objects.create(user=self.user2, content="Que pasa")
        message3=Message.objects.create(user=self.user3, content="Soy un espía!!!")
        self.thread.messages.add(message1,message2,message3)
        self.assertEqual(len(self.thread.messages.all()),2)

    def test_check_find_thread_using_custom_method(self):
        self.thread.users.add(self.user1, self.user2)
        thread=Thread.objects.find(self.user1, self.user2)
        self.assertEqual(thread, self.thread)

    def test_check_find_or_create_thread_using_custom_method(self):
        self.thread.users.add(self.user1, self.user2)
        thread=Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(thread, self.thread)
        thread=Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)
        