from flask import Flask , render_template, request, redirect,  url_for
app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():

	if request.method == "POST":
		direc_path = request.form["dir"]
		return redirect(url_for("progress", direc_path = direc_path))

	return render_template('home.html')

@app.route("/<direc_path>")
def progress(direc_path):
	return render_template('progress.html' , direc_path = direc_path)



'''
home has input for username & direc :
When entered redirects to progress
'''

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

'''
Progress first shows the username and direc . Also has a logout option to clear 
the session info..
'''
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

'''
Logout that erases all the existing session info ..
'''
@app.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("direc_path",None)
    return redirect(url_for("home"))
































if __name__ == "__main__":
	app.run(debug = True)