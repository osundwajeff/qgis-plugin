import logging

from flask import Flask, request, jsonify
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the lowest level to capture debug and above logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Directs logs to the terminal
    ]
)

@app.route("/v2.1/connect/token", methods=["POST"])
def token():
    if (
        request.form.get("grant_type") == "password"
        and request.form.get("client_id") == "test"
        and request.form.get("username") == "test"
        and request.form.get("password") == "test"
        and request.form.get("client_secret") == "test.secret"
    ):
        response = {
            "access_token": "token",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "offline_access openid"
        }
        return jsonify(response)
    else:
        print(f"Problem in authentication {request.form}")
        app.logger.error(f"Problem in authentication {request.form}")
        return jsonify({"error": "invalid_request"}), 400


@app.route("/field-level-maps/v4/coverage", methods=["POST"])
def field_level_maps_coverage():
    if request.headers.get("accept") != "application/json" or \
       request.headers.get("content-type") != "application/json":
        return jsonify({"error": "Invalid headers"}), 400

    data = request.get_json()
    if not data or "Geometry" not in data or "Crop" not in data or "SowingDate" not in data:
        return jsonify({"error": "Invalid data input"}), 400

    response = [
        {
            "coverageType": "CLEAR",
            "image": {
                "id": "IKc73hpUQ726BpoqhQpaU8SfYGFYTAL5hhyYZq4PwFY",
                "sensor": "SENTINEL_2",
                "soilMaterial": "BARE",
                "weather": "COLD",
                "date": "2024-11-02"
            },
            "maps": [{}]
        }
    ]
    return jsonify(response)

@app.route("/field-level-maps/v4/maps/base-reference-map/<string:string_id>", methods=["POST"])
def base_reference_map(string_id):
    if request.headers.get("accept") != "application/json" or \
       request.headers.get("content-type") != "application/json":
        return jsonify({"error": "Invalid headers"}), 400

    data = request.get_json()
    if not data or "SeasonField" not in data or "Image" not in data:
        return jsonify({"error": "Invalid data structure"}), 400

    response = {
        "id": "09BLXmtcED029BKAoVnjZKEQ",
        "externalIds": {},
        "seasonField": {
            "id": "seasonfield_id",
            "externalIds": {
                "id": "1LYkyW0ykCTFTpLEYZrMr9",
                "legacY_ID_NA": "nja3zv9"
            },
            "customerExternalId": None
        },
        "_links": {},
        "index": 0,
        "hotSpots": [],
        "legend": {},
        "zones": [],
        "date": "2024-10-21"
    }
    return jsonify(response)

@app.route("/field-level-maps/v4/maps/difference-map/<string:string_id>", methods=["POST"])
def difference_map(string_id):
    if request.headers.get("accept") != "application/json" or request.headers.get("content-type") != "application/json":
        return jsonify({"error": "Invalid headers"}), 400

    data = request.get_json()
    if not data or "SeasonField" not in data or "EarliestImage" not in data or "LatestImage" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    response = {
        "id": "09BLXmtcED029BKAoVnjZKEQ",
        "externalIds": {},
        "seasonField": {
            "id": "seasonfield_id",
            "externalIds": {
                "id": "1LYkyW0ykCTFTpLEYZrMr9",
                "legacY_ID_NA": "test"
            },
            "customerExternalId": None
        },
        "_links": {},
        "index": 0,
        "hotSpots": [],
        "legend": {},
        "zones": [],
        "date": "2024-10-21"
    }
    return jsonify(response)

@app.route("/field-level-maps/v4/maps/management-zones-map/<string:map_type>", methods=["POST"])
def management_zones_map(map_type):
    if request.headers.get("accept") != "application/json" or request.headers.get("content-type") != "application/json":

        return jsonify({"error": "Invalid headers"}), 400

    data = request.get_json()
    if not data or "SeasonField" not in data or "Images" not in data or "params" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    zone_count = data.get('params').get("zoneCount")
    if zone_count is None:
        return jsonify({"error": "Invalid or missing query parameter 'zoneCount'"}), 400

    response = {
        "id": "OPs0I035tUCMwrUOqPSi4g",
        "externalIds": {},
        "seasonField": {
            "id": "seasonfield_id",
            "externalIds": {
                "id": "1LYkyW0ykCTFTpLEYZrMr9",
                "legacY_ID_NA": "id"
            },
            "customerExternalId": None
        },
        "_links": {},
        "index": 0,
        "hotSpots": [],
        "legend": {},
        "zones": []
    }
    return jsonify(response)
