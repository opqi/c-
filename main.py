from aiohttp import web
from aiojobs.aiohttp import setup, spawn
from db import init_db, create_request
from routes import setup_routes
from settings import load_config, PACKAGE_NAME


async def init_app(config):
    app = web.Application()
    app['config'] = config
    setup_routes(app)

    await init_db(app)
    setup(app)
    return app


def main(configpath):
    config = load_config(configpath)
    app = init_app(config)
    web.run_app(app, host=config['host']['SE_HOST'],
                port=config['host']['SE_PORT'])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
