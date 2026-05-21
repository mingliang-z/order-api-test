import smtplib
import os
from email.mime.text import MIMEText

sender = os.environ["MAIL_USER"]
password = os.environ["MAIL_PASS"]
receiver = os.environ["MAIL_TO"]

repo = os.environ["GITHUB_REPOSITORY"]
branch = os.environ["GITHUB_REF_NAME"]
status = os.environ["JOB_STATUS"]

msg = MIMEText(
    f"仓库: {repo}\n分支: {branch}\n运行状态: {status}",
    "plain", "utf-8"
)
msg["Subject"] = f"测试报告 - {repo}"
msg["From"] = sender
msg["To"] = receiver

server = smtplib.SMTP_SSL("smtp.qq.com", 465)
server.login(sender, password)
server.sendmail(sender, [receiver], msg.as_string())
server.quit()
print("邮件发送成功")