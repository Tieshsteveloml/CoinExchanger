from django.shortcuts import render
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template
import smtplib
from email.utils import formataddr
from django.http import HttpResponse

# Create your views here.

email_address = "info@btcmovi.com"
email_password = "cufadppmpjcarynw"
# email_address = "Wellendorff23@gmail.com"
# email_password = "Met@$ilver"
smtp_server = "smtp.gmail.com"
smtp_port = "587"

site_name = "Btcmovi.com"
team_name = "Btcmovi.com support team"
company_name = "Btcmovi, Ltd"
site_url = "http://127.0.0.1:9000"


def check_key(key, dict_obj):
    if key not in dict_obj:
        return False
    return True


def get_menu_data():
    data = [
        {'id': 0,
         'url': '/',
         'name': 'start'},
        {'id': 1,
         'url': '/about_us',
         'name': 'about'},
        {'id': 2,
         'url': '/testimonials',
         'name': 'epistolia'}
    ]
    return data


def index(request):
    menu_data = get_menu_data()
    data = {
        "title": "BTCmovi.com - Bitcoin move easy",
        "activated_menu": 0,
        "activated_url": menu_data[0]['url'],
        "menu_data": menu_data,
    }
    template_name = 'dashboard/index.html'
    return render(request, template_name, data)


def about_us(request):
    menu_data = get_menu_data()
    data = {
        "title": "About us - Bitcoin move easy",
        "activated_menu": 1,
        "activated_url": menu_data[1]['url'],
        "menu_data": menu_data,
    }
    template_name = 'dashboard/about_us.html'
    return render(request, template_name, data)


def services(request):
    menu_data = get_menu_data()
    data = {
        "title": "Services - Bitcoin move easy",
        "activated_menu": 2,
        "activated_url": menu_data[2]['url'],
        "menu_data": menu_data,
    }
    template_name = 'dashboard/services.html'
    return render(request, template_name, data)


def contact(request):
    menu_data = get_menu_data()
    data = {
        "title": "Contacts - Bitcoin move easy",
        "activated_menu": 3,
        "activated_url": menu_data[3]['url'],
        "menu_data": menu_data,
    }
    template_name = 'dashboard/contact.html'
    return render(request, template_name, data)


def testimonials(request):
    menu_data = get_menu_data()
    data = {
        "title": "Testimonials - Bitcoin move easy",
        "activated_menu": 2,
        "activated_url": menu_data[2]['url'],
        "menu_data": menu_data,
    }
    template_name = 'dashboard/testimonials.html'
    return render(request, template_name, data)


def support(request):
    menu_data = get_menu_data()
    data = {
        "title": "Support",
        "activated_menu": 3,
        "activated_url": '',
        "menu_data": menu_data,
    }
    template_name = 'dashboard/support.html'
    return render(request, template_name, data)


def render_email(context, template_path):
    template = get_template(template_path)
    html = template.render(context)
    return html


def submit_support(request):
    try:
        params = request.POST
        subject = params['subject']
        message = params['description']
        if params['deposit_address'] != '':
            message += ";Address: " + params['deposit_address']
        res = send_email_to_user(email_address, subject, message, 'support', params['user_email'], params['username'])
        return HttpResponse(res)
    except Exception as e:
        return HttpResponse(str(e))


def send_mail(to_email, subject, message, from_email="", from_name=""):
    try:
        msg = MIMEMultipart()
        msg['subject'] = subject
        msg['from'] = formataddr(("Btcmovi support team", email_address))
        msg.add_header('reply-to', formataddr((from_name, from_email)))
        msg['to'] = formataddr(("Btcmovi support team", to_email))
        msg.attach(message)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)  # username & password
        server.sendmail(msg['from'], [msg['to']], msg.as_string())
        server.quit()
        print('Successfully sent the mail.')
        return 'success'
    except Exception as e:
        return str(e)
'''
def send_mail(to_email, subject, message, from_email=""):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        # msg['From'] = email_address
        msg['From'] = email_address
        msg['Reply-To'] = formataddr(("test", from_email))
        msg['To'] = ', '.join(to_email)
        msg['Date'] = email.utils.formatdate(timeval=None, localtime=False, usegmt=False)
        msg.set_content(message)
        # print(msg)
        server = smtplib.SMTP(smtp_server, smtp_port)
        # server.set_debuglevel(1)  # set debug level
        server.starttls()
        server.login(email_address, email_password)  # username & password
        server.send_message(msg, from_email)
        server.quit()
        print('Successfully sent the mail.')
        return 'success'
    except Exception as e:
        return str(e)
'''


def send_email_to_user(to_emails, subject, message, username='Admin', from_email="", from_name=""):
    try:
        context = {}
        context['site_name'] = site_name
        context["team_name"] = team_name
        context["company_name"] = company_name
        context['username'] = username
        context["site_url"] = site_url
        context['message'] = message.split(';')
        html = render_email(context, "dashboard/email_promo.html")
        part1 = MIMEText(html, 'html')
        res = send_mail(to_emails, subject=subject, message=part1, from_email=from_email, from_name=from_name)
        return res
    except Exception as e:
        return str(e)
