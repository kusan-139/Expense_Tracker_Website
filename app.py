import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.database import *

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=6000, key="refresh")

st.set_page_config(page_title="Expense Tracker Pro", layout="wide")
st.markdown(
    """
    <style>
    small {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Initialize DB
create_table()

st.title("💰 Expense Tracker Pro (Real-Time + Database)")

# ==============================
# CSV Loading Options
# ==============================

st.sidebar.markdown("## ⚙ Mode Selection")

# Initialize once
if "default_mode" not in st.session_state:
    st.session_state.default_mode = True
if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

def activate_default():
    st.session_state.manual_mode = False

def activate_manual():
    st.session_state.default_mode = False

st.sidebar.checkbox(
    "Default Mode",
    key="default_mode",
    on_change=activate_default
)

st.sidebar.checkbox(
    "Manual Mode",
    key="manual_mode",
    on_change=activate_manual
)

default_mode = st.session_state.default_mode
manual_mode = st.session_state.manual_mode

st.sidebar.markdown("## 📂 Data Loading Options")

if manual_mode:
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )
else:
    uploaded_file = None

# ---- Load CSV to Database ----
st.sidebar.warning("⚠ Load CSV to Database should be used ONLY ONCE to avoid duplicate records.")

if st.sidebar.button("📥 Load CSV to Database"):

    if manual_mode:
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            df_upload.columns = df_upload.columns.str.lower()
            conn = create_connection()
            df_upload.to_sql("transactions", conn, if_exists="append", index=False)
            conn.close()
            st.sidebar.success("Uploaded CSV Loaded Into Database!")
            st.rerun()
        else:
            st.sidebar.warning("Please upload a CSV file first.")
    else:
        load_csv_to_db("data/expenses.csv")
        st.sidebar.success("Default CSV Loaded Into Database!")
        st.rerun()

# ---- Load CSV Only (Temporary View) ----
st.sidebar.markdown("---")

if st.sidebar.button("📄 Load CSV (Only - No DB Save)"):

    if manual_mode:
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            df_upload.columns = df_upload.columns.str.lower()
            st.session_state["csv_only"] = df_upload
            st.sidebar.success("Uploaded CSV Loaded Temporarily!")
        else:
            st.sidebar.warning("Please upload a CSV file first.")
    else:
        df_default = pd.read_csv("data/expenses.csv")
        df_default.columns = df_default.columns.str.lower()
        st.session_state["csv_only"] = df_default
        st.sidebar.success("Default CSV Loaded Temporarily!")

# ---- Add Transaction Form ----
st.sidebar.header("➕ Add New Transaction")

with st.sidebar.form("add_transaction_form", clear_on_submit=True):

    date = st.date_input("Date", format="DD/MM/YYYY")
    category = st.text_input("Category")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    type_ = st.selectbox("Type", ["Expense", "Income"])

    submitted = st.form_submit_button("Add Transaction")

    if submitted:

        # Basic validation (optional but recommended)
        if not category:
            st.warning("Category cannot be empty.")
        elif amount <= 0:
            st.warning("Amount must be greater than 0.")
        else:
            insert_transaction(date.strftime("%d-%m-%Y"), category, description, amount, type_)
            st.success("Transaction Added Successfully!")
            st.rerun()


# ---- Reset Database Button ----
st.sidebar.markdown("---")

if st.sidebar.button("🗑 Reset Database"):
    reset_database()

    # Clear CSV-only session if active
    if "csv_only" in st.session_state:
        del st.session_state["csv_only"]

    st.sidebar.success("Database Reset Successfully!")
    st.rerun()
        
        
st.sidebar.markdown("---")
st.sidebar.markdown("## 📤 Export Options")

if st.sidebar.button("📁 Export DB to CSV"):
    df_export = get_data()

    if not df_export.empty:
        # Ensure datetime
        df_export["date"] = pd.to_datetime(df_export["date"], format="%d-%m-%Y", errors="coerce")

        # Format date without time
        df_export["date"] = df_export["date"].dt.strftime("%d-%m-%Y")

        csv = df_export.to_csv(index=False, float_format="%.2f").encode("utf-8")

        st.sidebar.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="exported_expenses.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("Database is empty.")
          
# ---- Fetch Data ----
# ==============================
# Data Source Selection
# ==============================

if "csv_only" in st.session_state:
    df = st.session_state["csv_only"]
else:
    df = get_data()
    
# ==============================
# Data Cleaning & Normalization
# ==============================

df.columns = df.columns.str.lower()

# Remove duplicate columns if any
df = df.loc[:, ~df.columns.duplicated()]

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

if "month" not in df.columns:
    df["month"] = df["date"].dt.month

# ---- Filters ----
st.sidebar.header("🔎 Filters")
categories = st.sidebar.multiselect(
    "Select Categories",
    df["category"].unique(),
    default=list(df["category"].unique())
)

filtered_df = df[df["category"].isin(categories)]

# ---- Raw Data ----
if "show_raw_data" not in st.session_state:
    st.session_state.show_raw_data = False

show_raw = st.checkbox(
    "Show Raw Data (Editable)",
    key="show_raw_data"
)

if show_raw:

    editable_df = filtered_df.copy()

    # Ensure date stays datetime internally
    editable_df["date"] = pd.to_datetime(editable_df["date"], format="%d-%m-%Y", errors="coerce")
    
    editable_df["date"] = editable_df["date"].dt.date
    
    editable_df.insert(0, "Select", False)
    
    edited_df = st.data_editor(
        editable_df,
        width="stretch",
        key="editor",
        column_config={
            "date": st.column_config.DateColumn(
                "Date",
                format="DD-MM-YYYY"
            )
        }
    )

    if st.button("💾 Save Changes"):

        conn = create_connection()
        cursor = conn.cursor()

        for index, row in edited_df.iterrows():
            cursor.execute("""
                UPDATE transactions
                SET date = ?, 
                    category = ?, 
                    description = ?, 
                    amount = ?, 
                    type = ?
                WHERE id = ?
            """, (
                row["date"].strftime("%d-%m-%Y"),
                row["category"],
                row["description"],
                float(row["amount"]),
                row["type"],
                int(row["id"])
            ))

        conn.commit()
        conn.close()

        st.success("Changes Saved to Database Successfully!")
        st.rerun()

# ---- Delete Selected Rows ----
    if st.button("🗑 Delete Selected Rows"):

        rows_to_delete = edited_df[edited_df["Select"] == True]

        if rows_to_delete.empty:
            st.warning("No rows selected.")
        else:
            conn = create_connection()
            cursor = conn.cursor()

            for row_id in rows_to_delete["id"]:
                cursor.execute(
                    "DELETE FROM transactions WHERE id = ?",
                    (int(row_id),)
                )

            conn.commit()
            conn.close()

            st.success(f"{len(rows_to_delete)} row(s) deleted successfully!")
            st.rerun()

# ---- Charts ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category-wise Total")
    category_total = filtered_df.groupby("category")["amount"].sum()
    st.bar_chart(category_total)

with col2:
    st.subheader("📈 Monthly Trend")
    monthly = (
    filtered_df
    .assign(month=filtered_df["date"].dt.month)
    .groupby("month")["amount"]
    .sum()
    )
    st.line_chart(monthly)

import plotly.express as px

# ---- Pie Chart ----
st.subheader("🥧 Expense Distribution")
expense_df = filtered_df[filtered_df["type"] == "Expense"]
pie_data = expense_df.groupby("category")["amount"].sum().reset_index()

if not pie_data.empty:
    fig = px.pie(
        pie_data, 
        values='amount', 
        names='category', 
        height=550,
        hole=0.4
    )
    # Plotly automatically handles overlapping text and adds interactive tooltips
    fig.update_traces(
        textposition='auto', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: %{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)