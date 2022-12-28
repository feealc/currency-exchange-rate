import smtplib
import email.message
import traceback
from logger.logger import logger


class GmailHandler:
    def __init__(self, email_owner: str, password: str, flag_send: bool):
        self.__email = email_owner
        self.__password = password
        self.__email_to: list[str] = []
        self.__flag_send = flag_send

        self.__msg: email.message.Message = email.message.Message()
        self.__server: smtplib.SMTP = smtplib.SMTP('smtp.gmail.com: 587')
        self.__setup()

    def __setup(self):
        self.__msg.add_header('Content-Type', 'text/html')
        self.__set_from(email_from=self.__email)

        self.__server.starttls()
        self.__server.login(self.__email, self.__password)

    def set_subject(self, subject: str):
        self.__msg['Subject'] = subject

    def __set_from(self, email_from: str):
        self.__msg['From'] = email_from

    def set_to(self, email_to: str = None, same_as_owner=False):
        self.__email_to = []
        if same_as_owner:
            self.__email_to.append(self.__email)
        else:
            if email_to is None:
                logger.critical('Destinatário não informado')
                raise Exception('Email to is none')
            self.__email_to.append(email_to)

    def add_to(self, email_to: str):
        self.__email_to.append(email_to)

    def get_to(self) -> list[str]:
        return self.__email_to

    def set_body(self, email_body: str):
        self.__msg.set_payload(email_body)

    def send(self, debug=False):
        if not self.__flag_send:
            if debug:
                print('send()')
                print(f'subject [{self.__msg["Subject"]}]')
                print(f'from [{self.__msg["From"]}]')
                print(f'to [{self.__msg["To"]}] {self.get_to()}')
                print(f'body [{self.__msg.get_payload()}]')
            try:
                self.__server.sendmail(self.__email, self.get_to(), self.__msg.as_string().encode('utf-8'))
                # self.__server.sendmail('', '', self.__msg.as_string().encode('utf-8'))
                # smtplib.SMTPRecipientsRefused
                logger.info('E-mail enviado com sucesso!')
            except Exception as e:
                logger.critical('Erro ao enviar email')
                logger.exception(e)
        else:
            logger.info('E-mail não será enviado')
