# import unittest
from wdbd.dbunit import DbUnit
# import wdbd.dbunit.utils as utils


if __name__ == "__main__":
    # # dbu = DbUnit()
    # cfg = {
    #     'server_url': 'rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com',
    #     'server_port': 3306,
    #     'db_name': 'fdata_dev',
    #     'user_id': 'dev',
    #     'user_password': 'dev_61875707',
    # }
    # dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=cfg), bak_dir=r'c:/temp/dbunit_bak/')
    # print(dbu)
    # print(dbu._db_engine)
    # print(dbu._backup_dir)

    # func:
    # dbu.export_data_file(db_engine=utils.get_conn_engine(cfg), table_name='dw_worker_status', file_path=r'c:/temp/dw_worker_status.csv')

    # # dbu.add_table('dw_worker_status', testdata_file=r'c:/temp/dw_worker_status.csv')
    # dbu.add_table('dw_worker_status')
    # dbu.backup()
    # dbu.load_data()

    # dbu.reload()

    try:
        dbu = DbUnit()
    except Exception:
        print('io err')

    pass
