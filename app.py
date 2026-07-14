import streamlit as st
import requests
from datetime import date

# =====================================================
# FASTAPI URL
# =====================================================
BASE_URL = "http://127.0.0.1:8000"

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.main{
    background-color:#f4f8fb;
}

h1{
    color:#003366;
    text-align:center;
}

h2,h3{
    color:#0b5394;
}

.stButton>button{
    background:#0b5394;
    color:white;
    border-radius:8px;
    width:100%;
    height:45px;
    font-size:16px;
}

.stButton>button:hover{
    background:#134f8c;
    color:white;
}

div[data-testid="stSidebar"]{
    background:#003366;
}

div[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.title("🏦 Loan Approval System")

# =====================================================
# SESSION STATE
# =====================================================
if "employee_logged_in" not in st.session_state:
    st.session_state.employee_logged_in = False

if "manager_logged_in" not in st.session_state:
    st.session_state.manager_logged_in = False

if "employee_name" not in st.session_state:
    st.session_state.employee_name = ""

if "account_number" not in st.session_state:
    st.session_state.account_number = ""

# =====================================================
# SIDEBAR
# =====================================================
menu = st.sidebar.selectbox(
    "Login As",
    [
        "Employee Login",
        "Manager Login"
    ]
)

# =====================================================
# EMPLOYEE LOGIN
# =====================================================
if menu == "Employee Login":

    st.header("Employee Login")

    employee_name = st.text_input("Employee Name")

    account_number = st.text_input(
        "Account Number",
        type="password"
    )

    if st.button("Login"):

        payload = {
            "employee_name": employee_name,
            "account_number": account_number
        }

        try:

            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=payload
            )

            if response.status_code == 200:

                st.session_state.employee_logged_in = True
                st.session_state.employee_name = employee_name
                st.session_state.account_number = account_number

                st.success("Login Successful")

            else:

                st.error("Invalid Employee Name or Account Number")

        except Exception:

            st.error("Unable to connect to FastAPI Server.")

# =====================================================
# MANAGER LOGIN
# =====================================================
elif menu == "Manager Login":

    st.header("Manager Login")

    manager_id = st.text_input("Manager ID")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if manager_id == "admin" and password == "Admin@123":

            st.session_state.manager_logged_in = True
            st.success("Manager Login Successful")

        else:

            st.error("Invalid Manager Credentials")

# =====================================================
# EMPLOYEE DASHBOARD
# =====================================================
if st.session_state.employee_logged_in:

    st.sidebar.success(
        f"Welcome {st.session_state.employee_name}"
    )

    employee_menu = st.selectbox(
        "Employee Menu",
        [
            "Submit Loan",
            "Update Loan",
            "Delete Loan",
            "View Loan Status"
        ]
    )

    # =====================================================
    # SUBMIT LOAN
    # =====================================================
    if employee_menu == "Submit Loan":

        st.header("Apply for Loan")

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=1000.0,
            step=1000.0
        )

        loan_type = st.selectbox(
            "Loan Type",
            [
                "Personal Loan",
                "Home Loan",
                "Education Loan",
                "Vehicle Loan",
                "Business Loan"
            ]
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=1000.0
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            step=1
        )

        loan_date = st.date_input(
            "Application Date",
            value=date.today()
        )

        if st.button("Submit Loan"):

            payload = {

                "employee_name":
                st.session_state.employee_name,

                "account_number":
                st.session_state.account_number,

                "loan_amount":
                loan_amount,

                "loan_type":
                loan_type,

                "monthly_income":
                monthly_income,

                "credit_score":
                credit_score,

                "date":
                str(loan_date)

            }

            try:

                response = requests.post(
                    f"{BASE_URL}/employee/apply-loan",
                    json=payload
                )

                if response.status_code == 200:

                    st.success(
                        "Loan Application Submitted Successfully."
                    )

                    st.json(response.json())

                else:

                    st.error(
                        response.json()["detail"]
                    )

            except Exception:

                st.error(
                    "Unable to connect to FastAPI Server."
                )

    # =====================================================
    # UPDATE LOAN
    # =====================================================
    elif employee_menu == "Update Loan":

        st.header("Update Loan")

        loan_id = st.number_input(
            "Loan ID",
            min_value=1,
            step=1
        )

        loan_amount = st.number_input(
            "New Loan Amount",
            min_value=1000.0,
            step=1000.0
        )

        loan_type = st.selectbox(
            "Loan Type",
            [
                "Personal Loan",
                "Home Loan",
                "Education Loan",
                "Vehicle Loan",
                "Business Loan"
            ],
            key="update_type"
        )

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            step=1000.0,
            key="update_income"
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            key="update_score"
        )

        loan_date = st.date_input(
            "Application Date",
            value=date.today(),
            key="update_date"
        )

        if st.button("Update Loan"):

            payload = {

                "loan_amount": loan_amount,
                "loan_type": loan_type,
                "monthly_income": monthly_income,
                "credit_score": credit_score,
                "date": str(loan_date)

            }

            try:

                response = requests.put(
                    f"{BASE_URL}/employee/update/{loan_id}",
                    json=payload
                )

                if response.status_code == 200:

                    st.success("Loan Updated Successfully")
                    st.json(response.json())

                else:

                    st.error(response.json()["detail"])

            except Exception:

                st.error("Unable to connect to FastAPI Server.")

    # =====================================================
    # DELETE LOAN
    # =====================================================
    elif employee_menu == "Delete Loan":

        st.header("Delete Loan")

        loan_id = st.number_input(
            "Loan ID",
            min_value=1,
            step=1,
            key="delete_id"
        )

        if st.button("Delete Loan"):

            try:

                response = requests.delete(
                    f"{BASE_URL}/employee/delete/{loan_id}"
                )

                if response.status_code == 200:

                    st.success("Loan Deleted Successfully")

                else:

                    st.error(response.json()["detail"])

            except Exception:

                st.error("Unable to connect to FastAPI Server.")

    # =====================================================
    # VIEW LOAN STATUS
    # =====================================================
    elif employee_menu == "View Loan Status":

        st.header("My Loan Status")

        try:

            response = requests.get(
                f"{BASE_URL}/employee/status/{st.session_state.account_number}"
            )

            if response.status_code == 200:

                loans = response.json()

                if loans:

                    st.dataframe(
                        loans,
                        use_container_width=True
                    )

                else:

                    st.info("No Loan Applications Found.")

            else:

                st.error(response.json()["detail"])

        except Exception:

            st.error("Unable to connect to FastAPI Server.")

# =====================================================
# MANAGER DASHBOARD
# =====================================================
if st.session_state.manager_logged_in:

    st.sidebar.success("Manager Logged In")

    st.header("Manager Dashboard")

    manager_menu = st.selectbox(
        "Manager Menu",
        [
            "View All Loan Requests",
            "Approve Loan",
            "Reject Loan"
        ]
    )

    # =====================================================
    # VIEW ALL LOAN REQUESTS
    # =====================================================
    if manager_menu == "View All Loan Requests":

        try:

            response = requests.get(
                f"{BASE_URL}/admin/loans"
            )

            if response.status_code == 200:

                loans = response.json()

                if loans:
                    st.dataframe(
                        loans,
                        use_container_width=True
                    )
                else:
                    st.info("No Loan Requests Found.")

            else:

                st.error(response.json()["detail"])

        except Exception:

            st.error("Unable to connect to FastAPI Server.")

    # =====================================================
    # APPROVE LOAN
    # =====================================================
    elif manager_menu == "Approve Loan":

        st.subheader("Approve Loan")

        loan_id = st.number_input(
            "Loan ID",
            min_value=1,
            step=1,
            key="approve_id"
        )

        if st.button("Approve"):

            try:

                response = requests.put(
                    f"{BASE_URL}/admin/approve/{loan_id}"
                )

                if response.status_code == 200:

                    st.success("Loan Approved Successfully")
                    st.json(response.json())

                else:

                    st.error(response.json()["detail"])

            except Exception:

                st.error("Unable to connect to FastAPI Server.")

    # =====================================================
    # REJECT LOAN
    # =====================================================
    elif manager_menu == "Reject Loan":

        st.subheader("Reject Loan")

        loan_id = st.number_input(
            "Loan ID",
            min_value=1,
            step=1,
            key="reject_id"
        )

        if st.button("Reject"):

            try:

                response = requests.put(
                    f"{BASE_URL}/admin/reject/{loan_id}"
                )

                if response.status_code == 200:

                    st.success("Loan Rejected Successfully")
                    st.json(response.json())

                else:

                    st.error(response.json()["detail"])

            except Exception:

                st.error("Unable to connect to FastAPI Server.")


# =====================================================
# LOGOUT
# =====================================================
st.sidebar.markdown("---")

if st.sidebar.button("Logout"):

    st.session_state.employee_logged_in = False
    st.session_state.manager_logged_in = False

    st.session_state.employee_name = ""
    st.session_state.account_number = ""

    st.success("Logged Out Successfully")

    st.rerun()