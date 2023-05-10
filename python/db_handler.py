import os
import sys

# 서드파티 라이브러리 사용을 위한 경로 지정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# DB Table 조회 후 class 생성
os.system("sqlacodegen {} > db_tables.py".format(os.environ['DB_INFO']))
from tables import *


def connect_db(data):

    #
    engine = create_engine(os.environ['DB_INFO'], echo=True).connect()

    results = []
    for k, v in data.items():
        t_name, c_name = k.split('.')
        results.append(globals()[t_name.capitalize()](api_name=n, service_num=i) for i, n in enumerate(v))

    print(results)
    with Session(engine) as session:
        session.bulk_save_objects(results[1:])
        #    api = session.query(globals()[t_name.capitalize()]).all()
        #    print(api)
        #    print(Api.__dict__.keys())

        # deleteList = tables.Api(
        #     api_name = "deleteList",
        #     service_num = 1
        # )

        #    for i in range(3):
        #        session.saveorupdate(globals()['test{}'.format(i)], unique_key = "api_name")
        session.commit()

    #
    engine.close()
