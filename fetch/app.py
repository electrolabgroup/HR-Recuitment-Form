from flask import Flask, render_template, send_file, make_response, abort
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId  # Import ObjectId for MongoDB
import io

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['job_applications']
fs = GridFS(db)
collection = db['applicants']
@app.route('/')
def index():
    # Fetch all applicants data from MongoDB
    applicants = collection.find()

    # Prepare data to display on the webpage
    applicants_data = []
    for applicant in applicants:
        applicant_info = {
            "applicant_name": applicant.get("applicant_name"),
            "job_title": applicant.get("job_title"),
            "resume_url": None,
            "resume_attachment" : applicant.get("resume_attachment")
        }

        # Print applicant data to debug
        print(f"Applicant Data: {applicant}")  # Debugging line to print the applicant's full data

        # Check if resume_attachment_id exists
        if "resume_attachment_id" in applicant:
            resume_id = applicant["resume_attachment_id"]
            applicant_info["resume_url"] = f"/view/{str(resume_id)}"  # Convert ObjectId to string for the URL

        applicants_data.append(applicant_info)

    return render_template('index.html', applicants=applicants_data)



@app.route('/view/<resume_id>')
def view_resume(resume_id):
    try:
        # Convert resume_id from string to ObjectId
        file_id = ObjectId(resume_id)
        
        # Fetch the file from GridFS
        file = fs.get(file_id)
        
        # Prepare the response with the file's content
        response = make_response(file.read())
        
        # Set appropriate content type (PDF in this case)
        response.headers['Content-Type'] = 'application/pdf'
        
        # Set the filename in the response headers
        response.headers['Content-Disposition'] = f'inline; filename={file.filename}'
        
        return response
    except Exception as e:
        return f"Error occurred while fetching file: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
