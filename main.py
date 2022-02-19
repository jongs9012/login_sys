
import streamlit as st
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData
import datetime


# When the btn pressed, Add some values to notice it clicked
# So it can draw some interface to interact with client

st.title("WELCOME")
logined = False

if logined == False:
    if st.button("Sign in"):
        st.subheader("Log in to see fancy datas!")
        userID = str(st.text_input("Enter ID"))
        userPWD = str(st.text_input("Enter Password", type="password"))
        if st.button("Log in"):
            # Sleeping Day or Night ?
            st.subheader("Are you sleeping at Night or Day ?")
            nightOrDay = st.radio("Night or Day", ("Day", "Night"))

            # Sleeping Hours
            st.subheader(f"How many hours you sleep at {nightOrDay}?")
            sleep_hours = st.radio("Hours you sleep", ("4 ~ 5 hours", "5 ~ 6 hours", "6 ~ 7 hours", "Others"))

            # Reason about sleeping that hours
            temp = "Why do you sleep not normally?" if sleep_hours is "Others" else f"Why do you sleeping {sleep_hours}"
            st.subheader(temp)
            reason = str(st.text_input("Please enter reason"))

            if len(reason) >= 1:
                c1, c2 = st.columns(2)
                with c1:
                    tempInC1 = "Are you sleeping at Once?" if sleep_hours is "Others" else f"Are you sleeping {sleep_hours} at Once?"
                    st.write(" ")
                    st.subheader(tempInC1)
                with c2:
                    st.subheader(" ")
                    onceOrNot = st.radio(" ",("Yes, I usually sleep once at a day.", "No, I'm not sleep once at a day."))

    # SIGN UP
    elif st.button("Sigh up"):
        st.subheader("Thanks for joining us")
        col1, col2 = st.columns(2)
        with col1:  # Set username
            st.header("Name")
            usernameOnsignup = str(st.text_input("Enter your name"))

        with col2:  # Set userID / userPWD
            st.header("ID / PW")
            useridOnSignup = str(st.text_input("Make wonderful ID"))
            userpwdOnSighup = str(st.text_input("Ridiculas PWD is the best", type="password"))
            if len(userpwdOnSighup) <= 8 and userpwdOnSighup != None:
                st.info("We recommend you to make long password")

        if (len(useridOnSignup) >= 2) and (len(userpwdOnSighup) >= 2) and (len(usernameOnsignup) >= 2):
            if st.checkbox("Agree to save your info"):
                if st.button("Sign UP!"):
                    userfile = open(f"./{usernameOnsignup}_info.txt", "w")
                    userfile.write(f"name : {usernameOnsignup}\n")
                    userfile.write(f"ID : {useridOnSignup}\n")
                    userfile.write(f"PWD : {userpwdOnSighup}\n")
                    userfile.write(f"SighUP time : {datetime.datetime.now()}")
                    userfile.close()
                    logined = True
                    st.experimental_rerun()
