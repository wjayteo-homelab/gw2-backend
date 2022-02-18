# import asyncio
import traceback
import flask

from stuff import dailies

flask_app = flask.Flask(__name__)
flask_app.config["DEBUG"] = False
ERROR_KEY = "error"


def make_response(data, status: int) -> flask.Response:
    return flask.make_response(flask.jsonify(data), status)


@flask_app.route("/", methods=["GET"])
def home():
    return "<div style='font-family: arial; position:fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);'>" \
           "A turtle made it to the water!" \
           "</div>"


@flask_app.route("/dailies", methods=["GET"])
async def test():
    try:
        result: dict = await dailies.get_dailies()
        return make_response(result, 200)
    except Exception as e:
        flask_app.logger.error(f"{e}")
        traceback.print_exc()
        print()
        return make_response({ERROR_KEY: "Unable to retrieve dailies."}, 500)

    # tries: int = 0
    #
    # while tries < 3:
    #     try:
    #         result: dict = await dailies.get_dailies()
    #         return make_response(result, 200)
    #     except Exception as e:
    #         flask_app.logger.error(f"{e}")
    #         traceback.print_exc()
    #         tries += 1
    # return make_response({ERROR_KEY: "Unable to retrieve dailies."}, 500)


@flask_app.route("/togglemax", methods=["GET"])
def toggle_max():
    dailies.toggle_max_level_only()
    return make_response({}, 200)


if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("Backend ready.")
    print()
    flask_app.run(host="0.0.0.0", port=5000)
