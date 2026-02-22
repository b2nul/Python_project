from datetime import datetime
import streamlit as st

# Page config
st.set_page_config(page_title="Smart Subscription System", layout="wide")

# color section
st.markdown("""
<style>
    /* design card*/
    div[data-testid="column"] {
        background-color: white !important;
        border: 3px solid #6B4E8F !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
    }

    /* design title*/
    div[data-testid="column"] h3 {
        color: #1E0B36 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-top: 0 !important;
        border-bottom: 3px solid #6B4E8F !important;
        padding-bottom: 10px !important;
    }

    /* design text inside card*/
    div[data-testid="column"] p {
        color: #333333 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        margin: 10px 0 !important;
    }

    /* design text*/
    div[data-testid="column"] strong {
        color: #6B4E8F !important;
        font-size: 16px !important;
    }

    /* design alert butten*/
    div[data-testid="column"] .stAlert {
        background-color: #FFEFEF !important;
        color: #B71C1C !important;
        border: 2px solid #B71C1C !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin-top: 10px !important;
    }

    /* design all butten*/
    .stButton button {
        background-color: #6B4E8F !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
    }

    /* design input*/
    .stTextInput input {
        border: 2px solid #D3C5E8 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📱 Smart Subscription Manager")

# Initialize session state
if 'user_accounts' not in st.session_state:
    st.session_state.user_accounts = {}

if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "login"

# CLASSES
# =========================
class CreditCard:
    def __init__(self, name, number, cvc, exp_date):
        self.name = name
        self.__number = number
        self.__cvc = cvc
        self.__exp_date = exp_date

    def mask_number(self):
        return "**** **** **** " + self.__number[-4:]

class UserAccount:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.subscriptions = []

    def add_subscription(self, sub):
        self.subscriptions.append(sub)

    def remove_subscription(self, sub_name):
        for i, sub in enumerate(self.subscriptions):
            if sub['name'] == sub_name:
                self.subscriptions.pop(i)
                return True, f"✅ Removed {sub_name}"
        return False, "❌ Subscription not found"

    def has_subscription(self, sub_name):
        return any(sub['name'] == sub_name for sub in self.subscriptions)

# DATA
# =========================
category_subs = {
    "Health": [
        {"name": "GYM 🏋️", "price": 100},
        {"name": "DIET APP 🥗", "price": 15},
        {"name": "WORKOUT APP 💪", "price": 20}
    ],
    "Entertainment": [
        {"name": "Netflix 🎬", "price": 40},
        {"name": "Disney+ ✨", "price": 35},
        {"name": "Spotify 🎵", "price": 20}
    ],
    "Software": [
        {"name": "Adobe Photoshop 🎨", "price": 50},
        {"name": "Microsoft Office 📊", "price": 60},
        {"name": "VS Code 👨‍💻", "price": 0}
    ],
    "Shopping": [
        {"name": "Amazon prime 🛒", "price": 50},
        {"name": "Noon vip 🛍️", "price": 60},
        {"name": "NiceOne 🎁", "price": 40}
    ]
}

# Create Account Page
def create_account_page():
    st.header("👤 Create New Account")

    with st.form("create_account"):
        username = st.text_input("Username").strip()
        email = st.text_input("Email").strip()
        password = st.text_input("Password", type="password").strip()

        if st.form_submit_button("Create Account"):
            if not (username and email and password):
                st.error("❌ Please fill all fields")
            elif "@" not in email or not email.endswith(".com"):
                st.error("❌ Email must contain '@' and end with '.com'")
            elif username in st.session_state.user_accounts:
                st.error("❌ Username already exists!")
            else:
                new_user = UserAccount(username, email, password)
                st.session_state.user_accounts[username] = new_user
                st.session_state.user = new_user
                st.session_state.page = "main"
                st.success("✅ Account created successfully!")
                st.balloons()
                st.rerun()

    st.divider()
    st.write("Already have an account?")
    if st.button("🔑 Log In"):
        st.session_state.page = "login"
        st.rerun()

def login_page():
    st.header("🔐 Login to your account")

    with st.form("login_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()

        if st.form_submit_button("Login"):
            users = st.session_state.user_accounts
            if username in users and users[username].password == password:
                st.session_state.user = users[username]
                st.session_state.page = "main"
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    st.divider()
    if st.button("📝 Create New Account"):
        st.session_state.page = "signup"
        st.rerun()
# Main Page
def main_page():
    user = st.session_state.user

    with st.sidebar:
        st.title(f"Welcome {user.username}! 👋")
        st.write(f"📧 {user.email}")
        st.divider()

        today = datetime.today()
        alerts = [sub for sub in user.subscriptions
                 if (sub["renewal_date"] - today).days <= 3]

        if alerts:
            st.warning("🚨 Upcoming Payment Alerts")
            for sub in alerts:
                days = (sub["renewal_date"] - today).days
                if days >= 0:
                    st.info(f"📅 {sub['name']}: {days} day(s) remaining")
                else:
                    st.error(f"📅 {sub['name']}: Expired ({abs(days)} days ago)")

        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 My Subscriptions", "➕ Add Subscription", "🗑️ Remove Subscription", "💰 Total Cost"])

    with tab1:
        st.header("My Subscriptions")

        if not user.subscriptions:
            st.info("No subscriptions yet. Add your first one!")
        else:
            today_date = datetime.today().date()
            cols = st.columns(3)

            for i, sub in enumerate(user.subscriptions):
                with cols[i % 3]:
                    renewal_date = sub["renewal_date"].date()
                    remaining_days = (renewal_date - today_date).days

                    with st.container(border=True):
                        st.subheader(sub['name'])
                        st.write(f"💰 **Price:** {sub['price']} SAR")
                        st.write(f"📅 **Renewal:** {renewal_date}")

                        if remaining_days < 0:
                            st.error(f"⏳ **Expired:** {abs(remaining_days)} days ago")
                        else:
                            st.write(f"⏳ **Days left:** {remaining_days}")

                        st.write(f"💳 **Card:** {sub['card']}")

                        if 0 <= remaining_days <= 3:
                            st.warning("⚠️ Renewal soon!")
                        elif remaining_days < 0:
                            st.error("❌ Subscription expired!")

    with tab2:
        st.header("Add New Subscription")

        # Initialize session state for subscription success message
        if 'subscription_added' not in st.session_state:
            st.session_state.subscription_added = False
            st.session_state.added_sub_name = ""

        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox("Choose Category", list(category_subs.keys()))
            subs = category_subs[category]
            sub_names = [f"{s['name']} - {s['price']} SAR" for s in subs]
            selected = st.selectbox("Choose Subscription", sub_names)

            if selected:
                selected_index = sub_names.index(selected)
                selected_sub = subs[selected_index]

                st.write("---")
                st.subheader("Renewal Info")
                renewal_date = st.date_input("Renewal Date", value=datetime.today(), min_value=datetime.today())

        with col2:
            st.subheader("Payment Info")
            card_name = st.text_input("Name on Card")
            card_number = st.text_input("Card Number (16 digits)", max_chars=16)
            col_a, col_b = st.columns(2)
            with col_a:
                cvc = st.text_input("CVC", max_chars=3)
            with col_b:
                exp_date = st.text_input("Expiry Date (MM/YY)", max_chars=5)

        # Show success message if subscription was added
        if st.session_state.subscription_added:
            st.success(f"✅ **{st.session_state.added_sub_name}** subscription added successfully!")

            # Reset the flag after showing the message
            st.session_state.subscription_added = False
            st.session_state.added_sub_name = ""

        if st.button("✅ Confirm Subscription", type="primary"):
            # Validate all fields are filled
            if not (card_name and card_number and cvc and exp_date):
                st.error("❌ Please fill all payment information")

            # Validate card name (letters only)
            elif not card_name.replace(" ", "").isalpha():
                st.error("❌ Card name must contain only letters")

            # Validate card number
            elif len(card_number) != 16 or not card_number.isdigit():
                st.error("❌ Card number must be 16 digits")

            # Validate CVC
            elif len(cvc) != 3 or not cvc.isdigit():
                st.error("❌ CVC must be 3 digits")

            # Validate expiry date format (MM/YY)
            elif len(exp_date) != 5 or exp_date[2] != '/' or not exp_date[:2].isdigit() or not exp_date[3:].isdigit():
                st.error("❌ Expiry date must be in MM/YY format")

            else:
               

                # Check for duplicate subscription
                if any(sub['name'] == selected_sub['name'] for sub in user.subscriptions):
                    st.error("❌ You are already subscribed to this service!")

                # All validations passed - add the subscription
                else:
                    card = CreditCard(card_name, card_number, cvc, exp_date)

                    subscription = {
                        "name": selected_sub["name"],
                        "price": selected_sub["price"],
                        "renewal_date": datetime.combine(renewal_date, datetime.min.time()),
                        "card": card.mask_number()
                    }

                    user.add_subscription(subscription)
                    st.session_state.user_accounts[user.username] = user

                    # Set success message in session state before rerun
                    st.session_state.subscription_added = True
                    st.session_state.added_sub_name = selected_sub["name"]

                    # Rerun to update the UI immediately
                    st.rerun()

    with tab3:
        st.header("Remove Subscription")

        if not user.subscriptions:
            st.info("No subscriptions to remove")
        else:
            cols = st.columns(2)
            for i, sub in enumerate(user.subscriptions):
                with cols[i % 2]:
                    renewal_date = sub["renewal_date"].date()
                    remaining_days = (renewal_date - datetime.today().date()).days

                    with st.container(border=True):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.subheader(sub['name'])
                            st.write(f"💰 {sub['price']} SAR")
                            st.write(f"📅 {renewal_date}")
                            if remaining_days < 0:
                                st.write(f"❌ Expired")
                            else:
                                st.write(f"⏳ {remaining_days} days left")
                        with col_b:
                            st.write("")
                            st.write("")
                            if st.button("🗑️", key=f"del_{i}", use_container_width=True):
                                success, msg = user.remove_subscription(sub['name'])
                                if success:
                                    st.session_state.user_accounts[user.username] = user
                                    st.success(msg)
                                    st.rerun()

    with tab4:
        st.header("Total Cost")

        if not user.subscriptions:
            st.info("No subscriptions")
        else:
            # Calculate total for active subscriptions only
            today = datetime.today().date()
            active_subs = [sub for sub in user.subscriptions if sub["renewal_date"].date() >= today]
            expired_subs = [sub for sub in user.subscriptions if sub["renewal_date"].date() < today]

            total_active = sum(sub["price"] for sub in active_subs)
            total_all = sum(sub["price"] for sub in user.subscriptions)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total (All)", f"{total_all} SAR")
            with col2:
                st.metric("✅ Active Total", f"{total_active} SAR")
            with col3:
                st.metric("📊 Total Subs", len(user.subscriptions))

            st.divider()
            st.subheader("Active Subscriptions")
            if active_subs:
                for sub in active_subs:
                    st.write(f"• **{sub['name']}:** {sub['price']} SAR")
            else:
                st.info("No active subscriptions")

            if expired_subs:
                st.subheader("Expired Subscriptions")
                for sub in expired_subs:
                    st.write(f"• ~~{sub['name']}: {sub['price']} SAR~~ (expired)")

# Page Router
if st.session_state.user is None:
    if st.session_state.page == "login":
        login_page()
    else:
        create_account_page()
else:
    main_page()