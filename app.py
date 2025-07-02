from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv(".env")
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html', title= "Home - Aditya Mishra", current_path=request.path, show_footer =False)

@app.route('/about')
def about():
    return render_template('about.html',title= "About - Aditya Mishra", current_path=request.path)

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name') # Use .get() to avoid KeyError if field is missing
        email = request.form.get('email')
        message = request.form.get('message')

        # --- Input Validation ---
        if not name or not email or not message:
            flash("Please fill in all the fields.", 'error')
            return redirect(url_for('contact')) # Redirect back to the contact page to show the error

        # Prepare the email
        msg = Message(subject=f"New Contact from {name}",
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

        try:
            mail.send(msg)
            flash("Message sent successfully!", 'success')
        except Exception as e:
            flash(f"Failed to send email: {e}", 'error') # Flash the specific error for debugging
            # Optionally log the error: app.logger.error(f"Mail send failed: {e}")
            # return f"Failed to send email: {e}" # Removed this as it breaks the flash message flow
    return render_template('contact.html', title="Contact - Aditya Mishra", current_path=request.path, show_footer =True)

@app.route('/project')
def project():
    return render_template('project.html',title= "Project - Aditya Mishra", current_path=request.path, show_footer =True)

@app.route('/donate')
def donate():
    return render_template('donate.html',title= "Donate - Aditya Mishra", current_path=request.path)
@app.route('/footer')
def footer():
    return render_template('footer.html', current_path=request.path )
if __name__ == '__main__':
    app.run(debug=True)