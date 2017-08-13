class User:

    def __init__(user):
        self.id   = user.id
        self.date = '' #TODO
        self.code = ''

class Verifier:

    users = []

    @staticmethod
    def add(user):
        ''' Add a user to the list of users to verify '''
        users.append(User(user))

    @staticmethod
    def send_code(user, mail):
        ''' Send a mail with a verification code '''
        i = len(self.users) - 1
        while i > 0 and user.id != users[i].id:
            i -= 1
        users[i].code = Verifier.generate_code()

    @staticmethod
    def generate_code():
        return 'SUPER CODE' #TODO

    @staticmethod
    def verif_mail(txt):
        if txt[-11:] != '@epitech.eu':
            return False
        # TODO : mail username (check there are no @...)
        return True
