# -*- coding: utf-8 -*-
"""Copy of Untitled39.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/110U3_5eAYnvhup8joC4hgjaEki_FhC7o
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "/content/Enrollments_Dataset.xlsx"
df = pd.read_excel(file_path)
print(df.head())

print(df.info())

print(df.isnull().sum())

print(df['Timezone'].unique())
print(df['Teacher Name'].unique())

df = df.drop(columns=['Unnamed: 35', 'Unnamed: 36', 'Unnamed: 37'], errors='ignore')

categorical_columns = ['Parent name', 'Child Name', 'Teacher Name', 'Communication Preference',
                       'Type', 'Class name', 'Country', 'Region', 'City', 'Timezone']

for col in categorical_columns:
    df[col] = df[col].fillna("Not Provided")

numerical_columns = ['Age', 'Score - Concept', 'Score - Interesting', 'Score - Another class', 'Final score']

for col in numerical_columns:
    df[col] = df[col].fillna(df[col].median())

timezone_mapping = {-5: "EST", 3: "EAT", 4: "AST"}
df['Timezone'] = df['Timezone'].replace(timezone_mapping)

df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Timestamp'] = df['Timestamp'].fillna(df['Date'])

df = df.drop_duplicates()
print(df.info())

print(df.isnull().sum())

df['Yes'].fillna(df['Yes'].mean(), inplace=True)
df['Maybe'].fillna(df['Maybe'].mean(), inplace=True)
df['No'].fillna(df['No'].mean(), inplace=True)
df['Score - Concept'].fillna(df['Score - Concept'].mean(), inplace=True)
df['Score - Interesting'].fillna(df['Score - Interesting'].mean(), inplace=True)
df['Score - Another class'].fillna(df['Score - Another class'].mean(), inplace=True)

df['Source'].fillna('Unknown', inplace=True)
df['Source details'].fillna('Unknown', inplace=True)
df['Phase Mapping'].fillna('Unknown', inplace=True)
df['Topics'].fillna('Unknown', inplace=True)
df['Attended?'].fillna('Unknown', inplace=True)
df['Concepts'].fillna('Unknown', inplace=True)
df['Interesting'].fillna('Unknown', inplace=True)
df['Another class'].fillna('Unknown', inplace=True)
df.drop(['Want another slot', 'Class Part Number', 'ID for sequential classes'], axis=1, inplace=True)
df.dropna(subset=['Class name', 'Teacher Name', 'Date'], inplace=True)

print(df.isnull().sum())

cleaned_file_path = 'cleaned_dataset.xlsx'
df.to_excel(cleaned_file_path, index=False, engine='openpyxl')
print(f"Cleaned dataset saved to {cleaned_file_path}")

attendance_counts = df.groupby(['Timezone', 'Start time (in PST)'])['Attended?'].apply(lambda x: (x == "Yes").sum())
attendance_counts = attendance_counts.sort_values(ascending=False)
print(attendance_counts.head(10))

top_timezones = attendance_counts.groupby('Timezone').sum().sort_values(ascending=False)
print("Top Time Zones for Scheduling Classes:")
print(top_timezones)

top_timings = attendance_counts.groupby('Start time (in PST)').sum().sort_values(ascending=False)
print("Top Timings for Scheduling Classes:")
print(top_timings)



teacher_scores = df.groupby('Teacher Name')['Final score'].mean().sort_values(ascending=False)
print("Best Teachers:")
print(teacher_scores.head(5))

class_scores = df.groupby('Class name')['Final score'].mean().sort_values(ascending=False)
print("Best Classes:")
print(class_scores.head(5))

teacher_class_scores = df.groupby(['Teacher Name', 'Class name'])['Final score'].mean().sort_values(ascending=False)
print("Best Teacher-Class Combinations:")
print(teacher_class_scores.head(10))

attendance_counts.to_csv("attendance_counts.csv")
teacher_scores.to_csv("teacher_scores.csv")
class_scores.to_csv("class_scores.csv")
teacher_class_scores.to_csv("teacher_class_scores.csv")
print("Insights have been saved to CSV files.")

print(df.columns)

teacher_df = df.groupby('Teacher Name')['Final score'].mean().reset_index()
teacher_df = teacher_df.sort_values(by='Final score', ascending=False)
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 12))
plt.barh(teacher_df['Teacher Name'], teacher_df['Final score'], color='skyblue')
plt.xlabel('Average Final Score')
plt.ylabel('Teacher Name')
plt.title('Average Final Score by Teacher')
plt.gca().invert_yaxis()  # Invert y-axis for better readability
plt.show()

class_df = df.groupby('Class name')['Final score'].mean().reset_index()
class_df = class_df.sort_values(by='Final score', ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x='Class name', y='Final score', data=class_df, palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Class Name')
plt.ylabel('Average Final Score')
plt.title('Top 10 Classes by Average Final Score')
plt.show()

if 'Another class' in df.columns and 'Teacher Name' in df.columns:
    teacher_booking_counts = df[df['Another class'] == 'Yes'].groupby('Teacher Name').size().sort_values(ascending=False)

    print("Teachers with most 'Another class' bookings:")
    print(teacher_booking_counts)
else:
    print("'Another class' or 'Teacher Name' column not found in the DataFrame.")

if 'Another class' in df.columns and 'Class name' in df.columns:
    course_booking_counts = df[df['Another class'] == 'Yes'].groupby('Class name').size().sort_values(ascending=False)
    print("Courses with most 'Another class' bookings:")
    print(course_booking_counts)
else:
    print("'Another class' or 'Class name' column not found in the DataFrame.")

if 'Another class' in df.columns and 'Class name' in df.columns:
    course_booking_counts = df[df['Another class'] == 'Maybe'].groupby('Class name').size().sort_values(ascending=False)
    print("might be an Another class' bookings:")
    print(course_booking_counts)
else:
    print("'Another class' or 'Class name' column not found in the DataFrame.")

if 'Interesting' in df.columns and 'Teacher Name' in df.columns:
    teacher_interest_counts = df[df['Interesting'] == 'Yes'].groupby('Teacher Name').size().sort_values(ascending=False)
    print("Teachers with the most 'Interesting' responses:")
    print(teacher_interest_counts)
else:
    print("'Interesting' or 'Teacher Name' column not found in the DataFrame.")

if 'Interesting' in df.columns and 'Class name' in df.columns:
    course_interest_counts = df[df['Interesting'] == 'Yes'].groupby('Class name').size().sort_values(ascending=False)
    print("Courses with the most 'Interesting' responses:")
    print(course_interest_counts)
else:
    print("'Interesting' or 'Class name' column not found in the DataFrame.")

interesting_courses = df[df['Interesting'] == 'Yes']['Class name'].value_counts()
print("Courses found interesting:")
print(interesting_courses)

rebooked_courses = df[df['Another class'] == 'Yes']['Class name'].value_counts()
print("\nCourses rebooked the most:")
print(rebooked_courses)

not_rebooked_courses = df[df['Another class'] == 'No']['Class name'].value_counts()
print("\nCourses not rebooked:")
print(not_rebooked_courses)

