from __future__ import annotations

import os
from decimal import Decimal, InvalidOperation

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
)

st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="wide")


def fetch_expenses(category: str | None = None, sort: str | None = None) -> list[dict]:
    params = {}
    if category and category != "All":
        params["category"] = category
    if sort:
        params["sort"] = sort

    response = requests.get(f"{API_BASE_URL}/expenses", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def create_expense(amount: str, category: str, description: str, date_value) -> tuple[bool, str]:
    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date_value),
    }

    response = requests.post(f"{API_BASE_URL}/expenses", json=payload, timeout=10)

    if response.ok:
        return True, "Expense saved successfully."

    try:
        error_payload = response.json()
        return False, error_payload.get("detail", "Failed to save expense.")
    except Exception:
        return False, "Failed to save expense."


def build_expenses_dataframe(expenses: list[dict]) -> pd.DataFrame:
    if not expenses:
        return pd.DataFrame(columns=["id", "amount", "category", "description", "date", "created_at"])

    df = pd.DataFrame(expenses)
    df["amount"] = df["amount"].astype(str)
    return df


def calculate_total(expenses: list[dict]) -> str:
    total = Decimal("0.00")
    for expense in expenses:
        try:
            total += Decimal(str(expense["amount"]))
        except (InvalidOperation, KeyError):
            continue
    return f"₹{total.quantize(Decimal('0.01'))}"


def get_available_categories(expenses: list[dict]) -> list[str]:
    categories = sorted(
        {
            expense["category"]
            for expense in expenses
            if expense.get("category")
        }
    )
    return ["All"] + categories


def main() -> None:
    st.title("Expense Tracker")
    st.caption("A minimal full-stack expense tracker.")

    st.subheader("Add Expense")

    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.text_input("Amount", placeholder="e.g. 250.50")
            category = st.text_input("Category", placeholder="e.g. Food")
        with col2:
            description = st.text_input("Description", placeholder="e.g. Lunch")
            expense_date = st.date_input("Date")

        submitted = st.form_submit_button("Save Expense")

        if submitted:
            if not amount.strip() or not category.strip():
                st.error("Amount and category are required.")
            else:
                try:
                    entered_amount = Decimal(amount.strip())
                    if entered_amount <= 0:
                        st.error("Amount must be greater than zero.")
                        return
                except InvalidOperation:
                    st.error("Please enter a valid numeric amount.")
                    return

                success, message = create_expense(
                    amount=amount.strip(),
                    category=category.strip(),
                    description=description.strip(),
                    date_value=expense_date,
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    st.subheader("Expense List")

    try:
        all_expenses = fetch_expenses(sort="date_desc")
    except requests.RequestException as exc:
        st.error(f"Could not load expenses from the backend API: {exc}")
        return

    categories = get_available_categories(all_expenses)

    filter_col, sort_col, total_col = st.columns([2, 2, 1])

    with filter_col:
        selected_category = st.selectbox("Filter by category", options=categories)

    with sort_col:
        selected_sort = st.selectbox(
            "Sort order",
            options=["Newest first"],
            index=0,
        )

    sort_value = "date_desc" if selected_sort == "Newest first" else None

    try:
        visible_expenses = fetch_expenses(
            category=selected_category,
            sort=sort_value,
        )
    except requests.RequestException as exc:
        st.error(f"Could not refresh filtered expenses: {exc}")
        return

    with total_col:
        st.metric("Total", calculate_total(visible_expenses))

    df = build_expenses_dataframe(visible_expenses)

    if df.empty:
        st.info("No expenses found for the current view.")
        return

    st.dataframe(
        df[["amount", "category", "description", "date", "created_at"]],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()