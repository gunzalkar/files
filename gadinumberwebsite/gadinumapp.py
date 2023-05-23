from flask import  Flask, jsonify, render_template, request, send_file,send_from_directory

app = Flask(__name__)

@app.route('/',methods=['GET'])
def shirt():
    return render_template('index.html')
@app.route('/',methods=['POST'])
def shirtpost():
    user = request.form['email']
    sub = request.form['subject']
    name = request.form['name']
    msg = request.form['msg']
    print("type: ",type(msg))
    msg = "Hello, I'm "+name+",\n email:"+user+"\n "+msg
    print("user: ", name)
    print("email: ",user)
    print("subject: ",sub)
    print("msg: ",msg)
    gmail_user = 'prasadnijai212@gmail.com'
    gmail_app_password = 'rggyateigdoqqoat'
    sent_from = gmail_user
    sent_to = ['prasadnijai212@gmail.com','gunzcorpllc@gmail.com','kshitijgunjalkar27@gmail.com']
    sent_subject = sub
    sent_body = msg
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (user, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
    return render_template('submission.html')
#-----------Errors ------------------


@app.errorhandler(404)
def page_not_found(error):
    er = "{}/{}".format(request.script_root, request.path)
    return render_template('error.html',er=er)

@app.errorhandler(413)
def page_not_found(error):
    return render_template('big_file.html')

import smtplib
@app.errorhandler(500)
def page_not_found(error):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        IP=request.environ['REMOTE_ADDR']
    else:
        IP=request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
    x={
    "IP": IP, 
    "Module": "server.html",
    "Content-Typed": "ERROR SERVER NOT FOUND (404)",
    "Timestamp": str(datetime.now())
    }
    json_object = json.dumps(x, indent=4)
    with open("log.json", "a") as outfile:
        outfile.write(json_object)
    
    '''gmail_user = 'prasadnijai212@gmail.com'
    gmail_app_password = 'rggyateigdoqqoat'
    
    sent_from = gmail_user
    sent_to = ['prasadnijai212@gmail.com','gunzcorpllc@gmail.com','kshitijgunjalkar27@gmail.com']
    sent_subject = "Error Occurred in Website."
    sent_body = ("This is Auto-generated mail from website\n\n"
                 "ERROR: 500\n"
                 "1) Login to SSH check if server is active or not.\n"
                 "2) Visit: https://beta.openai.com/playground and check if account got logged out automatically.\n"
                 "3) Restart the server.\n"
                 "4) If problem still persists, open SSH cmd and run following commands:\n"
                 "\tLogin as user prasad\n"
                 "\t\tsudo service nginx restart\n"
                 "\t\tsudo service app restart"
                 
                 "\nWebsite User.\n")

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)'''
    return render_template('servererror.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
