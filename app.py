from flask import Flask

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])

def index():
    try:
        pass
    except:
        pass

    return "Just passing through app.py"

if __name__ == "__main__":
    app.run(debug=True)

