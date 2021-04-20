import ast
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.httputil
import os.path
import random
# import dumps
from json import JSONEncoder
from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet
import string
from pymongo import errors
import json
import random
import requests
from database.database import database
from bson.json_util import dumps
from bson.objectid import ObjectId

tornado.options.parse_command_line()
tornado.options.define("port", default=2222,
                       help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        self.db_equipment = database('equipment')

        handlers = [
            (r"/", IndexHandler),
            (r"/issuedManager", IssuedManager),
            (r"/getEquipment", CreateEquipment),
            (r"/getSpecificEquipmentIssueEquipment",
             SpecificEquipmentIssueEquipment),
            (r"/isseuEquipment", IssueEquipment)
        ]
        tornado.web.Application.__init__(self, handlers)


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, DELETE, PUT')

    def options(self):
        self.write("Dashboard Server up and running")


class IndexHandler(BaseHandler):
    """
    Checking server status
    """

    def get(self):
        self.write("Radicali Home Test Server up and running")

# returns the issued Equipments


class IssuedManager(BaseHandler):
    def get(self):
        data = self.application.db_equipment.read_clean(
            {'status': 'NA'})
        self.write(dumps(data))

# Issue the equipment which are in pending state


class IssueEquipment(BaseHandler):
    # user_id Defines to whom issued
    def get(self):
        idd = self.get_argument("id")
        data = self.application.db_equipment.read_clean({'issued': 'pending'})
        res = self.application.db_equipment.update(
            {'id': int(idd)}, {'$set': {'status': 'NA', 'current_owner': 'user_id', 'issued': 'Success'}})
        if res == 'Success':
            self.write('Equipment issued Successfully')


class CreateEquipment(BaseHandler):

    # Return the available equipments
    def get(self):
        data = self.application.db_equipment.read_clean(
            {'status': 'Available'})
        self.write(dumps(data))

    # creates the equipment
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        equipment_id = data['id']
        equipment_name = data["equipment_name"]
        status = data["status"]
        current_owner = data["current_owner"]

        if equipment_name == '':
            self.write("Please enter the Equipment name")

        elif status != 'NA' and status != 'Available':
            self.write("Please enter status as 'NA' or 'Available'")

        elif current_owner == '':
            self.write("Current owner must be Filled")
        else:

            equipment_data = {
                "id": equipment_id,
                "equipment_name": equipment_name,
                "status": status,
                "current_owner": current_owner,
                "issued": "pending"

            }
            result = self.application.db_equipment.read_clean(
                {'id': equipment_id})
            if len(result):
                self.write('Equipment already Exists')
                self.write(dumps(data))
            else:

                res = self.application.db_equipment.insert(equipment_data)
                if res == 'Success':
                    self.write("Success fully added")


class SpecificEquipmentIssueEquipment(BaseHandler):
    # returns the specfic equipment
    def get(self):
        id = self.get_argument("id")
        data = self.application.db_equipment.read_clean({'id': int(id)})
        print(data)
        if len(data) == 0:
            self.write("Equipment does not exists")
        else:

            self.write(dumps(data))

    # Return of the Eqipment
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        res = self.application.db_equipment.update(
            {'id': data['id']}, {'$set': {'status': 'Available', 'issued': 'pending'}})
        if res == 'Success':
            self.write("Successfully return the Equipment")


def main():
    try:
        tornado.options.options.port = int(sys.argv[1])
    except:
        tornado.options.options.port = 2222
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
