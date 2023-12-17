from enum import Enum, auto
from entities import *
from controller import *


# -------Boundary
class State(Enum):
    """
    User interface state enumeration
    """
    LOGIN = auto()
    HOME = auto()
    BOOK = auto()
    APPOINTMENT = auto()
    FAVOURITE = auto()
    EXIT = auto()

    BOOK_SELECTBRANCH = auto()
    BOOK_NEARESTBRNCH = auto()
    BOOK_NEARESTBRNCH_SELECT = auto()

    BOOK_OVERVIEW = auto()
    BOOK_BRANCH_DETAIL = auto()
    BOOK_SELECT_PT = auto()
    BOOK_SELECT_SESSION = auto()
    BOOK_SELECT_REASON = auto()
    BOOK_CONFIRM = auto()
    BOOK_SUCCESS = auto()

    APP_VIEW = auto()
    APP_CANCEL = auto()
    APP_CANCEL_SUCCESS = auto()

    FAV_BOOK_SELECT_PT = auto()
    FAV_BOOK_SELECT_SESSION = auto()
    FAV_BOOK_CONFIRM = auto()
    FAV_BOOK_SUCCESS = auto()

    FAV_ADD_SELECTBRANCH = auto()
    FAV_ADD_SELECT_PT = auto()
    FAV_ADD_CONFIRM = auto()
    FAV_ADD_SUCCESS = auto()

    FAV_DELETE_SELECT = auto()
    FAV_DELETE_SUCCESS = auto()


class Userinterface:
    """
    Boundary class (View)
    """

    def __init__(self) -> None:
        # setup the controller
        self.manager = MSMS()

        self.current_state = State.LOGIN  # init state = login
        self.states = []  # list of state
        self.postcode = None  # Recorded postcode = None

        # variables to store user selections
        self.selected_branch = None
        self.selected_pt = None
        self.selected_session = None
        self.selected_reason = None
        self.selected_app = None

    def fav_delete_select(self):
        '''
        :return:
        '''

        favs = self.manager.get_member_favourites()  # favs = list of pt
        self.print_fav_delete_select_pt_screen(favs)  # print pt and their  branch
        # opt can only be within the range of len(favs)
        opt = self.get_user_option(
            len(favs), allow_back=True, allow_home=True)

        if opt == '0':
            self.current_state = self.states.pop()  # go back
        elif opt == 'home':
            self.current_state = State.HOME  # go home

        else:  # if user selects a pt

            self.selected_pt = favs[int(opt) - 1]  # Index off by one
            self.manager.delete_fav(self.selected_pt)  # delete the fav that matches with the selected_pt
            self.states.append(self.current_state)  # move to next state
            self.current_state = State.FAV_DELETE_SUCCESS  # update the state

    def fav_delete_success(self):
        '''
        :return: None
        '''
        self.print_fav_delete_success_screen()  # print the view

        # cant go back but can go home , 0 options for the user
        opt = self.get_user_option(
            0, allow_back=False, allow_home=True)

        if opt == 'home':
            self.current_state = State.HOME  # go home

    def fav_add_select_branch(self):
        '''
        :return: None
        '''

        branches = self.manager.get_all_branches()  # get all branches
        self.print_select_branch_screen(branches)  # print all branches

        # option within the range of branches len
        opt_branch = self.get_user_option(
            len(branches), allow_back=True, allow_home=True)

        if opt_branch == '0':  # go back
            self.current_state = self.states.pop()
        elif opt_branch == 'home':  # go home
            self.current_state = State.HOME
        else:
            # user select an option
            self.selected_branch = branches[int(opt_branch) - 1]  # index off by 1
            self.states.append(self.current_state)
            self.current_state = State.FAV_ADD_SELECT_PT  # select pt from the selected branch

    def fav_add_select_pt(self):
        '''
        :return: None
        '''
        pts = self.manager.get_pts_by_branch(self.selected_branch)  # see the pt works at the selected branch
        self.print_fav_add_select_pt_screen(pts)

        # ranges of options based on len of the pts list
        opt_pt = self.get_user_option(
            len(pts), allow_back=True, allow_home=True)

        if opt_pt == '0':
            self.current_state = self.states.pop()
        elif opt_pt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_pt = pts[int(opt_pt) - 1]  # index off by one
            self.states.append(self.current_state)
            self.current_state = State.FAV_ADD_CONFIRM

    def fav_add_confirm(self):
        '''
        :return: None
        '''
        self.print_fav_add_confirm_screen()

        opt = self.get_user_option(
            2, allow_back=True, allow_home=True)

        '''
        Do you want to save the above Branch & PT as
        one of your favourite?

        1. Yes
        2. No

        O or 2 for go back, 1 for confirm 

        '''

        if opt == '0' or opt == '2':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.states.append(self.current_state)
            self.manager.add_favourite(self.selected_pt)  # favrouite = list(pt)
            self.current_state = State.FAV_ADD_SUCCESS

    def fav_add_success(self):
        '''
        :return: None
        '''
        self.print_fav_add_success_screen()

        opt = self.get_user_option(
            0, allow_back=False, allow_home=True)

        # go home
        if opt == 'home':
            self.current_state = State.HOME

    def fav_book_select_pt(self):
        '''

        :return: None
        '''

        favs = self.manager.get_member_favourites()

        self.print_fav_select_pt_screen(favs)  # list of pt

        # ranges within the length of the fav list
        opt = self.get_user_option(
            len(favs), allow_back=True, allow_home=True)
        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_pt = favs[int(opt) - 1]
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SELECT_SESSION

    def app_view(self):
        '''
        :return: None
        '''

        apps = self.manager.get_apps_by_member()  # get all the appoinment

        self.print_app_view_screen(apps)  # print the screen

        opt = self.get_user_option(
            0, allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME

    def app_cancel(self):
        '''

        :return: None
        '''
        # get all the appoinments by the user
        apps = self.manager.get_apps_by_member()

        self.print_app_cancel_screen(apps)

        # options ranges within the len of the appoinment list
        opt = self.get_user_option(
            len(apps), allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_app = apps[int(opt) - 1]  # index off by one
            self.manager.cancel_app(self.selected_app)  # cancel the appointment
            self.states.append(self.current_state)
            self.current_state = State.APP_CANCEL_SUCCESS

    def app_cancel_success(self):
        '''

        :return: None
        '''

        self.print_app_cancel_success_screen()

        opt = self.get_user_option(
            0, allow_back=False, allow_home=True)
        if opt == 'home':
            self.current_state = State.HOME

    def book_overview(self):
        '''

        :return: None
        '''

        self.print_book_overview_screen()

        opt = self.get_user_option(
            2, allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        elif opt == '1':  # branch details
            self.states.append(self.current_state)
            self.current_state = State.BOOK_BRANCH_DETAIL
        elif opt == '2':  # select a pt
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SELECT_PT

    def book_branch_detail(self):
        '''

        :return: None
        '''
        # print the branch details
        self.print_branch_detail_screen(self.selected_branch)

        opt = self.get_user_option(
            0, allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME

    def book_select_pt(self):
        '''

        :return: None
        '''

        # get all the pt who works at this branch


        pts = self.manager.get_pts_by_branch(self.selected_branch)
        # print out the pts
        self.print_book_select_pt_screen(pts)

        # provide options based on the length of the pts
        opt_pt = self.get_user_option(
            len(pts), allow_back=True, allow_home=True)

        if opt_pt == '0':
            self.current_state = self.states.pop()
        elif opt_pt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_pt = pts[int(opt_pt) - 1]
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SELECT_SESSION

    def book_select_session(self):
        '''

        :return: None
        '''

        # list of sessions by that pt
        sessions = self.selected_pt.sessions

        # print the sessions
        self.print_book_select_session_screen(sessions)

        # options ranges from the length of the list of sessions
        opt = self.get_user_option(
            len(sessions), allow_back=True, allow_home=True)
        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_session = sessions[int(opt) - 1]
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SELECT_REASON

    def book_select_reason(self):
        '''

        :return: None
        '''
        reasons = self.manager.get_reasons()  # get all the reasons

        self.print_book_select_reason_screen(reasons)

        # provide options
        opt = self.get_user_option(
            len(reasons), allow_back=True, allow_home=True)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.selected_reason = reasons[int(opt) - 1]  # index off by one
            self.states.append(self.current_state)
            self.current_state = State.BOOK_CONFIRM

    def book_confirm(self):
        '''

        :return: None
        '''

        self.print_book_confirm_screen()

        opt = self.get_user_option(
            1, allow_back=True, allow_home=True)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:  # if opt = 1
            # create  appoinment based on the selected information
            self.manager.create_appointment(self.selected_pt, self.selected_session, self.selected_reason)
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SUCCESS

    def book_success(self):
        '''

        :return: None
        '''

        self.print_book_success_screen()  # successfully booked ! congrats

        opt = self.get_user_option(
            0, allow_back=False, allow_home=True)
        if opt == 'home':
            self.current_state = State.HOME

    def book_select_branch(self):
        '''

        :return: None
        '''
        branches = self.manager.get_all_branches()  # show all the branches

        self.print_select_branch_screen(branches)  # print all the branches

        # show options by branches
        opt_branch = self.get_user_option(
            len(branches), allow_back=True, allow_home=True)

        if opt_branch == '0':
            self.current_state = self.states.pop()
        elif opt_branch == 'home':
            self.current_state = State.HOME
        else:
            self.selected_branch = branches[int(opt_branch) - 1]
            self.states.append(self.current_state)
            self.current_state = State.BOOK_OVERVIEW

    def book_nearest_branch(self):
        '''

        :return: None
        '''

        self.print_provide_postcode_screen()

        while True:  # ask user for input
            opt = input('Please enter your postcode: ').strip()
            if opt:
                break

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        else:
            self.postcode = opt
            self.states.append(self.current_state)
            self.current_state = State.BOOK_NEARESTBRNCH_SELECT

    def book_nearest_branch_select(self):
        '''

        :return: None
        '''

        near_branches = self.manager.get_near_branches(self.postcode)  # get branches by postcode

        self.print_nearest_branch_screen(near_branches)  # show nearest branch sorted by its postcode difference

        opt_branch = self.get_user_option(
            len(near_branches), allow_back=True, allow_home=True)

        if opt_branch == '0':
            self.current_state = self.states.pop()
        elif opt_branch == 'home':
            self.current_state = State.HOME
        else:
            self.selected_branch = near_branches[int(opt_branch) - 1]
            self.current_state = State.BOOK_OVERVIEW

    def book(self) -> None:
        '''

        :return: None
        '''

        # select branch
        self.print_book_branch_option_screen()

        opt_branch = self.get_user_option(
            2, allow_back=True, allow_home=True, allow_multiple=False)

        if opt_branch == '0':
            self.current_state = self.states.pop()
        elif opt_branch == 'home':
            self.current_state = State.HOME
        elif opt_branch == '1':
            self.states.append(self.current_state)
            self.current_state = State.BOOK_SELECTBRANCH
        elif opt_branch == '2':
            self.states.append(self.current_state)
            self.current_state = State.BOOK_NEARESTBRNCH

    def manage_appointment(self) -> None:
        '''

        :return: None
        '''

        self.print_app_screen()  # print the appoinment screen

        opt = self.get_user_option(
            2, allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        elif opt == '1':  # view your appointment
            self.states.append(self.current_state)
            self.current_state = State.APP_VIEW
        elif opt == '2':  # to cancel an appointment
            self.states.append(self.current_state)
            self.current_state = State.APP_CANCEL

    def manage_favourite(self) -> None:
        '''

        :return: None
        '''

        self.print_fav_screen()  # print the fav screen

        opt = self.get_user_option(
            3, allow_back=True, allow_home=True, allow_multiple=False)

        if opt == '0':
            self.current_state = self.states.pop()
        elif opt == 'home':
            self.current_state = State.HOME
        elif opt == '1':  # quick acess and book
            self.states.append(self.current_state)
            self.current_state = State.FAV_BOOK_SELECT_PT
        elif opt == '2':  # add favrouite
            self.states.append(self.current_state)
            self.current_state = State.FAV_ADD_SELECTBRANCH
        elif opt == '3':  # delete a combo
            self.states.append(self.current_state)
            self.current_state = State.FAV_DELETE_SELECT

    def print_login_screen(self) -> None:
        info = '''
*******************************************
                  LOGIN
*******************************************

PT Appointment System.


        '''
        print(info)

    def print_home_screen(self) -> None:
        info = '''
*******************************************
              Homescreen
*******************************************

WELCOME, {}!

Here is your options:
1. Book an appointment
2. Manage appointments
3. Favourite
4. Log out
        '''.format(self.manager.get_login_firstname())
        print(info)

    def print_app_screen(self) -> None:
        info = '''
*******************************************
            Manage appointment
*******************************************

1. View appointments
2. Cancel an appointment

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_fav_delete_select_pt_screen(self, favs) -> None:
        fav_options = '\n'.join([str(i + 1) + '. ' + '{} @{}'.format(str(s), str(s.branch)) for i,
        s in enumerate(favs)])
        info = '''
*******************************************
      Delete favourite branch & PT
*******************************************
Your saved Branch & PT
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(fav_options)
        print(info)

    def print_fav_delete_success_screen(self) -> None:
        info = '''
*******************************************
    Delete favourite branch & PT
*******************************************


You have successfully deleted!


--------------------------------------------
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_fav_add_confirm_screen(self) -> None:
        branch_line = str(self.selected_pt.branch)
        trainer_line = str(self.selected_pt)
        info = '''
*******************************************
          Favourite confirmed
*******************************************
Selected branch: {}
Selected PT: {}

Do you want to save the above Branch & PT as
one of your favourite?

1. Yes
2. No

--------------------------------------------
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, trainer_line)
        print(info)

    def print_fav_add_success_screen(self) -> None:
        branch_line = str(self.selected_pt.branch)
        trainer_line = str(self.selected_pt)
        info = '''
*******************************************
          Favourite confirmed
*******************************************
Selected branch: {}
Selected PT: {}

Selected branch and PT has been added to
your list!


--------------------------------------------
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, trainer_line)
        print(info)

    def print_fav_add_select_pt_screen(self, pts) -> None:
        branch_line = str(self.selected_branch)
        pt_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(pts)])

        info = '''
*******************************************
         Book an appointment
*******************************************
Selected branch: {}

Available personal trainers:
{}

Please select your prefered personal trainer

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, pt_options)
        print(info)

    def print_fav_select_pt_screen(self, favs) -> None:
        fav_options = '\n'.join([str(i + 1) + '. ' + '{} @ {}'.format(str(s), str(s.branch)) for i,
        s in enumerate(favs)])
        info = '''
*******************************************
       Select your favourite
*******************************************
Your saved Branch & PT
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(fav_options)
        print(info)

    def print_fav_screen(self) -> None:
        info = '''
*******************************************
               Favourite
*******************************************

1. Favourite branch & PT Quick book
2. Add favourite branch & PT
3. Delete favourite branch & PT


--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_app_cancel_screen(self, apps) -> None:
        app_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(apps)])
        info = '''
*******************************************
            Cancel appointment
*******************************************
Your appointment details:
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(app_options)
        print(info)

    def print_app_view_screen(self, apps) -> None:
        app_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(apps)])
        info = '''
*******************************************
              View appointment
*******************************************
Your appointment details:
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(app_options)
        print(info)

    def print_app_cancel_success_screen(self) -> None:
        app_line = str(self.selected_app)
        info = '''
*******************************************
           Cancel appointment
*******************************************
Your appointment details:
{}


Cancelled successfully!
--------------------------------------------
Type "home" to return to homepage
--------------------------------------------
        '''.format(app_line)
        print(info)

    def print_branch_detail_screen(self, branch: Branch) -> None:
        info = '''
*******************************************
               Branch detail
*******************************************
Branch Information:

Branch Name: {}
Location: {}
Contact: {}
Opening hours: {}


--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch.get_branch_name(), branch.get_location(), branch.get_contact(), branch.get_opening_hours())
        print(info)

    def print_nearest_branch_screen(self, near_branches) -> None:
        branch_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(near_branches)])
        info = '''
*******************************************
              Select a branch
*******************************************
Your postcode is {}

Nearby Branches(From near to far):
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(self.postcode, branch_options)
        print(info)

    def print_provide_postcode_screen(self) -> None:
        info = '''
*******************************************
        Book an appointment
*******************************************

Please provide your postcode information





--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_book_success_screen(self) -> None:
        info = '''
*******************************************
           Book an appointment
*******************************************
Book Successfully!

Please check your appointment in "Manage
Appointments".


--------------------------------------------
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_book_confirm_screen(self) -> None:
        branch_line = str(self.selected_pt.branch)
        trainer_line = str(self.selected_pt)
        session_line = self.selected_session.time_slot
        reason_line = str(self.selected_reason)

        info = '''
*******************************************
           Book an appointment
*******************************************
Selected branch: {}
Selected personal trainer: {}
Selected session time: {}
Selected reason: {}

Your options:
1. Confirm the appointment

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, trainer_line, session_line, reason_line)
        print(info)

    def print_book_select_reason_screen(self, reasons) -> None:
        reasons_line = '\n'.join(['{}. {}'.format(i + 1, str(r)) for i, r in enumerate(reasons)])
        info = '''
*******************************************
         Book an appointment
*******************************************
What is your reason for seeing the PT?
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(reasons_line)
        print(info)

    def print_book_select_session_screen(self, sessions) -> None:
        branch_line = str(self.selected_pt.get_branch())
        trainer_line = str(self.selected_pt)
        session_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(sessions)])

        info = '''
*******************************************
           Book an appointment
*******************************************
Selected branch: {}
Selected personal trainer: {}

Available sessions:
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, trainer_line, session_options)
        print(info)

    def print_book_select_pt_screen(self, pts) -> None:
        branch_line = str(self.selected_branch)
        pt_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(pts)])

        info = '''
*******************************************
          Book an appointment
*******************************************
Selected branch: {}

Available personal trainers:
{}

Please select your prefered personal trainer

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line, pt_options)
        print(info)

    def print_book_overview_screen(self) -> None:
        branch_line = str(self.selected_branch)
        info = '''
*******************************************
           Book an appointment
*******************************************
Selected branch: {}

Branch options
1. About this branch
2. Available Personal Trainers


--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_line)
        print(info)

    def print_book_branch_option_screen(self) -> None:
        info = '''
*******************************************
             Book an appointment
*******************************************

Branch options
1. Select a branch
2. Find a nearest branch

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''
        print(info)

    def print_select_branch_screen(self, branches: list[Branch]) -> None:
        branch_options = '\n'.join([str(i + 1) + '. ' + str(s) for i,
        s in enumerate(branches)])
        info = '''
*******************************************
              Select a branch
*******************************************

All Branches:
{}

--------------------------------------------
Enter "0" to go back
Type "home" to return to homepage
--------------------------------------------
        '''.format(branch_options)
        print(info)

    def get_user_option(self, option_length, allow_back=False, allow_home=False, allow_multiple=False) -> str:
        '''
        :param option_length: int
        :param allow_back: boolean
        :param allow_home: boolean
        :param allow_multiple: boolean
        :return: a string
        option length is a customized value, it specify a range of valid option number that can be accepted by the system
        '''
        valid_options = []

        if option_length > 0:
            valid_options = [str(i) for i in range(1, option_length + 1)]
        if allow_home:
            valid_options.append('home')
        if allow_back:
            valid_options.append('0')

        while True:
            opt = input('Please enter an option: ').strip()
            if (allow_multiple and all([o in valid_options for o in opt.split('/')])) or (opt in valid_options):
                return opt
            else:
                print('Invalid option. Please enter again.')

    def login(self):
        self.print_login_screen()
        while True:
            username = input('Please input username: ')
            pwd = input('Plese input password: ')
            success = self.manager.login(username, pwd)
            if success:
                self.current_state = State.HOME
                break
            else:
                print('Wrong username or password. Please retry.')

    def home(self):
        '''
        :return: None
        '''

        self.states.clear()  # clear all the states

        self.states.append(self.current_state)  # add the current state

        self.print_home_screen()  # print the home screen

        opt = int(self.get_user_option(4))

        if opt == 1:
            self.current_state = State.BOOK
        elif opt == 2:
            self.current_state = State.APPOINTMENT
        elif opt == 3:
            self.current_state = State.FAVOURITE
        elif opt == 4:
            self.current_state = State.EXIT

    def exit(self):
        '''
        Save and quit the program
        :return: None
        '''
        self.manager.save()

    def run_main(self) -> None:
        """
        The main process of the management system
        """
        while True:
            if self.current_state == State.LOGIN:  # default state when started the program
                self.login()
            elif self.current_state == State.HOME:  # after login
                self.home()

            # Main menu
            elif self.current_state == State.BOOK:  # if option=1, from login page
                self.book()
            elif self.current_state == State.APPOINTMENT:  # if option=2, from login page
                self.manage_appointment()
            elif self.current_state == State.FAVOURITE:  # if option=3, from login page
                self.manage_favourite()
            elif self.current_state == State.EXIT:  # if option=4, from login page. save data and exit
                self.exit()
                break

            # ---- APPOINTMENT MAIN SCREEN
            elif self.current_state == State.APP_VIEW:  # view my appointment
                self.app_view()
            elif self.current_state == State.APP_CANCEL:  # cancel my appoinment
                self.app_cancel()
            elif self.current_state == State.APP_CANCEL_SUCCESS:  # cancel success
                self.app_cancel_success()

            # ---- FAVOURITE SCREEN
            elif self.current_state == State.FAV_BOOK_SELECT_PT:  # quickaccess, next STATE will be BOOK_SELECTED_SESSION
                self.fav_book_select_pt()

            # ----- ADDING FAVOURITE SCREEN
            elif self.current_state == State.FAV_ADD_SELECTBRANCH:  # opt=2
                self.fav_add_select_branch()
            elif self.current_state == State.FAV_ADD_SELECT_PT:  # after select a branch, select the pt from that branch
                self.fav_add_select_pt()
            elif self.current_state == State.FAV_ADD_CONFIRM:  # branch & pt selected
                self.fav_add_confirm()
            elif self.current_state == State.FAV_ADD_SUCCESS:  # done
                self.fav_add_success()

            # ------ FAV DELETE
            elif self.current_state == State.FAV_DELETE_SELECT:
                self.fav_delete_select()
            elif self.current_state == State.FAV_DELETE_SUCCESS:
                self.fav_delete_success()

            # ---- BOOK SCREEN
            elif self.current_state == State.BOOK_SELECTBRANCH:  # SELECT A BRANCH
                self.book_select_branch()
            elif self.current_state == State.BOOK_NEARESTBRNCH:  # ASK FOR YOUR POSTCODE
                self.book_nearest_branch()
            elif self.current_state == State.BOOK_NEARESTBRNCH_SELECT:  # SELECT FROM  NEAREST BRANCH LIST
                self.book_nearest_branch_select()
            elif self.current_state == State.BOOK_OVERVIEW:  # selected branch screen, you can select a pt or view branch detail
                self.book_overview()
            elif self.current_state == State.BOOK_BRANCH_DETAIL:  # branch information
                self.book_branch_detail()
            elif self.current_state == State.BOOK_SELECT_PT:  # go select pt
                self.book_select_pt()
            elif self.current_state == State.BOOK_SELECT_SESSION:  # select a session from that pt
                self.book_select_session()
            elif self.current_state == State.BOOK_SELECT_REASON:  # select a reason for seeing the pt
                self.book_select_reason()
            elif self.current_state == State.BOOK_CONFIRM:  # create appointment based on selected information
                self.book_confirm()
            elif self.current_state == State.BOOK_SUCCESS:  # booking done
                self.book_success()



