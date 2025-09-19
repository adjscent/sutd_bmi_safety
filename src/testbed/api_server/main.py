import os
from flask import Flask, jsonify, request, redirect, url_for, render_template_string
import redis

app = Flask(__name__)

# connect to Redis (adjust URL/port as needed)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(redis_url, decode_responses=True)

ACTIONS = ["supination", "flexion", "grasp", "pronation", "extension", "open"]

TEMPLATE = """
<!doctype html>
<html>
  <head>
    <title>Action Flags</title>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>Toggle Actions</h1>
    <form method="post" action="{{ url_for('update_actions') }}">
      {% for name, val in state.items() %}
        <div>
          <label>
            <input type="checkbox" name="{{ name }}" {% if val %}checked{% endif %}>
            {{ name.capitalize() }}
          </label>
        </div>
      {% endfor %}
      <button type="submit">Save</button>
    </form>

    <hr>

    <button type="button" id="show-btn">Show Current Values</button>
    <pre id="output" style="background:#f4f4f4;padding:10px;"></pre>

    <script>
      document.getElementById('show-btn').addEventListener('click', function() {
        fetch('{{ url_for("get_actions") }}')
          .then(response => response.json())
          .then(data => {
            document.getElementById('output').textContent = JSON.stringify(data, null, 2);
          })
          .catch(err => {
            document.getElementById('output').textContent = 'Error: ' + err;
          });
      });
    </script>
  </body>
</html>
"""


with app.app_context():
    pipe = r.pipeline()
    for action in ACTIONS:
        pipe.setnx(action, 0)  # only set if not exists
    pipe.execute()


@app.route("/actions", methods=["GET"])
def get_actions():
    pipe = r.pipeline()
    for action in ACTIONS:
        pipe.get(action)
    vals = pipe.execute()
    # Redis stores strings, so convert to bool
    state = {a: bool(int(v or 0)) for a, v in zip(ACTIONS, vals)}
    return jsonify(state)


@app.route("/", methods=["GET"])
def index():
    return (
        get_actions()
        if request.accept_mimetypes.best == "application/json"
        else render_template_string(TEMPLATE, state=get_actions().get_json())
    )


@app.route("/actions", methods=["POST"])
def update_actions():
    form = request.form
    pipe = r.pipeline()
    for action in ACTIONS:
        # checkbox present → True (1), otherwise False (0)
        pipe.set(action, int(action in form))
    pipe.execute()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
