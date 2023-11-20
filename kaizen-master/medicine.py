import xmlrpclib
import base64
import csv
import random
import psycopg2
from pprint import pprint
import logging
import uuid
import os

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'K5_001'    #the database
try:
    conn = psycopg2.connect("dbname='K5_001' user='postgres' host='localhost' password='123'")
    print ">>>>>>>>>>>>>>>>>>HIHIHIHIHIHI>>>>>>>>>>>>>>>>>>>>>>",conn
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
sock_common = xmlrpclib.ServerProxy ('http://localhost:1111/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:1111/xmlrpc/object')
with open('medicine.csv', 'rb') as patient_file:
    patient_datas = csv.reader(patient_file, delimiter=',', quotechar='"')
    code_seq = 0
    sequence = 0

    for row in patient_datas:
        print "row >>>>>>>>>>>>>>>>>>>>>", row
        if not code_seq:
            sequence += 1
            code_seq = 1
        else:
            sequence += 1
            domain = [('product_id', '=', int(row[0]))]
            res_id = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('name', '=', row[1].replace("'", "''"))])
            content_name = row[2]
            content_id = None
            values = {
                    'name': row[1].replace("'", "''"),
                    #'common_dosage':row[3],
                    'purchase_ok': True,
                    'sale_ok': True,
                    'type': 'consu',
                    'hospital_product_type': 'medicament',
                    'used_in': 'both',
                    'uom_id': 1,
                    'uom_po_id':1,
                    'categ_id':1,
                    #'tracking':1,
                    'active': True
                }
            if content_name:
                content_id = sock.execute(dbname, uid, pwd, 'medicament.content', 'search', [('name', '=', content_name)])
                content_id = content_id and content_id[0] or None
                if not content_id:
                   content_id = sock.execute(dbname, uid, pwd, 'medicament.content', 'create', {"name": content_name})
                values['content_ids'] = [(4, content_id)]
                cur.execute("""select template_id from medicament_content_rel""")
                prod_medicament_content_rel = cur.fetchall()
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>prod_medicament_content_rel>>>", prod_medicament_content_rel
                res_id = sock.execute(dbname, uid, pwd, 'product.template', 'search', [('content_ids', '=', content_id),('name', '=', row[1].replace("'", "''"))])
            if not res_id:
                print ">>>>>>>>>>>product_val>>>create>>>>>>>>>>>",values            
                partner_id = sock.execute(dbname, uid, pwd, 'product.template', 'create', values)     
            else:
                print ">>>>>>>>>>>product_val>>>write>>>>>>>>>>>",values 
                partner_id = sock.execute(dbname, uid, pwd, 'product.template', 'write', res_id, values)
