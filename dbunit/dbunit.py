

import os
import pandas as pd
import tempfile
import dbunit.utils as utils


class DbUnitImpl:
    """
    关系型数据库 单元测试工具
    """

    def __init__(self, db_engine=None, db_config=None, logger=None, bak_dir=None):
        self.back_files = {}    # 备份文件注册表，表名:备份文件
        self.test_data = {}     # 测试文件注册表，表名:测试文件
        if not logger:
            self._logger = utils.get_logger()
        else:
            self._logger = logger       # 日志

        # 数据库连接
        if not db_engine:
            self._db_engine = utils.get_conn_engine(db_config)
        else:
            self._db_engine = db_engine
        if self._db_engine is None:
            self._logger.error('无数据库连接，无法进行单元测试！')
            raise IOError('无数据库连接，无法进行单元测试！')

        if bak_dir is None:
            # 默认备份文件存放在系统临时文件夹下
            self._backup_dir = tempfile.gettempdir() + r'\dbtest_temp'
        else:
            self._backup_dir = bak_dir
        if not os.path.exists(self._backup_dir):
            os.mkdir(self._backup_dir)

    @staticmethod
    def export_data_file(db_engine, table_name, file_path):
        # 工具函数，数据库表导出备份文件
        df = pd.read_sql_table(table_name=table_name.lower(), con=db_engine)
        if df is not None:
            df.to_csv(file_path, index=False, encoding='utf-8')
            print('export {0} ==> {1} ok'.format(table_name, file_path))

    def _log(self, msg):
        # 记录日志
        if self._logger:
            self._logger.debug("【dbunit】" + msg)
        # else:
        #     print("【dbunit】" + msg)

    def add_table(self, tablename, testdata_file=None):
        # 添加 需要测试的表名测试用文件
        # testdata_file = None，说明改表仅需要清空，不要导入测试文件
        self.back_files[tablename] = None
        self.test_data[tablename] = testdata_file

    def backup(self):
        """备份数据表内容到临时文件
        """
        self._log('开始备份 ... ')
        # 建立临时文件夹
        if not os.path.exists(self._backup_dir):
            os.mkdir(self._backup_dir)

        try:
            # engine = utils.get_conn_engine()
            engine = self._db_engine
            session = utils.get_session(engine)

            # 所有表导出临时备份文件
            count_all = len(self.back_files)
            idx = 1
            for table_name in self.back_files:
                df = pd.read_sql_table(table_name=table_name.lower(), con=engine)
                # print(df)

                # if df is not None and not df.empty:
                if df is not None:
                    # 生成备份文件
                    bak_file = self._backup_dir + "\\" + table_name + '.csv'
                    df.to_csv(bak_file, index=False, encoding='utf-8', chunksize=10000)
                    self._log('[{0}/{1}] 表 {2} 备份到 {3} '.format(idx, count_all, table_name, bak_file))
                    self.back_files[table_name] = bak_file    # 登记
                else:
                    # 原始表无数据
                    self._log('[{0}/{1}] 表 {2} 中无数据 ... '.format(idx, count_all, table_name))
                idx += 1
            # self._log('back_files {0}'.format(self.back_files))
            # self._log('test_data {0}'.format(self.test_data))
            self._log('全部{0}个表备份完成！'.format(count_all))
        except Exception as err:
            self._log('备份原始数据时出现问题，' + str(err))
            raise Exception('备份原始数据时出现问题，' + str(err))
        finally:
            session.close()

    def load_data(self):
        """导入测试数据
        """
        self._log('导入测试数据 ... ')

        try:
            # engine = utils.get_conn_engine()
            engine = self._db_engine
            session = utils.get_session(engine)

            count_all = len(self.test_data)
            idx = 1
            for table_name in self.test_data:
                data_file = self.test_data[table_name]

                # 删除原始数据
                sql = "truncate table " + table_name
                session.execute(sql)

                if data_file is None:
                    # 无测试文件
                    self._log('[{0}/{1}] 表 {2} 无 测试文件 '.format(idx, count_all, table_name))
                elif os.path.exists(data_file):
                    # 导入测试数据
                    df = pd.read_csv(data_file)
                    # 导入数据库表
                    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                    self._log('[{0}/{1}] 表 {2} 导入测试数据  [{3}] '.format(idx, count_all, table_name, df.shape[0]))
                else:
                    # 测试文件不存在
                    self._log('[{0}/{1}] 表 {2} 测试文件不存在 [{3}] '.format(idx, count_all, table_name, data_file))
                idx += 1

            self._log('导入测试数据完成！')
        except Exception as err:
            self._log('导入测试数据时出现问题，' + str(err))
        finally:
            session.close()

    def reload(self):
        """恢复原始数据
        """
        self._log('恢复数据 ... ')

        try:
            # engine = utils.get_conn_engine()
            engine = self._db_engine
            session = utils.get_session(engine)

            count_all = len(self.back_files)
            idx = 1
            for table_name in self.back_files:
                data_file = self.back_files[table_name]

                # 删除原始数据
                sql = "truncate table " + table_name
                session.execute(sql)

                if not data_file:
                    self._log('[{0}/{1}] 表 {2} 没有备份，无法恢复'.format(idx, count_all, table_name))
                elif os.path.exists(data_file):
                    # 导入测试数据
                    df = pd.read_csv(data_file)
                    # 导入数据库表
                    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                    self._log('[{0}/{1}] 表 {2} 恢复 [{3}] '.format(idx, count_all, table_name, df.shape[0]))
                else:
                    # 测试文件不存在
                    self._log('[{0}/{1}] 表 {2} 备份文件不存在，无法恢复 [{3}] '.format(idx, count_all, table_name, data_file))
                idx += 1

            # TODO 删除建立的临时文件夹
            self._log('恢复数据完成！')
        except Exception as err:
            self._log('恢复数据时出现问题，' + str(err))
        finally:
            session.close()
