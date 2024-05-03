from flask import Flask, request, redirect, jsonify 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
from flask import Flask, render_template
from flasgger import Swagger
import os
import logging

app = Flask(__name__)
swagger = Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    shortcode = db.Column(db.String(6), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_redirect = db.Column(db.DateTime)
    redirect_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.errorhandler(500)
def handle_server_error(e):
        """
        Handle server errors.
        ---
        responses:
            500:
                description: Internal server error.
        """
        app.logger.error(f"Server error: {e}")
        return jsonify(error='Internal server error'), 500


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Create a new shortened URL.
    ---
    parameters:
      - name: url
        in: body
        type: string
        required: true
        description: The URL to shorten.
      - name: shortcode
        in: body
        type: string
        description: The desired shortcode.
    responses:
      201:
        description: The shortcode of the new URL.
    """
    data = request.get_json()

    # Validate the input
    if 'url' not in data:
        return jsonify(error='Url not present'), 400

    shortcode = data.get('shortcode')

    # Validate the shortcode
    if shortcode is not None and (len(shortcode) != 6 or not shortcode.isalnum() or shortcode not in (string.ascii_uppercase + string.ascii_letters + string.digits + "_")):
        return jsonify(error='Shortcode must be 6 characters long and contain only alphanumeric characters or underscores'), 412
    
    # Check if the shortcode is already in use
    if shortcode:
        if URL.query.filter_by(shortcode=shortcode).first():
            return jsonify(error='Shortcode already in use'), 409
    else:
        # Generate a random shortcode
        shortcode = ''.join(random.choices("_" + string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))

    # Create a new URL record
    new_url = URL(url=data['url'], shortcode=shortcode)
    db.session.add(new_url)
    db.session.commit()

    return jsonify(shortcode=shortcode), 201


@app.route('/<shortcode>', methods=['GET'])
def redirect_to_url(shortcode):
    """
    Redirect to the URL associated with the provided shortcode.
    ---
    parameters:
      - name: shortcode
        in: path
        type: string
        required: true
        description: The shortcode of the URL.
    responses:
      302:
        description: Redirect to the URL associated with the shortcode.
      404:
        description: Shortcode not found.
    """
    # Query the database for the URL with the provided shortcode
    url = URL.query.filter_by(shortcode=shortcode).first()

    # If the URL is not found, return an error response
    if url is None:
        return jsonify(error='Shortcode not found'), 404

    # Update the 'last_redirect' and 'redirect_count' fields of the URL record
    url.last_redirect = datetime.utcnow()
    url.redirect_count += 1
    db.session.commit()

    # Redirect to the URL
    return redirect(url.url, code=302)


@app.route('/<shortcode>/stats', methods=['GET'])
def get_stats(shortcode):
    """
    Get the statistics of the URL associated with the provided shortcode.
    ---
    parameters:
      - name: shortcode
        in: path
        type: string
        required: true
        description: The shortcode of the URL.
    responses:
      200:
        description: The statistics of the URL.
        schema:
          type: object
          properties:
            created:
              type: string
              format: date-time
              description: The creation time of the URL.
            lastRedirect:
              type: string
              format: date-time
              description: The last redirect time of the URL.
            redirectCount:
              type: integer
              description: The redirect count of the URL.
            url:
              type: string
              description: The original URL.
      404:
        description: Shortcode not found.
    """
    # Query the database for the URL with the provided shortcode
    url = URL.query.filter_by(shortcode=shortcode).first()

    # If the URL is not found, return an error response
    if url is None:
        return jsonify(error='Shortcode not found'), 404

    # Return the statistics of the URL
    return jsonify(created=url.created, lastRedirect=url.last_redirect, redirectCount=url.redirect_count, url=url.url), 200

if __name__ == "__main__":
    os.environ['FLASK_APP'] = 'app.py'
    app.run(host="0.0.0.0", port=8000, debug=True)
