#coding=utf8

from werobot import WeRoBot
robot = WeRoBot(enable_session=False, token='weixin',APP_ID='wxc9efef32dadb772',APP_SECRET='f3e4ecfbe96ca052cffea8eb55a03bc5')

@robot.handler
def hello(message):
    return 'Hello world'