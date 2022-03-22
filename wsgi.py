"""Application entry point."""
from flask import Flask
from plotlyflask import init_app


app = init_app()


if __name__ == "__main__":
    # No HTTPS cert:
    #app.run(host='0.0.0.0', port='8050', ssl_context='adhoc', debug=True)
    app.run(host='0.0.0.0', port='8050', ssl_context=(
        'cert.pem', 'key.pem'), debug=True)
