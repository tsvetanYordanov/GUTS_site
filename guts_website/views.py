# VIEWS
# =============================================
# Defines the views of the application. Each address renders a template
# from templates folder

import os, re, requests, json, hashlib, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, send_from_directory, session, redirect, url_for, jsonify
from guts_website import app, models, db, users
from guts_website.sensitive import FB_PAGE_ID, FB_ACCESS_TOKEN, GALLERY_PATH, HASH_SALT, EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER

from forms import LoginForm, EmailForm, AddEventForm, EditEventForm, AddProjectForm, SubscriptionsForm
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user)
                            
from sqlalchemy import Date, cast, and_, not_
from datetime import datetime

@app.route('/')
def show_main():
    form = EmailForm()
    if form.validate_on_submit():
        pass
    return render_template('home.html', form = form)

@app.route('/meetings')
def show_meetings():
    #current_events = models.Events.query.filter(and_(models.Events.dtstart <= datetime.now(),models.Events.dtend >= datetime.now())).all() 
    now = datetime.now()
    events = models.Event.query.filter(models.Event.dtend >= datetime.now()).order_by(models.Event.dtstart.asc()).all()
    past_events = models.Event.query.filter(models.Event.dtend < datetime.now()).order_by(models.Event.dtstart.desc()).all()
    return render_template('meetings.html', events = events, past_events = past_events, now = now)
    
@app.route('/projects')
def show_projects():
    projects = models.Project.query.order_by(models.Project.id.desc()).all();
    return render_template('projects.html', projects = projects)

@app.route('/hackathon')
def show_hackathon():
    form = EmailForm()
    return render_template('hackathon.html', form = form)
    
@app.route('/sponsors')
def show_sponsors():
    return render_template('sponsors.html')

@app.route('/contacts')
def show_contacts():
    return render_template('contacts.html')
    
@app.route('/submit', methods = ['POST'])
def show_submit():
    if (request.form["isGU"] == "true"):
        if not re.match(r"\d{7}[a-zA-Z]", request.form["gu_email"]):
            return "INVALID_EMAIL"
        finalEmail = request.form["gu_email"] + "@student.gla.ac.uk"
    else:
        finalEmail = request.form["other_email"] 
        if not re.match(r"(\w+[.|\w])*@(\w+[.])*\w+", finalEmail):
            return "INVALID_EMAIL"
    c = models.Member.query.filter(models.Member.email == finalEmail).first()
    
    if (c):
        return "EMAIL_EXISTS"
    elif (request.form["isGU"] == "false" and request.form["confirm_gu"] != "true"):
        return "NOT_GU"
    else:
        e = models.Member(
          fullname = request.form["fullname"], 
          email = finalEmail, 
          gumail = 1 if request.form["isGU"] == "true" else 0
        )
        db.session.add(e)
        db.session.commit()
        return finalEmail

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/hackathon_details.pdf')
def hackathon_details():
    return send_from_directory(app.static_folder, request.path[1:])
    
@app.route('/get_galleries_files')
def galleries():
    gid = request.args.get('gallery_id');
    return jsonify({"files":[x for x in os.listdir(os.path.join(GALLERY_PATH,gid,'t'))]});
    
@app.route('/get_events')
def get_events():
    eid = request.args.get("event_id")
    if (eid):
        events = models.Event.query.filter(models.Event.id == eid).all();
    else:
        events = models.Event.query.all();
    return jsonify(posts=list(events));
    
@app.route('/get_projects')
def get_projects():
    pid = request.args.get("project_id")
    if (pid):
        projects = models.Project.query.filter(models.Project.id == pid).all();
    else:
        projects = models.Project.query.all();
    return jsonify(posts=list(projects));

@app.route('/get_technologies')
def get_technologies():
    tid = request.args.get("technology_id")
    if (tid):
        technologies = models.Technology.query.filter(models.Technology.id == tid).all();
    else:
        technologies = models.Technology.query.all();
    return jsonify(posts=list(technologies));
    
@app.route('/get_platforms')
def get_platforms():
    pid = request.args.get("platform_id")
    if (pid):
        platforms = models.Platform.query.filter(models.Platform.id == pid).all();
    else:
        platforms = models.Platform.query.all();
    return jsonify(posts=list(platforms));
   
################################################################################
##########################         LOGIN         ###############################

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return users.USERS.get(int(id))


@app.route('/admin_page', methods = ['GET', 'POST'])
@login_required
def admin():
    form_event_add = AddEventForm()
    form_event_edit = EditEventForm()
    form_project_add = AddProjectForm()
    if request.method == 'GET':
        members = models.Member.query.all();
        events = models.Event.query.all();
        projects = models.Project.query.all();
        technologies = models.Technology.query.all();
        return render_template('admin.html', 
                                form_event_add = form_event_add, 
                                form_event_edit = form_event_edit,
                                form_project_add = form_project_add,
                                members = members, 
                                projects = projects, 
                                technologies = technologies
                                )
    if request.method == 'POST':
        action = request.form.get('action');
        if (action == "event-add"):
            d = {}
            for k,v in request.form.items():
                if (k == "action" or k == "csrf_token"):
                    continue
                d[k] = v
            event = models.Event(**d)
            db.session.add(event)
            db.session.commit()
            return "Added event."
        elif (action == "event-edit"):
            event_id = request.form.get('id');
            d = {}
            for k,v in request.form.items():
                if (k == "action" or k == "csrf_token" or k == 'id'):
                    continue
                d[k] = v
            
            #return str(d);
            db.session.query(models.Event).filter(models.Event.id == event_id).update(d);
            db.session.commit()
            return "Edited event."
        elif (action == "event-remove"):
            event_id = request.form.get('event_id');
            db.session.query(models.Event).filter(models.Event.id == event_id).delete();
            db.session.commit();
            return "Removed event."
        else:
            return "Fail"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']
        
        if username in users.USER_NAMES:
            user = users.USER_NAMES[username]
        else:
            error = 'Invalid username'
            return render_template('login.html',form = form, error=error)

        if user.check_password(password) == False:
            error = 'Invalid password'
            return render_template('login.html', form = form, error=error)
        else:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(users.USER_NAMES[username], remember=remember):
                session['logged_in'] = True
                return redirect(request.args.get("next") or url_for('admin'))
            else:
                error = "Could not login because login_user failed"
                return render_template('login.html', form = form, error = error)
    elif request.method == "GET":
        return render_template('login.html', form = form)
    else:
        error = "Please supply both a username and password"
        return render_template('login.html', form = form, error = error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_main'))
    
@app.route('/ufb', methods=['POST'])
def create_fb_event():
    url = "https://graph.facebook.com/" + FB_PAGE_ID +"/events"
    params = {
        'access_token': FB_ACCESS_TOKEN, 
        'name': request.form["title"],
        'start_time': '2013-09-26T19:00:00+0100',
        'end_time': '2013-09-26T20:00:00+0100',
        'description': request.form["description"],
        'location': request.form["location"]
    }
    r = requests.post(url, data = params)
    json_data = json.loads(r.text)
    return json_data["id"]
    
@app.route('/subscription_update', methods=['POST'])
def sub_status():
    email = request.form.get("email")
    req_key = request.form.get("req_key")
    write_key = models.Member.query.filter(models.Member.email == email).first().write_key;
    sub_meetings = 1 if request.form.get("sub_meetings") == 'y' else 0
    sub_hackathon = 1 if request.form.get("sub_hackathon") == 'y' else 0
    if (write_key != req_key):
        return "FAIL" + write_key + req_key
    else:
        db.session.query(models.Member).filter(models.Member.email == email).update({models.Member.sub_meetings: sub_meetings})
        db.session.query(models.Member).filter(models.Member.email == email).update({models.Member.sub_hackathon: sub_hackathon})
        db.session.commit()
        return "OK"
    
@app.route('/subscription')
def sub_manage():
    email = request.args.get("email")
    req_key = request.args.get("req_key")
    try:
        sub_meetings = models.Member.query.filter(models.Member.email == email).first().sub_meetings;
        sub_hackathon = models.Member.query.filter(models.Member.email == email).first().sub_hackathon;
        write_key = models.Member.query.filter(models.Member.email == email).first().write_key;
    except:
        return "Invalid request."
    if (req_key != write_key):
        return "Invalid key."
    else:
        form = SubscriptionsForm();
        form.email.data = email
        form.req_key.data = req_key
        form.sub_meetings.data = sub_meetings
        form.sub_hackathon.data = sub_hackathon
        return render_template('subscription.html', form=form, email=email)
        
#@app.route('/gen_keys')
#@login_required
#def gen_keys():
#    members = models.Member.query.all();
#    final = ""
#    for m in members:
#        e = m.email
#        h = hashlib.sha1(e+HASH_SALT).hexdigest()
#        db.session.query(models.Member).filter(models.Member.email == e).update({models.Member.write_key: h})
#        db.session.commit()
#        final += e + ": " + h + "<br>"
#    return "OK<br>"+final

@app.route('/email_template', methods=['GET'])
@login_required
def template():
    subject = "Glasgow University Tech Society Meeting"
    sender = "team@gutechsoc.com"
    members = models.Member.query.all();
    
    recipient = "1103581t@student.gla.ac.uk"
    req_key = models.Member.query.filter(models.Member.email == recipient).first().write_key;
    
    event = models.Event.query.filter(models.Event.id == request.args.get('event_id')).first()
    time = event.dtstart
    
    return render_template('email_template.html', 
                           subject = subject, 
                           recipient = recipient, 
                           req_key = req_key,
                           title = event.title,
                           description = event.description,
                           fb_event = event.fb_event,
                           time = time,
                           location = event.location)

@app.route('/email_hackathon', methods=['GET'])
@login_required
def email_hackathon():
    description =         description = "This is it! We are thrilled to announce that the tickets for Glasgow University Tech Society's first ever hackathon are now available for <a href='http://www.eventbrite.co.uk/event/8778636137?nomo=1'>reservation</a>! Join us on the 1st-3rd of November with faces from industry and academia for the most creative 29 hours of your life. Did I forget to mention the free Domino's pizzas and awesome prizes? Hurry up, the tickets are selling as we speak!  Entry only 5 pounds per person! <br><br> We look forward to seeing you all there :)"
    time="1-3 November"
    return render_template ('email_hackathon.html', 
                           description = description,
                           time = time)

@app.route('/send_email')
@login_required
def send_mail():
    subject = "Glasgow University Tech Society Meeting"
    sender = EMAIL_ADDRESS
    
    members = models.Member.query.all();
    event = models.Event.query.filter(models.Event.id == request.args.get('event_id')).first()
    
    print("e"+str(event.id))
     # Send the message via local SMTP server.
    # server = smtplib.SMTP('smtp.gmail.com',587)             # gmail port 465 or 587 
    server = smtplib.SMTP_SSL(SMTP_SERVER,465) # godaddy
    server.ehlo()                                             # both
    #server.starttls()                                        # gmail
    #server.ehlo()                                            # gmail
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)         # both
    
    for m in members:
        recipient = m.email
        req_key = m.write_key;

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        title = event.title
        description = event.description
        fb_event = event.fb_event
        location = event.location
        time="3rd October, 5 - 9 pm"
        # Create the body of the message (a plain-text and an HTML version).
        text = "Glasgow University Tech Society team has the pleasure of inviting you to a special event.\n\n"+title+"--------------------------------------------------\n\nWhen: "+time+"\nWhere: "+location+"--------------------------------------------------\n"+description+"--------------------------------------------------\n\n"+"To edit your subscription settings, visit: http://www.gutechsoc.com/subscription?email="+recipient+"&req_key="+req_key+"\n"
        html = render_template('email_template.html', 
                           subject = subject, 
                           recipient = recipient, 
                           req_key = req_key,
                           title = title,
                           description = description,
                           fb_event = fb_event,
                           time = time,
                           location = location)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

       
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        try:
            server.sendmail(sender, recipient, msg.as_string())
            print "Sent email to " + recipient
        except SMTPException:
            print "Failed to send email to " + recipient
    server.quit()
    return "sent!"

@app.route('/send_email_hackathon')
@login_required
def send_mail_hackathon():
    subject = "GUTS Hackathon Event"
    sender = EMAIL_ADDRESS
    
    members = models.Member.query.all();
    
     # Send the message via local SMTP server.
    # server = smtplib.SMTP('smtp.gmail.com',587)             # gmail port 465 or 587 
    server = smtplib.SMTP_SSL(SMTP_SERVER,465) # godaddy
    server.ehlo()                                             # both
    #server.starttls()                                        # gmail
    #server.ehlo()                                            # gmail
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)         # both
    
    for m in members:
        recipient = m.email
        req_key = m.write_key;

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        description = "This is it! We are thrilled to announce that the tickets for Glasgow University Tech Society's first ever hackathon are now available for <a href='http://www.eventbrite.co.uk/event/8778636137?nomo=1'>reservation</a>! Join us on the 1st-3rd of November with faces from industry and academia for the most creative 29 hours of your life. Did I forget to mention the free Domino's pizzas and awesome prizes? Hurry up, the tickets are selling as we speak! Entry only 5 pounds per person! <br><br> We look forward to seeing you all there :)"
        time="1-3 November"
        # Create the body of the message (a plain-text and an HTML version).
        text = "Tech Society has the pleasure of inviting you to the hackathon event of the year!\n\n--------------------------------------------------\n\nWhen: "+time+"\n--------------------------------------------------\n"+description+"--------------------------------------------------\n\n"+"To edit your subscription settings, visit: http://www.gutechsoc.com/subscription?email="+recipient+"&req_key="+req_key+"\n"
        html = render_template('email_hackathon.html', 
                           subject = subject, 
                           recipient = recipient, 
                           req_key = req_key,
                           description = description,
                           time = time)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

       
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        try:
            server.sendmail(sender, recipient, msg.as_string())
            print "Sent email to " + recipient
        except SMTPException:
            print "Failed to send email to " + recipient
    server.quit()
    return "sent!"






















