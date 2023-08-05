import json
import aiohttp_cors
from aiohttp import web
from db import Database

db = Database()
routes = web.RouteTableDef()


@routes.view('/users')
class UsersManager(web.View, aiohttp_cors.CorsViewMixin):

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
class UsersManager(web.View, aiohttp_cors.CorsViewMixin):

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
class UsersManager(web.View, aiohttp_cors.CorsViewMixin):

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
class UsersManager(web.View, aiohttp_cors.CorsViewMixin):

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

app.add_routes(routes)
cors = aiohttp_cors.setup(app, defaults={
    "http://horse-front.duckdns.org/": aiohttp_cors.ResourceOptions(),
})
for route in list(app.router.resources()):
    cors.add(route)
