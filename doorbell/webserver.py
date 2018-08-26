from flask import (
    Flask,
    render_template
)

# Create the application instance
app = Flask(__name__, root_path="../web")


# Create a URL route in our application for "/"
@app.route('/')
def home():
    return render_template('index.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
