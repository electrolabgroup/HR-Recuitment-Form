from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import requests
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Define the API endpoint and token
base_url = 'https://erpv14.electrolabgroup.com/'
endpoint = 'api/resource/Job Applicant'
url = base_url + endpoint

# Define headers for the API request
headers = {
    'Authorization': 'token 3ee8d03949516d0:6baa361266cf807',
    'Content-Type': 'application/json'
}

@app.route('/get_job_titles', methods=['GET'])
def get_job_titles():
    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Job Opening'
    url = base_url + endpoint

    params = {
        'fields': '["name","designation","status"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'])
        df = df[df['status'] == 'Open']
        df.rename(columns={'name': 'job_title'}, inplace=True)
        final_df = df.drop_duplicates(subset='job_title', keep='first')
        job_title_designation = final_df[['job_title', 'designation']].dropna().to_dict(orient='records')
        return jsonify(job_title_designation)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    applicant_name = request.form['applicant_name']
    job_title = request.form['job_title']
    email_id = request.form['email_id']
    designation = request.form['designation']
    phone_number = request.form['phone_number']
    status = request.form['status']
    country = request.form['country']
    cover_letter = request.form['cover_letter']
    lower_range = request.form['lower_range']
    upper_range = request.form['upper_range']
    resume_attachment = request.form['resume_attachment']
    resume_link = request.form['resume_link']

    # Prepare the data to be sent to the API  
    form_data = {
        "applicant_name": applicant_name,
        "job_title": job_title,
        "email_id": email_id,
        "designation": designation,
        "phone_number": phone_number,
        "status": status,
        "country": country,
        "cover_letter": cover_letter,
        "lower_range": lower_range,
        "upper_range": upper_range,
        "resume_attachment": resume_attachment,
        "resume_link": resume_link
    }

    # Send POST request to the API   
    response = requests.post(url, json=form_data, headers=headers)

    # Check response status
    if response.status_code == 200:
        flash('FORM SUBMITTED SUCCESSFULLY !', 'success')
    else:
        flash('Error: Please check the form and try again')

    # Redirect back to the home page or success page
    return redirect(url_for('home'))

@app.route('/terms')
def tnc():
    return render_template('tnc.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug=True)