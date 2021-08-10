def emailpush(addr, text, attch_a, attch_b):  # 邮件发送模块
    # smtplib 用于邮件的发信动作
    import smtplib
    from email.mime.text import MIMEText
    # email 用于构建邮件内容
    from email.header import Header
    # 用于构建附件
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    # 用于构建邮件头
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '1005760706@qq.com'
    password = 'zhmmjspzbtlrbfif'

    # 收信方邮箱，允许多个收件人
    to_addr = addr

    # 发信服务器
    smtp_server = 'smtp.qq.com'

    for to in to_addr:
        # 邮件头信息
        msg = MIMEMultipart()
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to)
        msg['Subject'] = Header('看股提醒')
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        message = MIMEText(text, 'plain', 'utf-8')
        msg.attach(message)

        # 构造附件（附件为JPG格式的图片）
        with open('daily_k.jpg', 'wb') as code:
            code.write(attch_a.content)
        with open('min_k.jpg', 'wb') as code:
            code.write(attch_b.content)

        attch_1 = 'daily_k.jpg'
        attch1 = MIMEApplication(open(attch_1, 'rb').read())
        attch1.add_header('Content-Disposition', 'attachment', filename=attch_1)
        msg.attach(attch1)

        attch_2 = 'min_k.jpg'
        attch2 = MIMEApplication(open(attch_2, 'rb').read())
        attch2.add_header('Content-Disposition', 'attachment', filename=attch_2)
        msg.attach(attch2)
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to, msg.as_string())
        # 关闭服务器
        server.quit()


if __name__ == '__main__':
    from shares import daily_k_chart, min_k_chart
    emailpush(addr='1005760706@qq.com', text='附件发送测试', attch_a=daily_k_chart, attch_b=min_k_chart)
