import hmac
import hashlib
import json
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    body = request.data
    signature = request.headers['x-pyrus-sig']
    secret = 'eYyxPz-1VzrCVh3l7HvNYnKERPG3NEMqCAbFOap7cF5ovW7XWQhnZzABkq~e4jMR4e~dv0ACO5K8fTnOaeBFAVE2GfAa3-6C'

    if _is_signature_correct(body, secret, signature):
        return _prepare_response(body.decode('utf-8'))


def _is_signature_correct(message, secret, signature):
    secret = str.encode(secret)
    digest = hmac.new(secret, msg=message, digestmod=hashlib.sha1).hexdigest()
    return hmac.compare_digest(digest, signature.lower())


def _prepare_response(body):
    task = json.loads(body)["task"]
    task_author = task["author"]["email"]
    return "{{\"text\": \"Hello, {}. This task approved by bot.\", \"approval_choice\": \"approved\"}}".format(task_author)

 
if __name__ == '__main__':
    app.run()
