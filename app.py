from flask import Flask, render_template, request, session
import os
import subprocess  # Add subprocess to run InputPreprocessing

app = Flask(__name__, static_folder="UserInterface/static", template_folder="UserInterface")
# Explicitly set the template folder
app.secret_key = "secret_key"  # Required for session management

# Define upload folders
CV_FOLDER = os.path.join('Public', 'InputFolder', 'CVInputFolder')
JOB_FOLDER = os.path.join('Public', 'InputFolder', 'JobInputFolder')
LETTER_FOLDER = os.path.join('Public', 'InputFolder', 'LetterFolder')
OUTPUT_FOLDER = os.path.join('Public', 'InputFolder', 'Preprocessed')

# Ensure the folders exist
os.makedirs(CV_FOLDER, exist_ok=True)
os.makedirs(JOB_FOLDER, exist_ok=True)
os.makedirs(LETTER_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    missing_files = {'cv_file': False, 'job_file': False, 'letter_file': False}
    success = False  # To indicate whether files were successfully saved

    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'submit':
            # Check if all files are uploaded
            if not session.get('cv_file'):
                missing_files['cv_file'] = True
            if not session.get('job_file'):
                missing_files['job_file'] = True
            if not session.get('letter_file'):
                missing_files['letter_file'] = True

            if all(session.get(key) for key in ['cv_file', 'job_file', 'letter_file']):
                # Clear session and set success flag
                session.pop('cv_file', None)
                session.pop('job_file', None)
                session.pop('letter_file', None)
                success = True

                # Run InputPreprocessing script after saving files
                try:
                    subprocess.run(
                        ['python', 'InputPreprocessing.py'], 
                        check=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    print("InputPreprocessing executed successfully.")
                except subprocess.CalledProcessError as e:
                    print("Error while executing InputPreprocessing.py:")
                    print(e.stderr)

            return render_template('index.html',
                                   cv_file=None,
                                   job_file=None,
                                   letter_file=None,
                                   missing_files=missing_files,
                                   success=success)

        else:
            # Handle file uploads and directly save to final destination
            if 'cv_file' in request.files:
                cv_file = request.files['cv_file']
                if cv_file.filename.endswith('.pdf'):
                    file_path = os.path.join(CV_FOLDER, cv_file.filename)
                    cv_file.save(file_path)
                    session['cv_file'] = file_path
                else:
                    return "Only PDF files are allowed for CV.", 400

            if 'job_file' in request.files:
                job_file = request.files['job_file']
                if job_file.filename.endswith('.pdf'):
                    file_path = os.path.join(JOB_FOLDER, job_file.filename)
                    job_file.save(file_path)
                    session['job_file'] = file_path
                else:
                    return "Only PDF files are allowed for Job Description.", 400

            if 'letter_file' in request.files:
                letter_file = request.files['letter_file']
                if letter_file.filename.endswith('.pdf'):
                    file_path = os.path.join(LETTER_FOLDER, letter_file.filename)
                    letter_file.save(file_path)
                    session['letter_file'] = file_path
                else:
                    return "Only PDF files are allowed for Cover Letter Description.", 400

    return render_template('index.html',
                           cv_file=session.get('cv_file'),
                           job_file=session.get('job_file'),
                           letter_file=session.get('letter_file'),
                           missing_files=missing_files,
                           success=False)


if __name__ == '__main__':
    app.run(debug=True)
