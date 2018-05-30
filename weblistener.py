from urllib.parse import urljoin
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

import requests
import os
import logging
import smtplib


class WebListen:
    def __init__(self):
        self.baseUrl = 'http://www.pgzx.edu.cn/'
        self.msgIndexUrl = urljoin(self.baseUrl, 'modules/peixunxinxi.jsp')
        self.msgList = []
        self.signal = True
        self.from_addr = 'your from_email_addr'
        self.from_pwd = 'your from_email_addr_password'
        self.smtp_server = 'smtp.163.com'
        self.to_addr = 'your to_email_addr'
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    def getPage(self):
        pageText = requests.get(self.msgIndexUrl).text
        soup = BeautifulSoup(pageText, 'lxml')
        msg_detail = soup.select('.left > a')
        for m in msg_detail:
            msg_title = m.get_text()
            msg_link = urljoin(self.baseUrl, 'modules/' + m.get('href'))
            msg = {'msg_title': msg_title, 'msg_link': msg_link}
            self.msgList.append(msg)

    def writeFile(self):
        file = open(r'/home/weblistener/msg_detail.txt', 'w')
        file.write(str(self.msgList))
        file.close()

    def initMsgFile(self):
        if os.path.exists(r'/home/weblistener/msg_detail.txt'):
            pass
        else:
            self.getPage()
            self.writeFile()

    def diffMsg(self):
        file_open = open(r'/home/weblistener/msg_detail.txt', 'r')
        file_open_content = file_open.read()
        msg_detail_old = eval(file_open_content)
        self.getPage()
        if msg_detail_old[0]['msg_title'] != self.msgList[0]['msg_title']:
            self.signal = False
            # 上一次获取信息跟本次获取信息不一致，将最新信息重新写入文件
            self.writeFile()
        else:
            pass

    def doAction(self):
        if self.signal is False:
            # 发送邮件
            self.emailAction()
            logging.info("培训信息有更新内容！")
        else:
            logging.info('培训信息暂无更新。')
            pass

    def emailAction(self):
        to_msg = MIMEText('<html><body><h1>网页更新提示</h1>' +
                          '<h3>教育部高等教育教学评估中心</h3>' +
                          '<h3>评估培训》培训信息</h3>' +
                          '<p>最新信息： <a href="' + self.msgList[0]['msg_link'] + '">' + self.msgList[0][
                              'msg_title'] + '</a>...</p>' +
                          '<p>（306电脑已自动将网页打开，请及时查看。）</p>' +
                          '</body></html>', 'html', 'utf-8')
        to_msg['Subject'] = Header('网页监测提醒', 'utf-8')
        to_msg['From'] = self.from_addr
        to_msg['To'] = self.to_addr

        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.from_pwd)
        server.sendmail(self.from_addr, [self.to_addr], str(to_msg))
        server.quit()

    def test(self):
        self.getPage()
        logging.info('正在发送邮件...')
        # to_msg = MIMEText('<html><body><h1>网页更新提示</h1>' +
        #          '<h3>教育部高等教育教学评估中心</h3>' +
        #          '评估培训》培训信息</h3>' +
        #          '<p>最新信息： <a href="' + self.msgList[0]['msg_link'] + '">' + self.msgList[0]['msg_title'] + '</a>...</p>' +
        #          '</body></html>', 'html', 'utf-8')
        # to_msg['Subject'] = Header('网页监测提醒', 'utf-8')
        # to_msg['From'] = self.from_addr
        # to_msg['To'] = self.to_addr
        # self.emailAction(to_msg)
        logging.info('发送邮件成功！')


if __name__ == '__main__':
    wl = WebListen()
    wl.initMsgFile()
    wl.diffMsg()
    wl.doAction()
    # wl.test()
