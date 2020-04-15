import dbunit.dbunit as impl


# 单元测试
class DbUnit(impl.DbUnitImpl):

    def __init__(self, db_engine=None, db_config=None, logger=None, bak_dir=None):
        impl.DbUnitImpl.__init__(self, db_engine=db_engine, db_config=db_config, logger=logger, bak_dir=bak_dir)
