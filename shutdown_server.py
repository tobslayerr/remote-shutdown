from flask import Flask, render_template, request, redirect, url_for, session
import os
import platform

app = Flask(__name__)
app.secret_key = "387611"

USERNAME = "Admin"
PASSWORD = "387611vkvm"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(f"Username received: {username}")
        print(f"Password received: {password}")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("control"))
        else:
            return "Password atau kata sandi salah", 401
    return render_template("login.html")

@app.route("/control", methods=["GET", "POST"])
def control():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    if request.method == "POST":
        action = request.form.get("action")
        system_name = platform.system()

        if action == "shutdown":
            if system_name == "Windows":
                os.system("powershell Stop-Computer")
            elif system_name == "Linux" or system_name == "Darwin":
                os.system("shutdown now")
            return "Laptop telah dimatikan daya.."
        
        elif action == "sleep":
            if system_name == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif system_name == "Linux":
                os.system("systemct1 suspend")
            elif system_name == "Darwin":
                os.system("pmset sleepnow")
            return "Laptop telah beralih ke sleep.."
        
    return render_template("control.html")  

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 