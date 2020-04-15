#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_dbunit.py
@Time    :   2020/02/28 18:38:39
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   Dbunit 单元测试

针对Dbunit模块的功能测试

本测试无需已有数据库表支持，会自动create/drop需要的表

测试内容：
1. 测试参数初始化，如临时文件夹路径是否生成，logger是否生成等
2. backup功能测试
3. load_data功能测试
4. reload功能测试

'''
import unittest
from dbunit import DbUnit
import dbunit.utils as utils
import os
import tempfile


class Test_DbUnit(unittest.TestCase):
    """测试DbUnit组件
    """

    def setUp(self):
        self.db_cfg = {
            'server_url': 'rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com',
            'server_port': 3306,
            'db_name': 'fdata_dev',
            'user_id': 'dev',
            'user_password': 'dev_61875707',
        }
        try:
            # 建立测试用临时表
            session = utils.get_session(utils.get_conn_engine(self.db_cfg))
            sql = "create table dbu_test_a (`name` VARCHAR(20) NOT NULL, PRIMARY KEY (`name`))"
            session.execute(sql)
            sql = "create table dbu_test_b (`id` VARCHAR(20) NOT NULL, PRIMARY KEY (`id`))"
            session.execute(sql)
        finally:
            session.close()
        return super().setUp()

    def tearDown(self):
        try:
            # Drop测试用临时表
            session = utils.get_session(utils.get_conn_engine(self.db_cfg))
            sql = "drop table dbu_test_a"
            session.execute(sql)
            sql = "drop table dbu_test_b"
            session.execute(sql)
        finally:
            session.close()
        return super().tearDown()

    def test_dbunit_init(self):
        """
        测试Dbunit对象的初始化
        """
        dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=self.db_cfg))
        self.assertDictEqual({}, dbu.back_files)
        self.assertDictEqual({}, dbu.test_data)
        # 默认的临时文件夹，应该是操作系统临时目录下的\dbtest_temp\
        bak_dir = tempfile.gettempdir() + r'\dbtest_temp'
        self.assertEqual(bak_dir, dbu._backup_dir)

        # 测试初始化参数为空，无法连接数据库的情况
        try:
            dbu = DbUnit()
            self.fail()
        except IOError:
            pass
        else:
            self.fail()

    def test_backup(self):
        """测试 backup 函数功能
        """
        dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=self.db_cfg))
        dbu.add_table('dbu_test_a', r'test\dbu_test_a.csv')
        dbu.add_table('dbu_test_b')     # 无测试数据情况
        dbu.backup()

        # 检查登记表情况
        bak_files = {
            'dbu_test_a': dbu._backup_dir + r'\dbu_test_a.csv',
            'dbu_test_b': dbu._backup_dir + r'\dbu_test_b.csv',
        }
        self.assertDictEqual(bak_files, dbu.back_files)

        # 检查备份文件是否生成
        self.assertTrue(os.path.exists(dbu._backup_dir + r'\dbu_test_a.csv'))
        self.assertTrue(os.path.exists(dbu._backup_dir + r'\dbu_test_b.csv'))

        # 测试表不存在的情况
        try:
            dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=self.db_cfg))
            dbu.add_table('xxxx')
            dbu.backup()
            self.fail()
        except Exception as err:
            self.assertIsNotNone(err)

    def test_load_data(self):
        """测试 load_data 函数功能
        """
        dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=self.db_cfg))
        dbu.add_table('dbu_test_a', r'test_dbunit\dbu_test_a.csv')
        dbu.add_table('dbu_test_b')     # 无测试数据情况
        dbu.backup()
        dbu.load_data()

        # 检查 测试数据表情况
        test_data = {
            'dbu_test_a': r'test_dbunit\dbu_test_a.csv',
            'dbu_test_b': None,
        }
        self.assertDictEqual(test_data, dbu.test_data)

        # 检查数据库表内容是否同测试数据一致
        try:
            session = utils.get_session(utils.get_conn_engine(self.db_cfg))
            # 检查表A：
            sql = "select * from dbu_test_a"
            cursor = session.execute(sql)
            records = cursor.fetchall()
            data = [('张三',), ('李四',)]
            self.assertListEqual(data, records)
            cursor.close()
            # 检查表B：
            sql = "select * from dbu_test_b"
            cursor = session.execute(sql)
            records = cursor.fetchall()
            self.assertListEqual([], records)
            cursor.close()
        finally:
            session.close()

    def test_reload(self):
        """测试 reload 函数功能
        """
        dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=self.db_cfg))
        dbu.add_table('dbu_test_a', r'test\dbu_test_a.csv')
        dbu.add_table('dbu_test_b')     # 无测试数据情况
        dbu.backup()
        dbu.load_data()
        dbu.reload()

        # 检查数据库表内容是否恢复最初情况？
        try:
            session = utils.get_session(utils.get_conn_engine(self.db_cfg))
            # 检查表A：
            sql = "select * from dbu_test_a"
            cursor = session.execute(sql)
            records = cursor.fetchall()
            self.assertListEqual([], records)
            cursor.close()
            # 检查表B：
            sql = "select * from dbu_test_b"
            cursor = session.execute(sql)
            records = cursor.fetchall()
            self.assertListEqual([], records)
            cursor.close()
        finally:
            session.close()
