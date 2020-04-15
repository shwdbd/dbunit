# dbunit

DbUnit，一款关系型数据库单元测试工具。

仿造Java版本的DbUnit，其在单元测试setup中备份需要的数据库表，导入准备好的测试数据，在完成单元测试后在TearDown阶段使用之前备份的文件恢复数据库表原始内容。

目前的版本是 v 0.2

v 0.2版本的特点为：

- 包名改为 dbunit。

## 安装方式

使用pip工具进行安装，如下：

```command
pip install dbunit
```

由于项目处于早期阶段，更新较多，请经常使用如下命令进行版本更新：

```command
pip install dbunit --upgrade
```

## 使用示例

```python
import unittest
from dbunit import DbUnit
import dbunit.utils as utils


class TestDemo(unittest.TestCase):

    def setUp(self):
        self.db_cfg = {
            'server_url': 'rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com',
            'server_port': 3306,
            'db_name': 'fdata_dev',
            'user_id': 'dev',
            'user_password': 'dev_61875707',
        }
        self.dbu = DbUnit(db_engine=utils.get_conn_engine(db_config=cfg))
        self.dbu.add_table('table_a', 'test_file_a.csv')
        self.dbu.add_table('table_b')
        self.dbu.backup()
        self.dbu.load_data()

    def tearDown(self):
        self.dbu.reload()

    def test_foo(self):
        # 业务测试
        pass

```
