# app.py
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError

from models import SurveySubmission, StoredSurveyRecord
from storage import append_json_line, sha256_hex

app = Flask(__name__)
# Allow cross-origin requests so the static HTML can POST from localhost or file://
CORS(app, resources={r"/v1/*": {"origins": "*"}})

@app.route("/ping", methods=["GET"])
def ping():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })

@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "detail": "Body must be application/json"}), 400

    # Fill user_agent if missing
    payload.setdefault("user_agent", request.headers.get("User-Agent"))

    # Validate input
    try:
        submission = SurveySubmission(**payload)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": ve.errors()}), 422

    # Compute submission_id if not provided
    sub_id = submission.submission_id
    if not sub_id:
        hour_bucket = datetime.now(timezone.utc).strftime("%Y%m%d%H")
        sub_id = sha256_hex(f"{submission.email}{hour_bucket}")

    # Hash PII
    email_hash = sha256_hex(submission.email)
    age_hash = sha256_hex(str(submission.age))

    record = StoredSurveyRecord(
        submission_id=sub_id,
        name=submission.name,
        email_hash=email_hash,
        age_hash=age_hash,
        consent=submission.consent,
        rating=submission.rating,
        comments=submission.comments,
        source=submission.source,
        received_at=datetime.now(timezone.utc).isoformat(),
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or ""),
        user_agent=submission.user_agent,
    )

    append_json_line(record.dict())
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
