# test runner顾名思义就是用来执行测试用例的，并且可以生成相应的测试报告。测试报告有两种展示形式，一种是text文本，一种是html格式。
#
# ​ html格式的就是HTMLTestRunner了，HTMLTestRunner 是 Python 标准库的 unittest 框架的一个扩展，它可以生成一个直观清晰的 HTML 测试报告。使用的前提就是要下载 HTMLTestRunner.py，下载完后放在python的安装目录下的scripts目录下即可。
#
# ​ text文本相对于html来说过于简陋，与控制台输出的没有什么区别，也几乎没有人使用，这里不作演示，使用方法是一样的。我们结合前面的测试套件来演示一下如何生成html格式的测试报告：
# run_test.py，与test_register.py、register.py同一目录下
import unittest, time
import BZSCS
from HTMLTestRunner import HTMLTestRunner
import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 创建测试套件
suite = unittest.TestSuite()

# 通过模块加载用例
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromModule(BZSCS))

# 创建测试程序启动器
runner = HTMLTestRunner(stream=open("report.html", "wb"),
                        description="接口自动化测试报告",
                        title="接口自动化测试报告")

# 使用启动器执行用例
runner.run(suite)

time.sleep(5)



# 发送邮件
class SendEmail():
    def __init__(self, username, passwd, recv, title, content,
                 file=None, ssl=False,
                 email_host='smtphz.qiye.163.com', port=25, ssl_port=465):
        self.username = username  # 用户名
        self.passwd = passwd  # 密码
        self.recv = recv  # 收件人，多个要传list ['a@qq.com','b@qq.com]
        self.title = title  # 邮件标题
        self.content = content  # 邮件正文
        self.file = file  # 附件路径，如果不在当前目录下，要写绝对路径
        self.email_host = email_host  # smtp服务器地址
        self.port = port  # 普通端口
        self.ssl = ssl  # 是否安全链接
        self.ssl_port = ssl_port  # 安全链接端口

    def send_email(self):
        msg = MIMEMultipart()
        # 发送内容的对象
        if self.file:  # 处理附件的
            file_name = os.path.split(self.file)[-1]  # 只取文件名，不取路径
            try:
                f = open(self.file, 'rb').read()
            except Exception as e:
                raise Exception('附件打不开！！！！')
            else:
                att = MIMEText(f, "base64", "utf-8")
                att["Content-Type"] = 'application/octet-stream'
                # base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 这里是处理文件名为中文名的，必须这么写
                att["Content-Disposition"] = 'attachment; filename="%s"' % (new_file_name)
                msg.attach(att)
        msg.attach(MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = ','.join(self.recv)  # 接收者账号列表
        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.email_host, port=self.port)
        # 发送邮件服务器的对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, msg.as_string())
            pass
        except Exception as e:
            print('出错了。。', e)
        else:
            print('发送成功！')
        self.smtp.quit()


if __name__ == '__main__':
    m = SendEmail(
        username='chenglong.li@sinosun.com.cn',
        passwd='a19881027!',
        recv=['chenglong.li@sinosun.com.cn'],
        title='接口自动化测试报告',
        content='HI，伴正事接口自动化冒烟测试已完成，执行结果见附件',
        file=r'C:\Users\23411\PycharmProjects\bzs\report.html',
        ssl=True,
    )
    m.send_email()