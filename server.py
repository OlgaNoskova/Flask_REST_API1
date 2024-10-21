import flask
import pydantic
from flask import jsonify, request
from flask.views import MethodView

import schema
from models import Session, Advertisement
from sqlalchemy.exc import IntegrityError

app = flask.Flask('app')


class HttpError(Exception):

    def __init__(self, status_code: int, error_message: dict | str | list):
        self.status_code = status_code
        self.error_message = error_message


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"error": er.error_message})
    response.status_code = er.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response


def validate(json_data: dict, schema_cls: type[schema.CreateAdvertisement]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)


def get_advertisement_by_id(advertisement_id):
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    return advertisement


def add_advertisement(advertisement):
    request.session.add(advertisement)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "advertisement already exists22")
    return advertisement


class AdvertisementView(MethodView):
    def get(self, advertisement_id):
        advertisement = get_advertisement_by_id(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        json_data = validate(request.json, schema.CreateAdvertisement)
        advertisement = Advertisement(**json_data)
        advertisement = add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id: int):
        advertisement = get_advertisement_by_id(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"status": "deleted"})


advertisement_view = AdvertisementView.as_view("advertisement")

app.add_url_rule("/advertisement/", view_func=advertisement_view, methods=["POST"])
app.add_url_rule("/advertisement/<int:advertisement_id>", view_func=advertisement_view, methods=["GET", "DELETE"])

app.run()
