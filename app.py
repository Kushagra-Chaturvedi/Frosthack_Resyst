import streamlit as st
import streamlit.components.v1 as components
from database_fx import *
import base64
import pandas as pd
import numpy as np


def findGeocode(city):
    try:

        geolocator = Nominatim(user_agent='')
          
        return geolocator.geocode(city)
      
    except GeocoderTimedOut:
          
        return findGeocode(city) 

def login():
	email_id = st.sidebar.text_input("Email ID")
	password = st.sidebar.text_input("Password ", type = 'password')
	if st.sidebar.button("LOGIN"):
		create_usertable()
		hashed_pwd = make_hashes(password)
		result2 = existing_user(email_id)
		result3 = check_pass(check_hashes(password, hashed_pwd))
		if result2 and result3 :
			st.success("Logged in Successfully" )
			return email_id
		elif result2 and ( not result3):
			st.warning("Incorrect password")
			return 0
		else:
			st.warning("User not exist. Please create an account")
			return 0

def sp(donor_type):
	if len(donor_type)==0:
		return [0,0,0]
	if len(donor_type)==1:
		if donor_type[0] == "Oxygen Cylinders":
			return [1,0,0]
		elif donor_type[0] == "Plasma":
			return [0,1,0]
		elif donor_type[0] == "Remdesivir Doses":
			return[0,0,1]
	if len(donor_type) ==2:
		if ("Oxygen Cylinders" in donor_type) and ("Plasma" in donor_type) :
			return[1,1,0]
		elif ("Oxygen Cylinders" in donor_type) and ("Remdesivir Doses" in donor_type) :
			return[1,0,1]
		elif ("Plasma" in donor_type) and ("Remdesivir Doses" in donor_type) :
			return[1,0,1]
	else :
		return [1,1,1]


def main():
	""" Simple Login"""
	Menu = ['Home','Service Provider', "Acceptors"]	
	choice = st.sidebar.selectbox("Menu", Menu)
	if choice == "Home":

		st.title("Covid Crisis ")
		LOGO_IMAGE = "banner-corona.png"
		st.markdown(
	    """
	    <style>
	    .container {
	        display: flex;
	    }
	    .logo-img {
	        float:right;
	        max-width : auto;
	        height : auto;

	    }
	    @media only screen and (max-width : 600px){
	    .logo-img{
	    	max-width : 300px;
	    	max-height :112px;
	    }
	    }
	    @media only screen and (max-width : 350px){
	    .logo-img{
	    	max-width : 200px;
	    	max-height :75px;
	    }
	    }
	    @media only screen and (min-width : 1300px){
	    .logo-img{
	    	max-width : 1100x;
	    	max-height :411px;
	    }
	    }
	    </style>
	    """,unsafe_allow_html=True)
		st.markdown(
	    f"""
	    <div class="container">
	        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
	    </div>
	    """,unsafe_allow_html=True)
		st.markdown("""
			 This platform is build to provide relief to patients and to help thosewho want to donate or help patients in 
			dire need of some aid. From donating plasma tomoney or any other resources, everything can be done. We would connect you
			 directly with the patients and you can help them. This will be a transparent process as you are directly connecting with
			  the patient so no need to worry about corruption.""")

	elif choice=="Service Provider":
		sp_menu = ["Login", "SignUp"]
		sp_choice = st.selectbox("Menu", sp_menu)
		if sp_choice=="SignUp":
			st.subheader("Create an Account")
			new_user = st.text_input('Username')
			email_id = st.text_input("Email ID")
			new_passwd = st.text_input('Password',type='password')
			if st.button('SignUp'):
				create_usertable()
				add_userdata(new_user,email_id,make_hashes(new_passwd))
				st.success("You have successfully created an account.Go to the Login Menu to login")		
		elif sp_choice=="Login":
			email_id = st.sidebar.text_input("Email ID")
			password = st.sidebar.text_input("Password ", type = 'password')
			hashed_pwd = make_hashes(password)
			email = email_id
			h_pwd = hashed_pwd
			pwd = password
			if st.sidebar.button("LOGIN"):
				create_usertable()
				result2 = existing_user(email_id)
				result3 = check_pass(check_hashes(password, hashed_pwd))
				if result2 and result3 :
					st.success("Logged in Successfully" )
				elif result2 and ( not result3):
					st.warning("Incorrect password")
				else:
					st.warning("User not exist. Please create an account")
			if login_user(email, check_hashes(pwd,h_pwd)):
				pin = st.text_input('Pin Code')
				city = st.text_input("City")
				state = st.text_input("State")
				phone = st.text_input("Contact Number")
				upi = st.text_input("UPI ID")
				items = ['Oxygen Cylinders','Plasma','Remdesivir Doses']
				donor_type = st.multiselect("Select what services your are providing", items )
				global avilable
				avilable = donor_type 
				if st.button("Register"):
					st.write('#Congrats !! Your information is saved corresponding to  this email adress : ' + str(email))
					st.success("Registered as a Service Provider of {}" .format(donor_type))
					oxy, plasma, rem = sp(donor_type)[0],sp(donor_type)[1],sp(donor_type)[2]
					oxy='Oxygen Cylinders' if oxy==1 else None
					plasma='Plasma' if plasma==1 else None
					rem='Remdesivir Doses' if rem==1 else None 
					create_sp()
					add_service_provider(email_id, oxy,plasma,rem,pin,city,state,phone, upi)

	elif choice=="Acceptors":
		needed = st.selectbox("Select what services your are providing", ['','Oxygen Cylinders','Plasma','Remdesivir Doses'])
		pin_code = st.text_input("Pin code")
		pin = pin_code
		donors = find_donors(pin,needed)
		df = pd.DataFrame(donors,columns=("Email Adress","Oxygen","Plasma","Remdesivir","Pin Code", "City","State","Phone","UPI ID"))
		if st.button("Submit"):
			if len(donors)==0:
				st.warning("Sorry!! We do not have any donors nearby.")
			else:
				st.success("List of avilable Service Providers is Given below")
				#st.table(df)
				for i in range(len(donors)):
					refined = refine_donors(donors[i][0])
				refined = pd.DataFrame(refined, columns= ('Username','email','pass'))
				dfnew= pd.DataFrame([refined['Username'], df["Email Adress"], df["Phone"],df[ "City"],df["Pin Code"],df["State"],df["UPI ID"]])
				st.table(dfnew)
if __name__ == '__main__':
	main()
