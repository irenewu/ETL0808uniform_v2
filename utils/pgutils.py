#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import re
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import logging


abs_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
abs_parent_path = os.path.dirname(abs_path)
sys.path.append(abs_path)
sys.path.append(abs_parent_path)



logger = logging.getLogger("data_transfer_from_mysql_to_pg")

#pg_srcuri = "mysql+pymysql://root:toor@172.16.193.83:3306/opsdata?charset=utf8"
#pg_touri = "postgresql+psycopg2://zhulustagingpgdb:ZhuluXb94A7466@192.168.1.81:5432/optimus_staging0324"
pg_srcuri = "postgresql+psycopg2://zhulustagingpgdb:ZhuluXb94A7466@192.168.1.81:5432/optimus_staging0324"
pg_touri = "postgresql+psycopg2://zhulustagingpgdb:ZhuluXb94A7466@192.168.1.81:5432/optimus_staging0324"

filter_keywords = ["&nbsp;", "&amp;", "\t", "\n", "\r", "&quot;", "&middot;"]


local_engine = create_engine(pg_srcuri, encoding='utf8')
server_engine = create_engine(pg_touri, client_encoding='utf8')


def GetPgConnection(pg_uri, engine):
    #engine = create_engine(pg_uri, client_encoding='utf8')
    DBSession = sessionmaker(bind=engine)
    return DBSession()


local_session = GetPgConnection(pg_srcuri, local_engine)
server_session = GetPgConnection(pg_touri, server_engine)

# 获取表中update_at最晚时间
def get_tablemaxdata(tableclass):
    return str(server_session.query(func.max(tableclass.updated_at)).first()[0])


# 字符串过滤
def replace_multi(src, key):
    if not isinstance(src, (str, unicode)):
        return src
    src = re.sub(r'[%s]' % filter_keywords, '', src)
    if u"descr" in key:
        return re.sub(r'<[\S\s]*?>', '', src)
    return src


# 字段归一
def field_unique(raw_data, tags):
    tokens = raw_data.split("|")
    for token in tokens:
        if token !="" and token!= "None":
            src = re.sub('\s+', '', token)
            tags.add(src)
    return tags


#remove space
def remove_space(my_word):
    if my_word is None:
        return ""
    res = re.sub('\s+', '', my_word)
    #半角转全角
    rstring = ""
    for uchar in res:
        inside_code = ord(uchar)
        if inside_code >= 65281 and inside_code <= 65374:  # 全角字符（除空格）根据关系转化成半角
            inside_code -= 65248
        rstring += unichr(inside_code)
    return rstring


def process_eachrow(old_row):
    new_row = dict()
    new_row["name"] = remove_space(old_row["product"])
    new_row["company_name"] = remove_space(old_row["company"])
    if old_row["company"] == "" and u"公司" in old_row["product"]:
        new_row["name"] = ""
        new_row["company_name"] = remove_space(old_row["product"])
    if old_row["icon"] != "":
        new_row["logo_url"] = old_row["icon"]
    else:
        new_row["logo_url"] = old_row["icon1"]
    new_row["intro"] = remove_space(old_row["yewu"])
    new_row["round"] = remove_space(old_row["lunci"])
    new_row["description"] = str(old_row.get("miaoshu")).strip()
    new_row["website"] = old_row["gw_link"]
    new_row["setup_time"] = old_row["opentime"]
    new_row["location"] = remove_space(old_row["province"])
    new_row["contact_name"] = ""
    new_row["contact_mobile"] = ""
    new_row["contact_email"] = ""
    new_row["contact_wechat"] = ""
    new_row["address"] = ""
    new_row["similar_ids"] = "{}"
    tags = set()
    tags = field_unique(str(old_row["tags"]), tags)
    tags = field_unique(str(old_row["tag_similar"]), tags)
    tags = field_unique(str(old_row["tags_match"]), tags)
    tags = field_unique(str(old_row["tags_unmatch"]), tags)
    tmp = ""
    for tag in tags:
        tmp = tmp + str(tag) + "|"
    new_row["tags"] = tmp
    sectors = set()
    sectors = field_unique(str(old_row["main_hangye"]), sectors)
    sectors = field_unique(str(old_row["sub_hangye"]), sectors)
    sectors = field_unique(str(old_row["hangye1"]), sectors)
    sectors = field_unique(str(old_row["hangye2"]), sectors)
    tmp2 = ""
    for sector in sectors:
        tmp2 = tmp2 + str(sector) + "|"
    new_row["sectors"] = tmp2
    #new fields
    new_row["country"] = old_row["country"]
    new_row["source_link"] = ""
    new_row["docs"] = ""
    new_row["valuation"] = old_row["valuations_money"]
    new_row["valuation_time"] = old_row["valuations_time"]
    return new_row


def process_eachrow_another(old_row):
    new_row = dict()
    new_row["name"] = remove_space(old_row["product"])
    new_row["company_name"] = remove_space(old_row["company"])
    if old_row["company"] == "" and u"公司" in old_row["product"]:
        new_row["name"] = ""
        new_row["company_name"] = remove_space(old_row["product"])
    new_row["logo_url"] = old_row["icon"]
    new_row["intro"] = remove_space(old_row["yewu"])
    new_row["round"] = remove_space(old_row["com_lunci"])
    new_row["description"] = str(old_row.get("description")).strip()
    new_row["website"] = old_row["gw_link"]
    new_row["setup_time"] = old_row.get("opentime","")
    new_row["location"] = remove_space(old_row["province"])
    new_row["contact_name"] = remove_space(old_row["founder_name"])
    new_row["contact_mobile"] = old_row["founder_phone"]
    new_row["contact_email"] = old_row["founder_email"]
    new_row["contact_wechat"] = old_row["founder_wechat"]
    new_row["address"] = remove_space(old_row["address"])
    new_row["similar_ids"] = "{}"
    tags = set()
    tags = field_unique(str(old_row["tags"]), tags)
    tmp = ""
    for tag in tags:
        tmp = tmp + str(tag) + "|"
    new_row["tags"] = tmp
    sectors = set()
    sectors = field_unique(str(old_row["hangye1"]), sectors)
    sectors = field_unique(str(old_row["hangye2"]), sectors)
    sectors = field_unique(str(old_row["hangye3"]), sectors)
    tmp2 = ""
    for sector in sectors:
        tmp2 = tmp2 + str(sector) + "|"
    new_row["sectors"] = tmp2
    #new fields
    new_row["country"] = old_row["country"]
    new_row["source_link"] = old_row["detail_link"]
    new_row["docs"] = old_row["bp_link"]
    new_row["valuation"] = ""
    new_row["valuation_time"] = ""
    return new_row



# 获取ormobj
def get_tableclass(table_name, ormobj):
    tableclass = [v for k, v in ormobj.iteritems() if k in table_name]
    return None if not tableclass else tableclass[0]


# 分页获取数据 slice version
def get_offsetdata(table_name, local_ormobj, query, page_size, page_no, current_offset):
    #all_datas = query.offset(current_offset).limit(page_size).all()
    table_class = get_tableclass(table_name, local_ormobj)
    all_datas = query.order_by(table_class.id).slice(current_offset, current_offset + page_size).all()
    datas = []
    if "product_company" in table_name:
        for old_row in iter(all_datas):
            old_row = dict(old_row.__dict__)
            new_row = process_eachrow(old_row)
            datas.append(new_row)
        #if len(datas) != page_size:
            #logger.info("query data incorrect %d, real length %d, data length %d, limit size %d", page_no, len(all_datas), len(datas), page_size)
    elif "crawler_project" in table_name:
        for old_row in iter(all_datas):
            old_row = dict(old_row.__dict__)
            new_row = process_eachrow_another(old_row)
            datas.append(new_row)
    else:
        logger.info("Wrong table name!")
        sys.exit(1)
    current_offset += len(datas)
    #logger.info("GET pageno %d, query length %d, real length %d, current offset: %d", page_no, len(all_datas), len(datas), current_offset)
    #logger.info("CHECK new page start id:%d", all_datas[0].id)
    return datas, current_offset


# 获取当前表所有字段
def get_tablecolumns(table_name, server_ormobj):
    tableclass = get_tableclass(table_name, server_ormobj)
    if not tableclass:
        return
    return tableclass.__table__.columns.keys()


# 获取 公司表公司id
def get_companyid(table_name, key_word, server_ormobj):
    tableclass = get_tableclass(table_name, server_ormobj)
    if not tableclass:
        return
    datas = server_session.query(tableclass).filter(tableclass.company_name == key_word).all()
    table_id = ""
    for data in datas:
        if not data:
            continue
        table_id = data.id
    return table_id


# 查询表数据总量
def get_datacount(table_name, local_ormobj):
    return map(lambda tacs: local_session.query(tacs).count(), [get_tableclass(table_name, local_ormobj)])


