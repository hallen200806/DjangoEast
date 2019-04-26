#coding=utf8

from werobot import WeRoBot
robot = WeRoBot(token='weixin')
@robot.handler
def hello(message):
    msg = message.content.strip().lower().encode('utf8')
    if msg == 'python':
        return '想学python啊'