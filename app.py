import click
from flask import Flask
from app import app
from config import DevConfig, TestingConfig, ProductionConfig

def create_app(config_name):
    if (config_name == 'dev'):
        app.config.from_object('config.DevConfig')
    elif (config_name == 'test'):
        app.config.from_object('config.TestingConfig')
    elif (config_name == 'prod'):
        app.config.from_object('config.ProductionConfig')
    else:
        raise ValueError(f"Unknown Configuration: {config_name}")
    return app

@click.command()
@click.option('--config', default='dev', help='The configurations to use are (dev, test, prod)')
def cli(config):
    app = create_app(config)
    app.run(host="0.0.0.0")
    return app

if __name__ == "__main__":
    cli()