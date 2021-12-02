import asyncio
import flask

from stuff import dailies, map_data

flask_app = flask.Flask(__name__)
flask_app.config["DEBUG"] = False
ERROR_KEY = "error"
MAP_DATA: dict = {}


def make_response(data, status: int) -> flask.Response:
    return flask.make_response(flask.jsonify(data), status)


@flask_app.before_first_request
async def before_first_request():
    global MAP_DATA
    try:
        MAP_DATA = await map_data.crawl_map_data()
    except Exception as e:
        flask_app.logger.error(f"Error while crawling map data: {e}")


@flask_app.route("/", methods=["GET"])
def home():
    return "<div style='font-family: arial; position:fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);'>" \
           "A turtle made it to the water!" \
           "</div>"


@flask_app.route("/dailies", methods=["GET"])
async def test():
    try:
        result: dict = await dailies.get_dailies(MAP_DATA)
        return make_response(result, 200)
    except Exception as e:
        flask_app.logger.error(f"Error while getting dailies: {e}")
        return make_response({ERROR_KEY: "Unable to retrieve dailies."}, 500)


if __name__ == "__main__":
    print("Backend ready.")
    print()
    flask_app.run(host="0.0.0.0", port=5000)
