import streamlit as st
from snscrape.modules.twitter import TwitterUserScraper
from snscrape.base import ScraperException
import re
import time 

def convert(val):
    # detemining whether val is username or ID
    val = str(val)
    res = bool(re.search(r"\s", val))
    if not res:
        try:
            val = int(val)
        except:
            val = val.replace("@","")
        
        # fetching username as val is numerical id
        if type(val)==int:
            try:
                master = TwitterUserScraper(val).entity
                Screen_Name = master.username
                profile_pic = master.profileImageUrl.replace("normal.jpg","200x200.jpg")
                redirect_url = f"https://twitter.com/intent/user?screen_name={Screen_Name}"
    
            except AttributeError or ScraperException:
                Screen_Name = f"USER ID - {val} DOES NOT EXIST, kindly enter correct userID"
                profile_pic = False
                redirect_url = False
                master = False
        # fetching ID as val is username
        else:
            try:
                master = TwitterUserScraper(val).entity
                User_ID = master.id
                profile_pic = master.profileImageUrl.replace("normal.jpg","200x200.jpg")
                redirect_url = f"https://twitter.com/intent/user?user_id={User_ID}"
                
            except AttributeError or ScraperException:
                User_ID = f"USERNAME - @{val} DOES NOT EXIST, kindly enter correct username"
                profile_pic = False
                redirect_url = False
                master = False
    
        if type(val)==int: return '@'+Screen_Name,profile_pic,redirect_url,master
        else: return User_ID,profile_pic,redirect_url,master
            
    # handling incrrect username format i.e it contains spaces 
    else:return (f"INCORRECT USERNAME FORMAT - {val} contains spaces, kindly enter correct username"),False,False,False
 


def main():
    st.set_page_config(
    page_title="TWConverter",
    page_icon="🐦",
)
    st.title("#")  
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title("Twitter Username to ID converter and Vice versa")
    
    st.header("Enter Twitter Username/ID")
    val = st.text_input("Eg: @edgeforex1 or 1234567890",key="placeholder",)
    submit = st.button("Find User")
    if submit and val:
        res,profilePic,redirectUrl,master = convert(val)
        with st.spinner('Searching...'):
            time.sleep(3)
        if profilePic:
            st.subheader("The user you're looking for is:")
            st.header(res)
            st.text("");st.text("")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'''
                            <a href="{redirectUrl}">
                            <img src="{profilePic}" />
                            </a>''',
                            unsafe_allow_html=True
                )
            with col2:
                dispName = "Display Name: "+master.displayname
                followCount = "Follower's Count: "+str(master.followersCount)
                followinCount = "Following Count: "+str(master.friendsCount)
                tweetCount = "Tweets Count: "+str(master.statusesCount)
                st.text(dispName)
                st.text(followCount)
                st.text(followinCount)
                st.text(tweetCount)
        else:
            st.error(res)

    ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
with <img src="https://em-content.zobj.net/source/skype/289/red-heart_2764-fe0f.png" alt="heart" height= "10"/><a style='display: inline; text-align: left;' href="https://edge-forex.com/" target="_blank"> by EdgeForex</a></p>
</div>

</div>
"""
    st.write(ft, unsafe_allow_html=True)
if __name__=="__main__":
    main()