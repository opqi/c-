from aiohttp import web, ClientSession
from aiojobs.aiohttp import setup, spawn
import hashlib
import uuid
import json
import sender
import db


async def fetch(session, url):
    async with session.get(url) as Response:
        resp = await Response.read()
        await session.close()
        return resp

async def count_hash(request, u_id):
    async with request.app['db_pool'].acquire() as conn:
        data = await db.get_data_by_id(conn, u_id)
    try:
        async with ClientSession() as session:
            md5_hash = await fetch(session, data['url'])
            md5_hash = str(hashlib.md5(md5_hash).hexdigest())

        async with request.app['db_pool'].acquire() as conn:
            await db.insert_hash(conn, u_id, 'done', md5_hash)
        if data['email']:
            sender.send_mail(data['email'], data['url'], md5_hash)
    except:
        async with request.app['db_pool'].acquire() as conn:
            await db.insert_hash(conn, u_id)


async def submit(request):
    try:
        u_id = str(uuid.uuid1())
        params = await request.text()
        info = dict(item.split("=", 1) for item in params.split("&", 1))
    except:
        resp_obj = {'status': '501 not implemented'}
        return web.Response(text=json.dumps(resp_obj) + '\n',
                            status=500)

    async with request.app['db_pool'].acquire() as conn:
        try:
            await db.create_request(conn, u_id, info['url'], info['email'])
            resp_obj = {'id': u_id}
            await spawn(request, count_hash(request, u_id))
            return web.Response(text=json.dumps(resp_obj) + '\n',
                                status=200)
        except:
            try:
                await db.create_request(conn, u_id, info['url'])
                resp_obj = {'id': u_id}
                await spawn(request, count_hash(request, u_id))
                return web.Response(text=json.dumps(resp_obj) + '\n',
                                    status=200)
            except:
                resp_obj = {'status': '501 not implemented'}
                return web.Response(text=json.dumps(resp_obj) + '\n',
                                    status=500)


async def check(request):
    try:
        u_id = request.query['id']
        try:
            async with request.app['db_pool'].acquire() as conn:
                data = await db.get_data_by_id(conn, u_id)

            if data['status'] == 'running':
                resp_obj = {'status': data['status']}
                return web.Response(text=json.dumps(resp_obj) + '\n',
                                    status=200)

            resp_obj = {'md5': data['md5_hash'],
                        'status': data['status'], 'url': data['url']}
            return web.Response(text=json.dumps(resp_obj, indent=1) + '\n',
                                status=200)
        except:
            resp_obj = {'status': '404 not found'}
            return web.Response(text=json.dumps(resp_obj) + '\n',
                                status=404)
    except:
        resp_obj = {'status': '501 not implemented'}
        return web.Response(text=json.dumps(resp_obj) + '\n',
                            status=501)
