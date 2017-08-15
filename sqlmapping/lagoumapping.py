#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys


from sqlalchemy import Column, String, DateTime, Integer, MetaData, Text, \
    SmallInteger, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(schema='data')
Base = declarative_base(metadata=meta)
#Base.metadata.create_all(server_engine) #create schema

meta1 = MetaData(schema='data')
Base1 = declarative_base(metadata=meta1)


class ProjectFrom(object):

    id = Column(Integer, primary_key=True)
    source = Column(String)
    company = Column(String)
    product = Column(String)
    post_time = Column(DateTime)
    alias = Column(String)
    barcode = Column(String)
    icon = Column(String)
    detail_link = Column(String)
    description = Column(Text)
    yewu = Column(Text)
    tags = Column(String)
    gw_link = Column(String)
    hangye1 = Column(String)
    hangye2 = Column(String)
    hangye3 = Column(String)
    com_id = Column(Integer)
    com_lunci = Column(String)
    capital = Column(String)
    com_scale = Column(String)
    com_status = Column(String)
    country = Column(String)
    province = Column(String)
    city = Column(String)
    address = Column(String)
    spider_status = Column(SmallInteger)
    md5 = Column(String)
    founder_name = Column(String)
    founder_email = Column(String)
    founder_phone = Column(String)
    founder_wechat = Column(String)
    bp_link = Column(String)
    api_link = Column(String)
    app_url = Column(Text)
    apk_name = Column(String)
    snapshot = Column(Text)
    complete_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    compare_flag = Column(Integer)
    managers_flag = Column(Integer)
    manager_time = Column(String)
    opentime = Column(String)
    addedzb = Column(SmallInteger)


#src
class LocalProject1(Base1, ProjectFrom):
    __tablename__ = "cp_crawler_project"
    __table_args__ = (UniqueConstraint('source', 'company', 'product'),)


class ProjectFrom2(object):
    id = Column(Integer, primary_key=True)
    source = Column(String)
    company = Column(String)
    product = Column(String)
    post_time = Column(DateTime)
    alias = Column(String)
    barcode = Column(String)
    icon = Column(String)
    detail_link = Column(String)
    description = Column(Text)
    yewu = Column(Text)
    tags = Column(String)
    gw_link = Column(String)
    hangye1 = Column(String)
    hangye2 = Column(String)
    hangye3 = Column(String)
    com_id = Column(Integer)
    com_lunci = Column(String)
    capital = Column(String)
    com_scale = Column(String)
    com_status = Column(String)
    country = Column(String)
    province = Column(String)
    city = Column(String)
    address = Column(String)
    spider_status = Column(SmallInteger)
    md5 = Column(String)
    founder_name = Column(String)
    founder_email = Column(String)
    founder_phone = Column(String)
    founder_wechat = Column(String)
    bp_link = Column(String)
    api_link = Column(String)
    app_url = Column(Text)
    apk_name = Column(String)
    snapshot = Column(Text)
    complete_flag = Column(SmallInteger)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    compare_flag = Column(Integer)
    managers_flag = Column(Integer)
    manager_time = Column(String)


#src
class LocalProject2(Base1, ProjectFrom2):
    __tablename__ = "mf_crawler_project2"
    __table_args__ = (UniqueConstraint('source', 'company', 'product'),)


class ProductCompanyFrom(object):

    id = Column(Integer, primary_key=True)
    product = Column(String)
    company = Column(String)
    gw_link = Column(String)
    tags = Column(String)
    tags_match = Column(String)
    tags_unmatch = Column(String)
    miaoshu = Column(Text)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    renzheng = Column(SmallInteger)
    icon = Column(String)
    icon1 = Column(String)
    hangye1 = Column(String)
    symbol = Column(String)
    hangye2 = Column(String)
    main_hangye = Column(String)
    sub_hangye = Column(String)
    vice_hangye = Column(String)
    albums = Column(String)
    tag_similar = Column(String)
    lunci = Column(String)
    luncivalue = Column(Integer)
    rongzi_count = Column(SmallInteger)
    orderbyrztime = Column(String)
    opentime = Column(String)
    yewu = Column(String)
    country = Column(String)
    province = Column(String)
    city = Column(String)
    need_flag = Column(SmallInteger)
    display_flag = Column(SmallInteger)
    rongzi_flag = Column(SmallInteger)
    is_company = Column(SmallInteger)
    is_product = Column(SmallInteger)
    ziben_jieduan = Column(String)
    ziben_code = Column(String)
    valuations_time = Column(String)
    valuations_money = Column(String)
    unicorn = Column(String)
    company_status = Column(String)
    company_properties = Column(String)
    short_url = Column(String)
    unionid = Column(String)
    uuid = Column(String)
    is_dealjp = Column(SmallInteger)


class LocalProductCompany1(Base1, ProductCompanyFrom):
    __tablename__ = "mf_product_company"
    __table_args__ = (UniqueConstraint('product', 'company', 'gw_link'),)


class LocalProductCompany2(Base1, ProductCompanyFrom):
    __tablename__ = "mf_product_company_copy"
    __table_args__ = (UniqueConstraint('product', 'company', 'gw_link'),)


class LocalProductCompany3(Base1, ProductCompanyFrom):
    __tablename__ = "mf_product_company2"
    __table_args__ = (UniqueConstraint('product', 'company', 'gw_link'),)


class ProductCompanyTo(object):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_name = Column(String)
    logo_url = Column(String)
    intro = Column(String)
    sectors = Column(String)
    tags = Column(String)
    round = Column(String)
    description = Column(String)
    website = Column(String)
    setup_time = Column(String)
    location = Column(String)
    contact_name = Column(String)
    contact_mobile = Column(String)
    contact_email = Column(String)
    contact_wechat = Column(String)
    address = Column(String)
    similar_ids = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    lastmodified_at = Column(DateTime)

    country = Column(String)
    source_link = Column(String)
    docs = Column(String)
    valuation = Column(String)
    valuation_time = Column(String)


class ServerProductCompany(Base, ProductCompanyTo):
    __tablename__ = "hub_products_test"
    __table_args__ = (UniqueConstraint('name', 'company_name', 'website'),)







