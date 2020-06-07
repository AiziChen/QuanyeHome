import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(subject, content, to_addr):
    from_addr = "dav.chen@qq.com"

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("Quanyec", 'utf-8')
    message['To'] = Header(to_addr, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP("smtp.qq.com")
        server.login("1098679804", "")
        server.sendmail(from_addr, to_addr, message.as_string())
        server.quit()
        return True
    except smtplib.SMTPException:
        return False

# 测试
# send_email("新绿色药业自动签到提示", "签到成功", "xyz@163.com")
