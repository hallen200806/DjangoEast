#coding=utf8

from werobot import WeRoBot
robot = WeRoBot(token='weixin')
@robot.handler
def hello(message):
    msg = message
    if message == 'python':
        return '想学python啊'