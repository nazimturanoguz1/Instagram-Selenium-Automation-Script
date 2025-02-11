from instagramUserInfo import username, password  # Import username and password from a separate file (for security)
from selenium.webdriver.common.by import By  # Importing By class to locate elements
from selenium.webdriver.common.keys import Keys  # Importing Keys to simulate keyboard input
from selenium import webdriver  # Importing Selenium WebDriver
import time  # Importing time module to use sleep for delays
from selenium.webdriver.chrome.service import Service  # Importing Service to manage ChromeDriver
import pandas as pd  # Importing pandas for data handling
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Instagram:
    def __init__(self, username, password):
        """ Initialize the Instagram bot with Chrome WebDriver and login credentials """

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})  # Set Chrome language to English

        service = Service("D:/FollowBot/chromedriver-win64/chromedriver.exe")  # Specify the full path to ChromeDriver
        self.browser = webdriver.Chrome(service=service, options=chrome_options)  # Launch the Chrome browser
        self.username = username
        self.password = password
        self.wait = WebDriverWait(self.browser, 10)  # Initialize WebDriverWait with a timeout of 10 seconds

    def signIn(self):
        """ Log into Instagram using the provided credentials """

        self.browser.get("https://www.instagram.com/accounts/login/")  # Open Instagram login page
        time.sleep(2)  # Wait for the page to load

        # Locate and fill in the username and password fields
        usernameInput = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div[1]/div[1]/div/label/input")))
        passwordInput = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div[1]/div[2]/div/label/input")))
        time.sleep(1)

        usernameInput.send_keys(self.username)  # Enter username
        passwordInput.send_keys(self.password)  # Enter password
        passwordInput.send_keys(Keys.ENTER)  # Press Enter to log in

        # Wait for login to complete (using WebDriverWait)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role=button]")))
        time.sleep(5)  # Wait for login to complete

        self.browser.find_element(By.CSS_SELECTOR, "div[role=button]").click()  # Close the pop-up dialog if it appears
        time.sleep(1)

    def getFollowers(self, username):
        """ Retrieve the list of followers of a given Instagram user """

        self.browser.get(f"https://www.instagram.com/{username}/")  # Open the user's profile page
        time.sleep(2)

        # Click on the followers section
        try:
            followers_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/followers/']")))
            followers_link.click()
            time.sleep(4)
        except Exception as e:
            print(f"Error clicking followers link: {e}")
            return

        # Find the dialog box containing the list of followers
        try:
            dialog = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role=dialog]")))
        except Exception as e:
            print(f"Error locating followers dialog: {e}")
            return

        followerCount = len(dialog.find_elements(By.CSS_SELECTOR, ".x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3"))
        print(f"first count: {followerCount}")  # Print the initial follower count

        # Scroll down to load more followers
        while True:
            dialog.click()  # Click to keep focus on the dialog
            time.sleep(2)

            scroll_count = 5  # Number of times to scroll down
            for i in range(scroll_count):
                self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)  # Scroll down
                time.sleep(1)
                newcount = len(dialog.find_elements(By.CSS_SELECTOR, ".x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3"))

            if followerCount != newcount:  # If new followers are loaded, update count
                followerCount = newcount
                print(f"new count: {followerCount}")  # Print updated count
            else:
                break  # Stop scrolling when no new followers are loaded

        # Extract follower profile links
        users = dialog.find_elements(By.CSS_SELECTOR, ".x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3")

        followerList = []

        for user in users:
            # followerName = user.find_element(By.CSS_SELECTOR,"._ap3a._aaco._aacw._aacx._aad7._aade").text
            followerLink = user.find_element(By.TAG_NAME, "a").get_attribute("href")  # Get profile URL
            followerList.append(followerLink)
            # print(followerLink)

        # Save the follower list to a text file
        with open("followers.txt", "w", encoding="UTF-8") as file:
            for item in followerList:
                file.write(item + "\n")

        # Save the follower list to an Excel file
        df = pd.DataFrame(followerList, columns=["Instagram Followers"])
        df.to_excel("followers.xlsx", index=False, engine='openpyxl')

    def followUser(self, username):
        """ Follow a given Instagram user """

        self.browser.get(f"https://www.instagram.com/{username}")  # Open the user's profile page
        time.sleep(2)

        try:
            followButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Follow']/ancestor::button")))  # Locate the follow button by text
            if followButton.text != "Following":  # Check if the user is not already followed
                followButton.click()  # Click the follow button
                time.sleep(2)
            else:
                print("You are already following this user.")  # Print a message if already following
        except Exception as e:
            print(f"Could not follow user {username}: {e}")

    def unFollowUser(self, username):
        """ Unfollow a given Instagram user """

        self.browser.get(f"https://www.instagram.com/{username}")  # Open the user's profile page
        time.sleep(2)

        try:
            # Locate the follow button (now "Following" or "Requested")
            followButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Following') or contains(text(),'Requested')]/ancestor::button")))

            if followButton.text == "Following" or followButton.text == "Requested":  # Check if the user is followed
                followButton.click()  # Click the button to unfollow
                time.sleep(2)

                # Locate and confirm the unfollow action
                confirmButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Unfollow']")))
                confirmButton.click()  # Confirm unfollow action


            else:
                print("You are not following this user.")  # Print a message if not following
        except Exception as e:
            print(f"Could not unfollow user {username}: {e}")



# Instantiate the Instagram bot with login credentials
instagram = Instagram(username, password)
instagram.signIn()  # Log into Instagram
instagram.getFollowers("makromusic.tr")  # Retrieve followers of a specific user
# Example list of users to follow
# Read the list of users to follow from the Excel file
df = pd.read_excel("D:/FollowBot/githubbotkodu/Instagram-Selenium-Automation-Script/followers.xlsx", engine='openpyxl')
user_list = df["Instagram Followers"].tolist()

# Extract only the username part from the URLs
user_list = [url.split("instagram.com/")[1].strip("/") for url in user_list]

# Follow each user in the list with a delay
for user in user_list:
    instagram.followUser(user)
    time.sleep(600)

# Unfollow a user (commented out)
#instagram.unFollowUser("enter_username_here")