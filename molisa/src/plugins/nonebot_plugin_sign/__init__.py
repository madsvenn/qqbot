from datetime import datetime

import nonebot
from nonebot.adapters import Event
from nonebot import on_command, logger, on_keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from .config import OperationMysql


sign = on_command('签到')


@sign.handle()
async def sign_user(bot: Bot, event: Event):
    user_qq = event.get_user_id()
    sql = 'select * from sign where user_qq = '
    # logger.info(sql+user_qq)
    sql_select = sql+user_qq

    op_mysql = OperationMysql()
    user = op_mysql.search_one(sql_select)

    time = datetime.now().strftime("%Y-%m-%d")
    # logger.info(time)
    # logger.info(user['last_insertDate'].strftime("%Y-%m-%d"))
    if not(user == None):
       if user['last_insertDate'].strftime("%Y-%m-%d") == time:
           # sql_update = 'update sign set count = count + ' + '1' + ', last_insertDate = now(), integral = integral + 1' + ' where user_qq =' + user_qq
           # logger.info(sql_update)
           #
           # op_mysql = OperationMysql()
           # op_mysql.updata_one(sql_update)
           #
           # logger.info("成功")
           # logger.info("已经签过了")
           uid = 'uid: ' + str(user['uid']) + '\n'
           at_ = "[CQ:at,qq={}]".format(user_qq)
           message = at_ +'\n'+ uid + '今天已经签过到了哦~'+'\n'+'发送‘金币获取’查看获取金币的方法'
           await bot.send(event, Message(message))

       else:
           sql_update = 'update sign set count = count + ' + '1, ' + 'last_insertDate = now(), integral = integral + 1' + ' where user_qq =' + user_qq
           logger.info(sql_update)

           op_mysql = OperationMysql()
           op_mysql.updata_one(sql_update)

           logger.info("成功")
           message = await success(user_qq)
           await bot.send(event, Message(message))
    else:
        sql_insert = 'insert into sign values ' + '( ' + user_qq + ',' + '1, now(),1,null)'
        logger.info(sql_insert)

        op_mysql = OperationMysql()
        op_mysql.insert_one(sql_insert)

        logger.info("签到成功")

        message = await success(user_qq)
        await bot.send(event, Message(message))



async def success(user_qq: str):
    sql = 'select * from sign where user_qq = '
    sql_select = sql+user_qq

    op_mysql = OperationMysql()
    user = op_mysql.search_one(sql_select)
    at_ = "[CQ:at,qq={}]".format(user_qq)
    uid = 'uid: ' + str(user['uid']) + '\n'
    logger.info(user['last_insertDate'])
    message = at_ + '签到成功'+'\n'+ uid + '已连续签到 ' + str(user['count']) +' 天'+'\n'+'金币有 '+ str(user['integral']) +'\n'+'最后一次签到时间：'+str(user['last_insertDate'].strftime("%Y-%m-%d %H:%M:%S"))
    message = message + '\n' + '发送‘个人信息’即可查看'

    return message


info = on_command('个人信息',aliases={'我的个人信息'})
@info.handle()
async def info_select(bot: Bot, event: Event):
    user_qq = event.get_user_id()
    sql = 'select * from sign where user_qq = '
    # logger.info(sql+user_qq)
    sql_select = sql+user_qq

    op_mysql = OperationMysql()
    user = op_mysql.search_one(sql_select)
    at_ = "[CQ:at,qq={}]".format(user_qq)
    uid = 'uid: '+ str(user['uid']) + '\n'
    message = at_ +'\n' + uid + '已连续签到 ' + str(user['count']) + ' 天' + '\n' + '金币有 ' + str(
        user['integral']) + '\n' + '最后一次签到时间：' + str(user['last_insertDate'].strftime("%Y-%m-%d %H:%M:%S"))
    if not user==None:
        await bot.send(event, Message(message))
    else:
        await bot.send(event, Message("暂未有相关信息~"))

corn = on_command('金币获取')
@corn.handle()
async def corn_method(bot: Bot, event: Event):
    await bot.send(event, Message('签到获取，玩游戏（随机唐可可）获取，联系我主人更改数据库'))