import os
import requests
from json import JSONDecodeError
from flask import Flask, jsonify, abort
from utils import gdrive, MetadataNotFound

MANIFEST = {
    "id": "dev.stremio.googledrive",
    "version": "1.0.7",
    "name": "dEV",
    "description": "If you know, you know.",
    "logo": "https://github.com/roydev19/hehe/raw/main/cover.jpg",
    "resources": ["stream"],
    "types": ["movie", "series"],
    "catalogs": []
}

app = Flask(__name__)
gd = gdrive()
gd.cf_proxy_url = os.environ.get('CF_PROXY_URL')


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    resp.headers['X-Robots-Tag'] = 'noindex'
    return resp


@app.route('/')
def init():
    return 'Addon is alive.'


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)


@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)
    try:
        return respond_with({'streams': gd.get_streams(type, id)})
    except MetadataNotFound as e:
        print(f'ERROR: {e}')
        abort(404)
    except JSONDecodeError as e:
        if id[:5] == 'kitsu':
            print(f'ERROR: Cloudflare anime kitsu 1020\n{e}')
        else:
            print(f'JSONDecodeError: Failed to fetch meta for {type} {id}\n{e}')
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
