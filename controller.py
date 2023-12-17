from entities import *
import csv


class MSMS:
    '''
    Controller Class (Controller)
    '''

    def __init__(self) -> None:

        # login user
        self.login_user = None

        # list of objects
        self.users = []
        self.reasons = []
        self.branches = []
        self.pts = []

        # load all data into the list
        self.load_data()

    def load_data(self):
        '''
        load all the data from the csv into the application
        :return: None
        '''
        with open('data/user.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # print(row)
                self.users.append(
                    User(row['username'], row['password'], row['email']))

        with open('data/branch.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.branches.append(Branch(
                    row['branchname'], row['postcode'], row['location'], row['contact'], row['opening_hours']))

        with open('data/pt.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # ptname,branchname
                self.pts.append(PT(row['ptname'], row['branchname']))

        with open('data/reason.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.reasons.append(Reason(row['reasonname']))

    # validate user's provided username and password
    def login(self, username, pwd) -> bool:
        '''
        :param username: string
        :param pwd: string
        :return: bool
        '''
        # if provided details matches with the database
        for u in self.users:
            if u.get_username() == username and u.get_password() == pwd:  # validate
                # load a member
                self.login_user = Member(u.get_username(),
                                         u.get_password(), u.get_email())
                return True

        return False

    def get_login_username(self):
        '''
        :return: str The login user name
        '''
        return self.login_user.get_username()

    def get_login_firstname(self): #used for display the name at the homescreen
        '''

        :return: str memeber firstname
        '''
        return self.login_user.get_firstname()

    def get_reasons(self) -> list[Reason]:
        '''
        :return: list of reasons objects
        '''
        return self.reasons

    def get_all_branches(self) -> list[Branch]:
        '''
        :return: list of branches objects
        '''
        return self.branches

    def get_pts_by_branch(self, branch) -> list[PT]:
        '''
        :param branch: branch object
        :return: list of pt that work at that branch
        '''

        res = []


        for p in self.pts: #p is  pt object


            if p.get_branch().get_branch_name() == branch.get_branch_name():
                res.append(p)
        return res

    def create_appointment(self, pt, session, reason):
        '''
        :param pt: object
        :param session: object
        :param reason: object
        :return: None
        '''
        self.login_user.add_appointment(pt, session, reason.get_reason_name())

    def add_favourite(self, pt):
        '''
        :param pt: object
        :return: None
        '''
        self.login_user.add_favourite(pt)

    def cancel_app(self, selected_app):
        '''
        :param selected_app: object
        :return: None
        '''
        self.login_user.calcel_app(selected_app)

    def get_apps_by_member(self):
        '''
        :return: None
        load all the appointment of the given user
        '''
        return self.login_user.get_appointments()

    def get_member_favourites(self):
        '''
        :return: None
        load all the favrouite of that member
        '''
        return self.login_user.get_favourites()

    def delete_fav(self, selected_pt):
        '''
        :param selected_pt: object
        :return: None
        Delete the selected_pt from the fav list of the member
        '''
        self.login_user.delete_fav(selected_pt)

    def get_near_branches(self, postcode):
        '''
        :param postcode: 4 digit integer
        :return: list of branch sorted on its similarities.
        '''
        branch_similarity = []

        for b in self.branches:
            pc = b.get_postcode()
            sim = abs(int(postcode) - int(pc))
            branch_similarity.append((b, sim))  # list of tuple

        # sort on the sim
        res = sorted(branch_similarity, key=lambda i: i[1])

        return [i[0] for i in res]  # list of branch sorted on the similarities

    def save(self):
        '''
        :return: None

        Save the appointment and the favourite of the user into the csv files
        Write to "database"
        note: save is only called when exit the program

        '''
        # save fav
        self.save_fav()
        # save appointment
        self.save_app()

    def save_fav(self):
        """
        :return:None

        username,ptname,branchname
        tom,trainer A,Boxhill branch
        henry,trainer B,Doncaster branch
        henry,trainer A,Boxhill branch

        """
        lines = []
        with open('data/fav.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # username,ptname,branchname
                if row[0] == self.login_user.get_username():
                    continue
                lines.append(','.join(row) + '\n')

        for f in self.login_user.get_favourites():
            l = ','.join([self.login_user.get_username(), f.get_name(),
                          f.get_branch().get_branch_name()]) + '\n'
            lines.append(l)

        with open('data/fav.csv', 'w') as file:
            file.writelines(lines)

    def save_app(self):
        '''
        :return: None

        username,branchname,ptname,time_slot,reasonname
        tom,Boxhill branch,trainer A,18/10/2023 10:00-10:30,Bulking
        henry,Doncaster branch,trainer B,17/10/2023 09:00-09:30,Weight loss

        '''
        lines = []
        with open('data/app.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # username,branchname,ptname,time_slot,sportname
                if row[0] == self.login_user.get_username():
                    continue
                lines.append(','.join(row) + '\n')

        for a in self.login_user.get_appointments():
            l = ','.join([self.login_user.get_username(), a.get_branchname(),
                          a.get_ptname(), a.get_session().get_time_slot(), a.get_reason()]) + '\n'
            lines.append(l)

        # print(lines)
        with open('data/app.csv', 'w') as file:
            file.writelines(lines)
