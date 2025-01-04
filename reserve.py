# from werkzeug.utils import secure_filename
# from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import requests
# import pandas as pd
# import random
# import pymongo
# from pymongo import MongoClient
# import os

# app = Flask(__name__)
# app.secret_key = 'your_secret_key' 

# random_number = random.randint(100000, 999999)

# base_url = 'https://erpv14.electrolabgroup.com/'
# endpoint = 'api/resource/Job Applicant'
# url = base_url + endpoint

# headers = {
#     'Authorization': 'token 3ee8d03949516d0:6baa361266cf807',
#     'Content-Type': 'application/json'
# }

# client = MongoClient('mongodb://localhost:27017/')
# db = client['job_applications']  # Database
# collection = db['applicants']  # Collection for storing applicant details

# # Function to save data in MongoDB
# def save_to_mongo(applicant_name, job_title, resume_attachment_url):
#     applicant_data = {
#         "applicant_name": applicant_name,
#         "job_title": job_title,
#         "resume_attachment": resume_attachment_url
#     }
#     collection.insert_one(applicant_data)


# @app.route('/get_job_titles', methods=['GET'])
# def get_job_titles():
#     base_url = 'https://erpv14.electrolabgroup.com/'
#     endpoint = 'api/resource/Job Opening'
#     url = base_url + endpoint

#     params = {
#         'fields': '["name","designation","status"]',
#         'limit_start': 0, 
#         'limit_page_length': 100000000000,
#     }

#     headers = {
#         'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
#     }

#     response = requests.get(url, params=params, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         df = pd.DataFrame(data['data'])
#         df = df[df['status'] == 'Open']
#         df.rename(columns={'name': 'job_title'}, inplace=True)
#         final_df = df.drop_duplicates(subset='job_title', keep='first')
#         job_title_designation = final_df[['job_title', 'designation']].dropna().to_dict(orient='records')
#         return jsonify(job_title_designation)
#     else:
#         return jsonify({"error": "Failed to fetch data from API"}), 500


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/submit', methods=['POST'])
# def submit_form():
#     try:
#         # Get general form data
#         applicant_name = request.form['applicant_name']
#         job_title = request.form['job_title']
#         email_id = request.form['email_id']
#         designation = request.form['designation']
#         phone_number = request.form['phone_number']
#         status = request.form['status']
#         country = request.form['country']
#         cover_letter = request.form['cover_letter']
#         lower_range = request.form['lower_range']
#         upper_range = request.form['upper_range']
#         resume_link = request.form['resume_link']

#         resume_attachment = request.files['resume_attachment']

#         filename = secure_filename(resume_attachment.filename)
#         file_url = f"/private/files/{filename.split('.')[0]}_{random_number}.{filename.split('.')[-1]}"

#         # Get custom work experience data (from custom_external_work_history table)
#         company_name = request.form.getlist('company_name[]')
#         work_designation = request.form.getlist('designation[]')
#         salary = request.form.getlist('salary[]')
#         address = request.form.getlist('address[]')
#         contact = request.form.getlist('contact[]')
#         custom_from = request.form.getlist('custom_from[]')
#         custom_to = request.form.getlist('custom_to[]')
#         total_experience = request.form.getlist('total_experience[]')

#         # Prepare work experience data
#         work_experience_data = []
#         for i in range(len(company_name)):
#             work_experience_data.append({
#                 "company_name": company_name[i],
#                 "designation": work_designation[i],
#                 "salary": salary[i],
#                 "address": address[i],
#                 "contact": contact[i],
#                 "custom_from": custom_from[i],
#                 "custom_to": custom_to[i],
#                 "total_experience": total_experience[i]
#             })

#         # Get academic details (from custom_education table)
#         school_univ = request.form.getlist('school_univ[]')
#         qualification = request.form.getlist('qualification[]')
#         level = request.form.getlist('level[]')
#         year_of_passing = request.form.getlist('year_of_passing[]')
#         class_per = request.form.getlist('class_per[]')
#         maj_opt_subj = request.form.getlist('maj_opt_subj[]')

#         # Prepare academic data
#         academic_data = []
#         for i in range(len(school_univ)):
#             academic_data.append({
#                 "school_univ": school_univ[i],
#                 "qualification": qualification[i],
#                 "level": level[i],
#                 "year_of_passing": year_of_passing[i],
#                 "class_per": class_per[i],
#                 "maj_opt_subj": maj_opt_subj[i]
#             })

#         save_to_mongo(applicant_name, job_title, file_url)


#         # Prepare the final payload
#         form_data = {
#             "applicant_name": applicant_name,
#             "job_title": job_title,
#             "email_id": email_id,
#             "designation": designation,
#             "phone_number": phone_number,
#             "status": status,
#             "country": country,
#             "cover_letter": cover_letter,
#             "lower_range": lower_range,
#             "upper_range": upper_range,
#             "resume_attachment": file_url,
#             "resume_link": resume_link,
#             "custom_education": academic_data,  # custom_education data (academic details)
#             "custom_external_work_history": work_experience_data  # custom_external_work_history data (work experience)
#         }

#         response = requests.post(url, json=form_data, headers=headers)

#         # Check response status
#         if response.status_code == 200:
#             flash('FORM SUBMITTED SUCCESSFULLY!', 'success')
#         else:
#             flash(f'Error: {response.status_code} - {response.text}', 'error')

#     except Exception as e:
#         flash(f'Error occurred: {str(e)}', 'error')

#     return redirect(url_for('home'))

# @app.route('/terms')
# def tnc():
#     return render_template('tnc.html')

# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = 8000, debug=True)