#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2020/04/13 20:53:20
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   工具模块
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging.config


def get_logger():
    """
    返回一个日志器
    :rtype:
    :param config_file_path: str 配置文件路径
    :return: logger日志器
    """
    config_file_path = r'dbunit/log.cfg'

    logging.config.fileConfig(config_file_path)
    return logging.getLogger('dbunit')


def get_conn_engine(db_config):
    """返回数据库连接引擎

    demo for db_config:
    {
        'server_url': '127.0.0.1',
        'server_port': 3306,
        'db_name': 'fdata_dev',
        'user_id': 'root',
        'user_password': '123456',
        'echo': false,
        'max_overflow': 0,
        'pool_size': 5,
        'pool_timeout': 10,
        'pool_recycle': -1,
    }

    Arguments:
        db_config {dict} -- mysql数据库连接配置

    Returns:
        [engine] -- 数据库连接引擎
    """
    log = get_logger()
    if not db_config:
        log.error('数据库配置为空，无法建立数据库连接')
        return None

    # mysql+mysqlconnector://dev:dev_61875707@rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com:3306/fdata_dev
    try:
        conn_str = 'mysql+mysqlconnector://{user_id}:{user_password}@{server_url}:{server_port}/{db_name}'.format(
            server_url=db_config.get('server_url'),
            user_id=db_config.get('user_id'),
            user_password=db_config.get('user_password'),
            server_port=db_config.get('server_port'),
            db_name=db_config.get('db_name'))
        # engine = create_engine(conn_str, echo=True)
        engine = create_engine(conn_str, echo=db_config.get('echo', False),
                               max_overflow=db_config.get(
                                   'max_overflow', 0),  # 超过连接池大小外最多创建的连接
                               pool_size=db_config.get(
                                   'pool_size', 5),  # 连接池大小
                               pool_timeout=db_config.get(
                                   'pool_timeout', 10),  # 池中没有线程最多等待的时间，否则报错
                               # 多久之后对线程池中的线程进行一次连接的回收（重置）
                               pool_recycle=db_config.get('pool_recycle', -1)
                               )
        return engine
    except Exception as err:
        log.error("数据库连接失败，" + str(err))
        return None


def get_session(engine):
    """新建并返回数据库会话（session）

    如果参数提供engine则使用之，否则新建

    Keyword Arguments:
        engine {sqlalchemy.engine} -- 如果参数提供engine则使用之，否则新建 (default: {None})

    Returns:
        [sqlalchemy.session] -- 数据库会话
    """
    log = get_logger()
    try:
        SessionFactory = sessionmaker(engine)
        db_session = SessionFactory()
        return db_session
    except Exception as err:
        log.error(str(err))
        return None


if __name__ == "__main__":
    cfg = {
        'server_url': 'rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com',
        'server_port': 3306,
        'db_name': 'fdata_dev',
        'user_id': 'dev',
        'user_password': 'dev_61875707',
    }
    e = get_conn_engine(db_config=cfg)
    session = get_session(engine=e)
    print(e)
    print(session)
