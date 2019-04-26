#coding=utf8

from werobot import WeRoBot
robot = WeRoBot(token='weixin')
@robot.handler
def hello(message):
    return 'Hello world'