import json

import aiohttp_jinja2
import jinja2
from aiohttp import web

from db import Database

db = Database()
routes = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def return_site(request):
    return


@routes.view('/users')
class UsersManager(web.View):
    async def get(self):
        return web.json_response(json.dumps(db.get_all_users(), default=str), content_type='application/json')

    async def post(self):
        data = await self.request.json()
        print(data)
        db.update_data(data, 'users')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}

    async def delete(self):
        data = await self.request.json()
        print(data)
        db.delete_user(data, 'users')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}


@routes.view('/completed')
class UsersManager(web.View):
    async def get(self):
        return web.json_response(json.dumps(db.get_completed_data(), default=str), content_type='application/json')

    async def post(self):
        data = await self.request.json()
        print(data)
        db.update_data(data, 'completed')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}

    async def delete(self):
        data = await self.request.json()
        print(data)
        db.delete_user(data, 'completed')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}


@routes.view('/payments')
class UsersManager(web.View):
    async def get(self):
        return web.json_response(json.dumps(db.get_payments(), default=str), content_type='application/json')

    async def post(self):
        data = await self.request.json()
        print(data)
        db.update_data(data, 'payments')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}

    async def delete(self):
        data = await self.request.json()
        print(data)
        db.delete_user(data, 'payments')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}


@routes.view('/feedback')
class UsersManager(web.View):
    async def get(self):
        return web.json_response(json.dumps(db.get_feedback(), default=str), content_type='application/json')

    async def post(self):
        data = await self.request.json()
        print(data)
        db.update_data(data, 'feedback')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}

    async def delete(self):
        data = await self.request.json()
        print(data)
        db.delete_user(data, 'feedback')
        return web.json_response({'success': True}), 200, {'ContentType': 'application/json'}


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./front/dist'))
routes.static('/assets', './front/dist/assets')
app.add_routes(routes)

