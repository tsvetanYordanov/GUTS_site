from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, HiddenField

class EmailForm(Form):
    fullname = TextField('fullname')
    gu_email = TextField('gu_email')
    other_email = TextField('other_email')
    confirm_gu = BooleanField('confirm_gu', default = False)
    
class LoginForm(Form):
    username = TextField('username')
    password = TextField('password')
    remember = BooleanField('remember', default = True)
    
    
class EventForm(Form):
    title = TextField('Title')
    icon = TextField('Icon')
    dtstart = TextField('Start date/time')
    dtend = TextField('End date/time')
    location = TextField('Location')
    description = TextAreaField('Description')
    map_query = TextField('Query for GMaps')
    
    
class AddEventForm(EventForm):
    action = HiddenField(default='event-add')
    fb_event = HiddenField('Facebook event page')
    
class EditEventForm(EventForm):
    id = HiddenField()
    action = HiddenField(default='event-edit')
    
class ProjectForm(Form):
    title = TextField('Title')
    author = TextField('Author')
    contact = TextField('Contact')
    website = TextField('Website')
    description = TextAreaField('Description')
    icon = TextField('Icon')
    
class AddProjectForm(ProjectForm):
    action = HiddenField(default='project-add')

class TechnologyForm(Form):
    name= TextField('Technology')
    website = TextField('Website')

class SubscriptionsForm(EventForm):
    email = HiddenField('email')
    req_key = HiddenField('req_key')
    sub_meetings = BooleanField('Subscribe to meetings notifications')
    sub_hackathon = BooleanField('Subscribe to hackathon notifications')






