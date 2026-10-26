
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Sample student data
data = {
    "Student": [
        "Aman", "Rohit", "Priya", "Neha", "Karan",
        "Simran", "Arjun", "Pooja", "Rahul", "Anjali"
    ],
    "Python": [85, 65, 92, 45, 78, 88, 56, 73, 35, 95],
    "DBMS": [80, 70, 89, 50, 75, 91, 60, 68, 40, 93],
    "Networking": [78, 72, 95, 42, 82, 85, 58, 76, 38, 90]
}

df = pd.DataFrame(data)

subjects = ["Python", "DBMS", "Networking"]

df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1).round(2)
df["Result"] = df["Average"].apply(
    lambda marks: "Pass" if marks >= 40 else "Fail"
)

def get_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    return "F"

df["Grade"] = df["Average"].apply(get_grade)

st.title("🎓 Student Performance Dashboard")
st.write("Analyze student marks, grades and results.")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

selected_result = st.sidebar.selectbox(
    "Select Result",
    ["All", "Pass", "Fail"]
)

selected_subject = st.sidebar.selectbox(
    "Select Subject",
    subjects
)

filtered_df = df.copy()

if selected_result != "All":
    filtered_df = filtered_df[
        filtered_df["Result"] == selected_result
    ]

# Summary metrics
st.subheader("Performance Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(filtered_df))

if len(filtered_df) > 0:
    col2.metric(
        "Average Marks",
        round(filtered_df["Average"].mean(), 2)
    )

    col3.metric(
        "Highest Average",
        round(filtered_df["Average"].max(), 2)
    )

    pass_rate = (
        filtered_df["Result"].eq("Pass").mean() * 100
    )

    col4.metric("Pass Rate", f"{pass_rate:.1f}%")

    # Student records
    st.subheader("Student Records")
    st.dataframe(filtered_df, use_container_width=True)

    # Subject-wise marks
    st.subheader(f"{selected_subject} Marks")
    subject_chart = filtered_df.set_index("Student")[
        [selected_subject]
    ]
    st.bar_chart(subject_chart)

    # Average comparison
    st.subheader("Student Average Comparison")
    average_chart = filtered_df.set_index("Student")[["Average"]]
    st.bar_chart(average_chart)

    # Top performer
    st.subheader("Top Performer")

    top_student = filtered_df.loc[
        filtered_df["Average"].idxmax()
    ]

    st.success(
        f"{top_student['Student']} scored an average "
        f"of {top_student['Average']} marks "
        f"and received Grade {top_student['Grade']}."
    )

    # Download data
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Student Report",
        data=csv,
        file_name="student_performance_report.csv",
        mime="text/csv"
    )

else:
    st.warning("No students found for this filter.")
