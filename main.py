from time import sleep
import streamlit as st
from datetime import datetime

st.set_page_config(layout='wide', )

def checking_account(id, pwd):
    try:
        list_ = []
        with open(f"./users/{id}_info.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                list_.append(line.split(":"))
            if list_[1][1] == id and list_[2][1] == pwd:
                if list_[4][1] == "False":
                    return (True, False)
                elif list_[4][1] == "True":
                    return (True, True)
            else:
                return (False, False)
    except FileNotFoundError:
        return (False, False)

# User survey
def survey(id):
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
        once_or_not = st.radio("Once at a day?", ("Yes, I usually sleep once at a day.", "No, I'm not sleep once at a day."))

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
        submitBtn = st.button("Submit")

        # When the survey is finished
        if submitBtn:
            newContent = ""
            with open(f"./users/{id}_info.txt", "r") as file:
                lines = file.readlines()
                for i, l in enumerate(lines):
                    if list(l.split(":"))[0] == "Surveyed":
                        newString = "Surveyed:True\n"
                    elif list(l.split(":"))[0] != "Surveyed":
                        newString = l
                    if newString:
                        newContent += newString
                newContent += f"SleepTime:{night_or_day}\nSleepHours:{sleep_hours}\nWhySleep:{reason}\nSleepingAtOnce:{once_or_not}\nDreamingTimes:{dreaming_times}\nGradeOfSleep:{quality_dream}\nLightState:{light_state}"
            # Update the survey
            with open(f"./users/{id}_info.txt", "w") as f:
                f.write(newContent)
            st.success("Finished ! \n Please Logout and Login again :)")

def read_data(id):
    texts = []
    with open(f"./users/{id}_info.txt", "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            data = line.strip().split(":")
            if data[0] == "SIGN_UP_TIME":
                data[1] = data[1] + ":" + data[2]
                data.pop(2)
            texts.append(data)
    return texts



def create_Account(name, id, password, time):
    userfile = open(f"./users/{id}_info.txt", "w")
    userfile.write(f"NAME:{name}\n")
    userfile.write(f"ID:{id}\n")
    userfile.write(f"PWD:{password}\n")
    userfile.write(f"SIGN_UP_TIME:{time[0:16]}\n")
    userfile.write(f"Surveyed:False")
    userfile.close()
    st.success("Sucessfully finished !")
    st.write("Go to login menu to login.")

def div():
    st.subheader("___________________________")

def short_div():
    st.subheader("____________________")

def compare_days(userID):
    format = '%Y-%m-%d %H:%M'
    userDate = read_data(userID)[3][1]

    date = datetime.strptime(userDate, format)
    now = datetime.now()
    date_diff = now - date
    return date_diff.days, int(date_diff.seconds/3600)


def main():
    # Title message
    st.title("Welcome", anchor=False)

    # Sidebar Menu
    menu = ["Main", "Login", "Sign Up"]
    choose = st.sidebar.selectbox("Menu",menu)
    div()

    # Main page
    if choose == "Main":
        st.write("Click the button on left top to open sidebar")


    # Login page
    if choose == "Login":
        st.subheader("Sign in to see fancy datas!", anchor=False)

        userID = str(st.sidebar.text_input("Enter ID"))
        userPWD = str(st.sidebar.text_input("Enter Password", type="password"))

        st.sidebar.subheader("Click the box to login \nIf click check box again you will logout")
        loginCheckBox = st.sidebar.checkbox("Login")
        checkLogin = checking_account(userID, userPWD)  # Receive a value from userinfo.txt
        if loginCheckBox:

            # Correct ID / PW
            if checkLogin[0]:
                # If user doesn't have survey data.
                if checkLogin[1] == False:
                    survey(userID)

                # After Surveyed
                else:
                    userData = read_data(userID)

                    # Beta alart
                    st.warning("This is beva version. Many things are not working :(")

                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.subheader(f"Hi ! {userData[0][1]}")
                        select_bar = ["Home", "Main", "My info"]
                        main_select_box = st.selectbox("Choose menu",select_bar)
                    with c2:
                        # Home Menu
                        if main_select_box == "Home":
                            st.subheader("This is Home Menu")

                        # Main Menu
                        if main_select_box == "Main":
                            # with c2:
                            st.subheader("Average Sleep time")
                            st.subheader("Grade of Sleep")

                            with c3:
                                st.subheader("Quality of sleep")
                                st.subheader("Light state")


                        # My info
                        if main_select_box == "My info":
                          # with c2:
                            short_div()
                            st.subheader(f"User Id")
                            st.subheader(f"{userData[1][1]}")

                            date_diff = compare_days(userID)
                            short_div()
                            st.subheader(f"Day we spend together")
                            st.subheader(f"{date_diff[0]} Days, {date_diff[1]} Hours")
                            with c3:
                                short_div()
                                st.subheader("Sleep type")
                                st.subheader(f"{userData[5][1]}")
                                short_div()
                                st.subheader("Sleeping Hours")
                                st.subheader(f"{userData[6][1]}")
                                short_div()
                                st.subheader("Reason about sleeping hours")
                                st.subheader(f"{userData[7][1]}")
                                short_div()
                                st.subheader("Sleeping at once ?")
                                st.subheader(f"{userData[8][1][0:2]}.")
                            with c4:
                                short_div()
                                st.subheader("How often you dreaming ?")
                                st.subheader(f"{userData[9][1]} times")
                                short_div()
                                st.subheader("Grade of sleeping")
                                st.subheader(f"Score : {userData[10][1]}")
                                short_div()
                                st.subheader("Turn on light when sleeping ?")
                                st.subheader(f"{userData[11][1]}")

            # Wrong password
            else:
                st.sidebar.write("ID or Password is wrong")



    # Sign up page
    if choose == "Sign Up":
        st.subheader("Thanks for joining us", anchor=False)
        st.header("Name")
        userName = str(st.text_input("Enter your name"))
        st.header("ID / PW", anchor=None)
        userID = str(st.text_input("Make wonderful ID"))
        userPWD = str(st.text_input("Ridicules password is the best", type="password"))
        if len(userPWD) <= 8 and userPWD != None:
            st.info("We recommend you to make long password")
        if (len(userID) >= 2) and (len(userPWD) >= 2) and (len(userName) >= 2):
            if st.checkbox("Agree to save my info"):
                # Save and register user
                if st.button("Sign UP!"):
                    # Make user file
                    create_Account(userName, userID, userPWD, str(f"{datetime.now()}"))




if __name__ == '__main__':
    main()


