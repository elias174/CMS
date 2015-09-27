from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for
)
mod_hello = Blueprint('hello_world', __name__, url_prefix='/hello_world')

@mod_hello.route('/hello_world/', methods=['GET', 'POST'])
def signin():
    return render_template("hello_world.html")
