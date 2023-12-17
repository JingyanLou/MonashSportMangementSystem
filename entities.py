import csv

class User:

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email

    def get_username(self):
        '''
        :return: string username
        '''
        return self.username

    def get_password(self):
        '''

        :return: string password
        '''
        return self.password

    def get_email(self):
        '''

        :return: string email
        '''
        return self.email

    def __str__(self) -> str:
        '''

        :return: string username
        '''
        return self.username

class Reason:
    def __init__(self, reason_name) -> None:
        self.reason_name = reason_name

    def get_reason_name(self):
        '''

        :return: string reason name
        '''
        return self.reason_name

    def __str__(self) -> str:
        '''

        :return: string reason name
        '''
        return self.reason_name

class Appointment:
    def __init__(self, branchname, ptname, session, reason) -> None:
        '''
        :param branchname: string branchname
        :param ptname: string ptname
        :param session:
        :param reason:
        '''
        self.branchname = branchname
        self.ptname = ptname
        self.session = session
        self.reason = reason

    def get_branchname(self):
        '''

        :return: string branchname
        '''
        return self.branchname

    def get_ptname(self):
        '''

        :return: string pt name
        '''
        return self.ptname

    def get_session(self):
        '''

        :return: ?
        '''
        print("haaah",self.session)
        return self.session

    def get_reason(self):
        '''

        :return:
        '''
        return self.reason

    def __str__(self) -> str:
        return '{} | {}\n@{} | {}'.format(self.session.time_slot, self.ptname, self.branchname, self.reason)

class Report:
    def __init__(self) -> None:
        pass

class Session:
    def __init__(self, time_slot) -> None:
        self.time_slot = time_slot

    def get_time_slot(self):
        return self.time_slot

    def __eq__(self, __value) -> bool:
        return self.time_slot == __value.time_slot

    def __str__(self) -> str:
        return '{}'.format(self.time_slot)

class Branch:
    def __init__(self, branch_name, postcode, location='xx', contact='yy', opening_hours='zz') -> None:
        self.branch_name = branch_name
        self.postcode = postcode
        self.location = location
        self.contact = contact
        self.opening_hours = opening_hours

    def get_branch_name(self):
        return self.branch_name

    def get_postcode(self):
        return self.postcode

    def get_location(self):
        return self.location

    def get_contact(self):
        return self.contact

    def get_opening_hours(self):
        return self.opening_hours

    def __str__(self) -> str:
        return self.branch_name


class Member(User):
    def __init__(self, username, password, email) -> None:
        super().__init__(username, password, email)

        #list of pt objects
        self.favs = []
        #list of appoinment objects
        self.apps = []

        # load member detail info
        with open('data/member.csv', 'r') as file:
            reader = csv.DictReader(file)
            # username,firstname,lastname,gender,address,postcode,suburb,phone
            for row in reader:
                if row['username'] == self.username:
                    self.firstname = row['firstname']
                    self.lastname = row['lastname']
                    self.gender = row['gender']
                    self.address = row['address']
                    self.postcode = row['postcode']
                    self.suburb = row['suburb']
                    self.phone = row['phone']
                    break
        # load favs
        with open('data/fav.csv', 'r') as file:
            reader = csv.DictReader(file)
            # username,ptname,branchname
            for row in reader:
                if row['username'] == self.username:
                    self.favs.append(PT(row['ptname'], row['branchname']))

        # load apps
        with open('data/app.csv', 'r') as file:
            reader = csv.DictReader(file)
            # username,branchname,ptname,time_slot,reasonname
            for row in reader:
                if row['username'] == self.username:
                    self.apps.append(Appointment(row['branchname'], row['ptname'], Session(
                        row['time_slot']), row['reasonname']))

    def get_firstname(self):
        '''

        :return: str memeber firstname
        '''
        return self.firstname

    def get_favourites(self):
        return self.favs

    def add_favourite(self, pt):

        duplicate_found = False
        #one pt can only work at one branch!
        # no duplicated pt are allowed!
        for p in self.favs:
            if p.get_name() == pt.get_name():
                duplicate_found = True
                break

        if not duplicate_found:
            self.favs.append(pt)

    def delete_fav(self, selected_pt):
        #selected pt: pt object
        new_favs = []
        #for each pt in the fav , if f has the same name and has the same branch ! -> remove
        #else append to the list as new favs
        for f in self.favs:
            if (f.get_name() != selected_pt.get_name() and
                    f.branch.get_branch_name() != selected_pt.branch.get_branch_name()):
                new_favs.append(f)

        self.favs = new_favs

    def get_appointments(self):
        return self.apps

    def add_appointment(self, pt, session, reason):
        self.apps.append(Appointment(
            pt.get_branch().get_branch_name(), pt.get_name(), session, reason))

    def calcel_app(self, selected_app):
        new_apps = []
        for a in self.apps:
            # for each appoinmen
            if (a.get_branchname() != selected_app.get_branchname() or
                    a.get_ptname() != selected_app.get_ptname() or
                    a.get_session() != selected_app.get_session()):

                new_apps.append(a)

        self.apps = new_apps

class PT:
    def __init__(self, name, branchname) -> None:
        self.name = name
        self.sessions = []

        # load the branch info
        with open('data/branch.csv', 'r') as file:
            breader = csv.DictReader(file)
            for brow in breader:
                if brow['branchname'] == branchname:
                    self.branch = Branch(
                        brow['branchname'], brow['postcode'], brow['location'], brow['contact'], brow['opening_hours'])
                    break

        # load the available sessions
        with open('data/session.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ptname'] != self.name:
                    continue
                # ptname,time_slot,sport
                self.sessions.append(Session(row['time_slot']))

    def get_name(self):
        return self.name

    def get_branch(self):
        return self.branch

    def __str__(self) -> str:
        return self.name
