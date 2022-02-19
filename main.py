from time import sleep
import streamlit as st
import datetime

st.set_page_config(layout='wide', )

def avaliable_account(id, pwd):
    return True



# User survey
def survey():
    # Sleeping Day or Night ?
    st.subheader("Are you sleeping at Night or Day ?", anchor=False)
    nightOrDay = st.radio("Night or Day", ("Day", "Night"))
    # Sleeping Hours
    st.subheader(f"How many hours you sleep at {nightOrDay}?")
    sleep_hours = st.radio("Hours you sleep", ("4 ~ 5 hours", "5 ~ 6 hours", "6 ~ 7 hours", "Others"))
    # Reason about sleeping that hours
    temp = "Why do you sleep not normally?" if sleep_hours == "Others" else f"Why do you sleeping {sleep_hours}"
    st.subheader(temp)
    reason = str(st.text_input("Please enter reason"))
    if len(reason) >= 1:
        onceOrNot = st.radio(" ", ("Yes, I usually sleep once at a day.", "No, I'm not sleep once at a day."))
        st.subheader("How many times a week do you dream ?")
        dreamingTimes = st.radio("Times you dreaming", ("0 ~ 1 times", "2 ~ 3 times", "4 ~ 5 times", "Others"))
        qualityDream = st.slider("If you were to grade your sleep?", 0, 100, 70)
        st.write(f"[ Score : {qualityDream} ]")
        temp = "Are you sleeping at Once?" if sleep_hours == "Others" else f"Are you sleeping {sleep_hours} at Once?"
        st.subheader(temp)
        lightState = st.radio("Do you sleep with the lights on?", ("Turn on", "Turn off"))
        st.subheader("")
        st.subheader("_______________________________")
        st.write("Do you agree to provide information?")
        st.write("It's not used for commercial purpose and is used for information analysis.")
        submitBtn = st.button("Submit")


def create_Account(name, id, password, time):
    userfile = open(f"./users/{name}_info.txt", "w")
    userfile.write(f"name:{name}\n")
    userfile.write(f"ID:{id}\n")
    userfile.write(f"PWD:{password}\n")
    userfile.write(f"Sign_up_time:{time}")
    userfile.close()
    st.success("Sucessfully finished !")
    st.write("Go to login menu to login.")


def main():
    # Title message
    st.title("Welcome", anchor=False)

    # Sidebar Menu
    menu = ["Main", "Login", "Sign Up"]
    choose = st.sidebar.selectbox("Menu",menu)

    # Main page
    if choose == "Main":
        st.subheader("We handle so many data that can make you surprise.")
        st.subheader("Why don't you sign up to see all data?")


    # Login page
    if choose == "Login":
        st.subheader("Sign in to see fancy datas!", anchor=False)
        st.subheader("_______________________________")

        userID = str(st.sidebar.text_input("Enter ID"))
        userPWD = str(st.sidebar.text_input("Enter Password", type="password"))

        if len(userID) >= 1 and len(userPWD) >= 1:
            st.sidebar.subheader("Click the box to login \nIf click check box again you will logout")
        loginCheckBox = st.sidebar.checkbox("Login")
        tested = False  # Receive a value from userinfo.txt
        if loginCheckBox:
            if avaliable_account(userID, userPWD):
                if tested == False:
                    survey()
                else:
                    st.subheader("Passed")
            # If user doesn't have survey data.
            else:
                st.sidebar.write("ID or Password is wrong")



    # Sign up page
    if choose == "Sign Up":
        st.subheader("Thanks for joining us", anchor=False)
        st.subheader("_______________________________")
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
                    create_Account(userName, userID, userPWD, datetime.datetime.now())




if __name__ == '__main__':
    main()


