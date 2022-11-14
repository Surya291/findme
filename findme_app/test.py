import base64
from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask , render_template, request, redirect,  url_for, session
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key= "findme"

'''
file uploads...
'''
@app.route('/upload')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        return render_template("success.html", name = f.filename)  

#app.permanent_session_lifetime = timedelta(minutes = 5)

# for showing images..
@app.route("/plot")
def plot():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, -1])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"



@app.route("/", methods = ["POST", "GET"])
def home():

    if request.method == "POST":

        user = request.form["nm"]
        direc_path = request.form["dir"]

        session["user"] = user
        session["direc_path"] = direc_path

        return redirect(url_for("progress"))

    elif "user" in session:
        return redirect(url_for("progress"))

    return render_template('home.html')

@app.route("/progress" , methods = ["POST", "GET"])
def progress():

    if request.method == "POST":
        return redirect(url_for("logout"))

    else:

        if ("user" in session):
            user = session["user"]
            direc_path = session["direc_path"]
            return render_template('progress.html' , user = user ,direc_path = direc_path)

        else:
            return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("direc_path",None)
    return redirect(url_for("home"))




if __name__ == "__main__":
    app.run(debug = True)