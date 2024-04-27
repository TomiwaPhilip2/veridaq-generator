from flask import Flask
from veridaqRequests.alumniReference import generateAlumniReference
from veridaqRequests.docVerification import generateDocVerification
from veridaqRequests.individualReference import generateIndividualReference
from veridaqRequests.memberReference import generateMemberReference
from veridaqRequests.studentStatus import generateStudentStatus
from veridaqRequests.workReference import generateWorkReference

app = Flask(__name__)

@app.route('/doc-verification',methods=["GET"])
def getDoc():
    return generateDocVerification()

@app.route('/work-reference', methods=["GET"])
def getDoc2():
    return generateWorkReference()

@app.route('/student-status', methods=["GET"])
def getDoc3():
    return generateStudentStatus()

@app.route('/individual-reference', methods=["GET"])
def getDoc4():
    return generateIndividualReference()

@app.route('/member-reference', methods=["GET"])
def getDoc5():
    return generateMemberReference()

@app.route('/alumni-reference', methods=["GET"])
def getDoc6():
    return generateAlumniReference()

if __name__ == '__main__':
    app.run(debug=True)
