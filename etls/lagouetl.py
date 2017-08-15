#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import logging
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger("filter_data_to_staging")
filetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=str(filetime)+'.log',
                    filemode='w')
abs_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
abs_parent_path = os.path.dirname(abs_path)
sys.path.append(abs_path)
sys.path.append(abs_parent_path)

from ETL0808uniform_v2.sqlmapping.lagoumapping import LocalProject1, LocalProject2, LocalProductCompany1, LocalProductCompany2, LocalProductCompany3, ServerProductCompany
from ETL0808uniform_v2.utils.pgutils import get_offsetdata, get_tableclass, get_companyid, get_datacount, get_tablecolumns, local_session, replace_multi \
    ,server_session


filter_keywords = ["&nbsp;", "&amp;", "\t", "\n", "\r", "&quot;", "&middot;"]
local_ormobj = {"cp_crawler_project": LocalProject1, "mf_crawler_project2": LocalProject2
                ,"mf_product_company_copy": LocalProductCompany2, "mf_product_company2": LocalProductCompany3
                , "mf_product_company": LocalProductCompany1}
server_ormobj = {"cp_crawler_project": ServerProductCompany, "mf_crawler_project2": ServerProductCompany
                ,"mf_product_company_copy": ServerProductCompany, "mf_product_company2": ServerProductCompany
                , "mf_product_company": ServerProductCompany}

'''
# 获取新orm对象
def get_newobj(table_name, columns, data, server_ormobj):
    tableclass = get_tableclass(table_name, server_ormobj)()
    for k, v in data.iteritems():
        if columns.__contains__(k):
            setattr(tableclass, k, v)
    return tableclass
'''

# 分页写
def add_pageddata(table_name, server_session, server_ormobj, page_data, insert_count):
    session = server_session
    table_class = get_tableclass(table_name, server_ormobj)
    IntegrityError = 0
    try:
        session.execute(table_class.__table__.insert(), page_data)
        session.commit()
        insert_count += len(page_data)
        return insert_count
    except Exception, e:
        session.rollback()
    for piece_data in page_data:
        try:
            session.execute(table_class.__table__.insert(), piece_data)
            session.commit()
            insert_count += 1
        except Exception, e:
            if e.message.__contains__("duplicate key"):
                IntegrityError += 1
            else:
                logger.info(e)
            session.rollback()
    #logger.info("ADD insert count: %d, IntegrityError: %d, data size: %d", insert_count, IntegrityError, len(page_data))
    return insert_count


#分页读写 slice
def get_then_put(table_name, query, page_size, page_no, server_ormobj, local_ormobj, current_offset, insert_count):
    page_data, current_offset = get_offsetdata(table_name, local_ormobj, query, page_size, page_no, current_offset)
    insert_count = add_pageddata(table_name, server_session, server_ormobj, page_data, insert_count)
    return current_offset, insert_count


#分页拖库 slice
def copy_data(table_name):
    logger.info("---------Begin %s--------", table_name)
    insert_count = 0
    current_offset = 0
    counts = get_datacount(table_name, local_ormobj)[0]
    page_size = 1000
    page_no = 0
    tableclass = get_tableclass(table_name, local_ormobj)
    if not tableclass:
        return
    query = local_session.query(tableclass)
    logger.info("data count: %d", counts)
    while current_offset < counts:
        page_no += 1
        current_offset, insert_count = get_then_put(table_name, query, page_size, page_no,  server_ormobj,local_ormobj, current_offset, insert_count)
        logger.info("COPY pageno %d, insert count: %d current offset: %d", page_no, insert_count, current_offset)
    logger.info("%d %d",current_offset, insert_count)


def main():
    logger.info("-----Begin-----")
#    copy_data("cp_crawler_project")
    copy_data("mf_crawler_project2")
#    copy_data("mf_product_company_copy")
#    copy_data("mf_product_company2")
#    copy_data("mf_product_company")
    logger.info("-----Exit-----")


if __name__ == "__main__":
    main()


