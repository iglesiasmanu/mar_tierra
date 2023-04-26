import os
import secrets
import subprocess
from datetime import datetime

from PIL import Image
from flask import request
from flask_login import current_user
from mar_tierra import app_root
from mar_tierra.views.homes.forms import NewHomeFom
from mar_tierra.views.functions import send_mail_html_cc


# SEND AUTOMATION EMAIL - Standard - Functions
def send_confimation_email():
    form = NewHomeFom(request.form)
    appointment_date = form.appointment_date.data
    appointment_hour = form.appointment_hour.data
    Description = "New Devices"
    user = str(current_user)

    body_1 = open('mar_tierra/Notifications/confirmation_email.html').read()
    body_3 = open('mar_tierra/Notifications/Signature.html').read()
    body_1 = body_1.format(user, appointment_date, appointment_hour, Description, body_3)

    body = [body_1]

    send_mail_html_cc(msg_from='NonReply@ibm.com',
                      to=user,
                      cc="ferjg@ibm.com",
                      subject='Devices Operations home Confirmation',
                      text=body,
                      picture='mar_tierra/views/imageDevices.png',
                      files=[],
                      debug=False)

def return_device_send_confimation_email():
    form = AppointmentForm(request.form)
    appointment_date = form.appointment_date.data
    appointment_hour = form.appointment_hour.data
    Description = "Return Device"
    user = str(current_user)

    body_1 = open('mar_tierra/Notifications/return_confirmation_email.html').read()
    body_3 = open('mar_tierra/Notifications/Signature.html').read()
    body_1 = body_1.format(user, appointment_date, appointment_hour, Description, body_3)

    body = [body_1]

    send_mail_html_cc(msg_from='NonReply@ibm.com',
                      to=user,
                      cc="ferjg@ibm.com",
                      subject='Devices Operations home Confirmation',
                      text=body,
                      picture='mar_tierra/views/imageDevices.png',
                      files=[],
                      debug=False)
