from os import path, listdir
import streamlit as st
from datetime import datetime

st.set_page_config(layout='wide')


def read_data(id_):
    return_value = []
    with open(f"./users/{id_}_info.txt", "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            data = line.strip().split(":")
            if data[0] == "SIGN_UP_TIME":
                data[1] = data[1] + ":" + data[2]
                data.pop(2)
            return_value.append(data)
    return return_value


def checking_account(id_, pwd):
    try:
        list_ = []
        with open(f"./users/{id_}_info.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                line = line.strip()
                list_.append(line.split(":"))
            if list_[1][1] == id_ and list_[2][1] == pwd:
                if list_[4][1] == "False":
                    return True, False
                elif list_[4][1] == "True":
                    return True, True
            else:
                return False, False
    except FileNotFoundError:
        return False, False


# User survey
def survey(id_):
    # Sleeping Day or Night ?
    st.subheader("Are you sleeping at Night or Day ?", anchor=False)
    night_or_day = st.radio("Night or Day", ("Day", "Night"))
    # Sleeping Hours
    st.subheader(f"How many hours you sleep at {night_or_day}?")
    sleep_hours = st.radio("Hours you sleep", ("4 ~ 5 hours", "5 ~ 6 hours", "6 ~ 7 hours", "Others"))
    # Reason about sleeping that hours
    temp = "Why do you sleep not normally?" if sleep_hours == "Others" else f"Why do you sleeping {sleep_hours}"
    st.subheader(temp)
    reason = str(st.text_input("Please enter reason"))
    if len(reason) >= 1:
        temp = "Are you sleeping at Once?" if sleep_hours == "Others" else f"Are you sleeping {sleep_hours} at Once?"
        st.subheader(temp)
        once_or_not = st.radio("Once at a day?", ("Yes, I usually sleep once at a day.",
                                                  "No, I'm not sleep once at a day."))

        st.subheader("How many times a week do you dream ?")
        dreaming_times = st.radio("Times you dreaming", ("0 ~ 1 times", "2 ~ 3 times", "4 ~ 5 times", "Others"))
        st.subheader("If you were to grade your sleep?")
        quality_dream = st.slider("Score", 0, 100, 70)
        st.write(f"[ Score : {quality_dream} ]")

        light_state = st.radio("Do you sleep with the lights on?", ("Turn on", "Turn off"))
        st.subheader("")
        div()
        st.write("Do you agree to provide information?")
        st.write("It's not used for commercial purpose and is used for information analysis.")
        submit_btn = st.button("Submit")

        # When the survey is finished
        if submit_btn:
            new_content = ""
            with open(f"./users/{id_}_info.txt", "r") as file:
                lines = file.readlines()
                for i, l in enumerate(lines):
                    if list(l.split(":"))[0] == "Surveyed":
                        new_string = "Surveyed:True\n"
                    elif list(l.split(":"))[0] != "Surveyed":
                        new_string = l
                    if new_string:
                        new_content += new_string
                new_content += f"SleepTime:{night_or_day}\n" \
                               f"SleepHours:{sleep_hours}\n" \
                               f"WhySleep:{reason}\n" \
                               f"SleepingAtOnce:{once_or_not}\n" \
                               f"DreamingTimes:{dreaming_times}\n" \
                               f"GradeOfSleep:{quality_dream}\n" \
                               f"LightState:{light_state}"
            # Update the survey
            with open(f"./users/{id_}_info.txt", "w") as f:
                f.write(new_content)
            st.success("Finished ! \n Please Logout and Login again :)")


def scrap_data():
    all_data = []
    for filename in listdir("./users"):
        print("File name :", filename)
        '''
        with open(path.join("./users", filename), "r") as f:
            text = f.read()
        '''
        all_data.append(read_data(filename[0:-9]))
    return all_data


def find_average(index):
    data_list = []
    for filename in listdir("./users"):
        data_list.append(read_data(filename[0:-9]))
    value_list = []
    for i, value in enumerate(data_list):
        if value[4][1] == "True":
            value_list.append(value[index][1])
        else:
            pass
    return value_list


def create_account(name, id_, password, time):
    user_file = open(f"./users/{id_}_info.txt", "w")
    user_file.write(f"NAME:{name}\n")
    user_file.write(f"ID:{id_}\n")
    user_file.write(f"PWD:{password}\n")
    user_file.write(f"SIGN_UP_TIME:{time[0:16]}\n")
    user_file.write(f"Surveyed:False")
    user_file.close()
    st.success("Successfully finished !")
    st.write("Go to login menu to login.")


def div():
    st.subheader("___________________________")


def short_div():
    st.subheader("____")


def compare_days(user_id):
    format_ = '%Y-%m-%d %H:%M'
    user_date = read_data(user_id)[3][1]

    date = datetime.strptime(user_date, format_)
    now = datetime.now()
    date_diff = now - date
    return date_diff.days, int(date_diff.seconds/3600)


def main():
    # Title message
    st.title("Welcome", anchor=False)

    # Sidebar Menu
    menu = ["Main", "Login", "Sign Up"]
    choose = st.sidebar.selectbox("Menu", menu)
    div()

    # Main page
    if choose == "Main":
        st.write("Click the button on left top to open sidebar")

    # Login page
    if choose == "Login":
        st.subheader("Sign in to see fancy data!", anchor=False)

        user_id = str(st.sidebar.text_input("Enter ID"))
        user_pwd = str(st.sidebar.text_input("Enter Password", type="password"))

        st.sidebar.subheader("Click the box to login \nIf click check box again you will logout")
        login_check_box = st.sidebar.checkbox("Login")
        check_login = checking_account(user_id, user_pwd)  # Receive a value from userinfo.txt
        if login_check_box:

            # Correct ID / PW
            if check_login[0]:
                # If user doesn't have survey data.
                if check_login[1] is False:
                    survey(user_id)

                # After Surveyed
                else:
                    user_data = read_data(user_id)

                    # Beta alarm
                    st.warning("This is beta version. Many things are not working :(")
                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.subheader(f"Hi ! {user_data[0][1]}")
                        select_bar = ["Home", "Main", "My info"]
                        main_select_box = st.selectbox("Choose menu", select_bar)

                    with c2:
                        # Home Menu
                        if main_select_box == "Home":
                            st.subheader("This is Home Menu")

                        # Main Menu
                        if main_select_box == "Main":
                            # with c2:
                            st.subheader("Average Sleep time")
                            st.write(find_average(6))
                            st.subheader("Grade of Sleep")
                            st.write(find_average(10))

                            with c3:
                                st.subheader("Quality of sleep")
                                st.write(find_average(8))
                                st.subheader("Light state")
                                st.write(find_average(11))

                        # My info
                        if main_select_box == "My info":

                            with c1:
                                info_menu = ["Account", "Survey Info"]
                                info_choose = st.selectbox("Menu", info_menu)
                            # with c2:
                            if info_choose == "Account":
                                short_div()
                                st.subheader(f"User Id")
                                st.subheader(f"{user_data[1][1]}")
                                with c3:
                                    date_diff = compare_days(user_id)
                                    short_div()
                                    st.subheader(f"Day we spend together")
                                    st.subheader(f"{date_diff[0]} Days, {date_diff[1]} Hours")
                            if info_choose == "Survey Info":

                                short_div()
                                st.subheader("Sleep type")
                                st.subheader(f"{user_data[5][1]}")
                                short_div()
                                st.subheader("Sleeping Hours")
                                st.subheader(f"{user_data[6][1]}")
                                with c3:
                                    short_div()
                                    st.subheader("Reason about sleeping hours")
                                    st.subheader(f"{user_data[7][1]}")
                                    short_div()
                                    st.subheader("Sleeping at once ?")
                                    st.subheader(f"{user_data[8][1][0:3]}.")
                                with c4:
                                    short_div()
                                    st.subheader("How often you dreaming ?")
                                    st.subheader(f"{user_data[9][1]} times")
                                    short_div()
                                    st.subheader("Grade of sleeping")
                                    st.subheader(f"Score : {user_data[10][1]}")
                                    short_div()
                                    st.subheader("Turn on light when sleeping ?")
                                    st.subheader(f"{user_data[11][1]}")

            # Wrong password
            else:
                st.sidebar.write("ID or Password is wrong")

    # Sign up page
    if choose == "Sign Up":
        st.subheader("Thanks for joining us", anchor=False)
        st.header("Name")
        user_name = str(st.text_input("Enter your name"))
        st.header("ID / PW", anchor=None)
        user_id = str(st.text_input("Make wonderful ID"))
        user_pwd = str(st.text_input("Ridicules password is the best", type="password"))
        if len(user_pwd) <= 8 and user_pwd is not None:
            st.info("We recommend you to make long password")
        if (len(user_id) >= 2) and (len(user_pwd) >= 2) and (len(user_name) >= 2):
            if st.checkbox("Agree to save my info"):
                # Save and register user
                if st.button("Sign UP!"):
                    # Make user file
                    if path.exists(f"./users/{user_id}_info.txt"):
                        st.warning("This id is already existence. Please use another ID.")
                    else:
                        create_account(user_name, user_id, user_pwd, str(f"{datetime.now()}"))


if __name__ == '__main__':
    main()
