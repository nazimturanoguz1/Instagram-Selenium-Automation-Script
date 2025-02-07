# 📸 Instagram Automation Bot

A Python-based Instagram bot that automates login, follower retrieval, following, and unfollowing users using **Selenium WebDriver**.

## 🚀 Features
- **Automatic Login**: Logs in using provided credentials.
- **Fetch Followers**: Retrieves and exports the follower list.
- **Follow Users**: Automates following Instagram users.
- **Unfollow Users**: Automates unfollowing users with confirmation.
- **Data Export**: Saves follower data to `.txt` and `.xlsx` files.

## 🛠️ Technologies Used
- **Python 3.x**
- **Selenium WebDriver**
- **Pandas (for data handling)**
- **Chromedriver**

## 📦 Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-username/Instagram-Automation-Bot.git
cd Instagram-Automation-Bot
```

2️⃣ **Download and set up ChromeDriver**
- Download **ChromeDriver** matching your browser version: [ChromeDriver](https://sites.google.com/chromium.org/driver/)
- Place the `chromedriver.exe` file in the project directory.

## 🔑 Configuration
1. Create a file named **`instagramUserInfo.py`** in the project folder.
2. Add the following lines with your Instagram credentials:
   ```python
   username = "your_username"
   password = "your_password"
   ```
⚠️ **Do NOT share your credentials!** Add `instagramUserInfo.py` to `.gitignore`.

## 🚀 Usage

### **1. Login to Instagram**
```python
from instagram import Instagram
from instagramUserInfo import username, password

bot = Instagram(username, password)
bot.signIn()
```

### **2. Get Followers List**
```python
bot.getFollowers("instagram_username")
```

### **3. Follow a User**
```python
bot.followUser("instagram_username")
```

### **4. Unfollow a User**
```python
bot.unFollowUser("instagram_username")
```

## ⚠️ Disclaimer
This bot is for **educational purposes only**. Using automation on Instagram may violate their **terms of service**. Use it responsibly.

## 🤝 Contributing
Pull requests are welcome! Feel free to fork the repository and submit improvements.

## 📄 License
MIT License. See `LICENSE` for more details.

