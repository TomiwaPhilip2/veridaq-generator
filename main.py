from flask import Flask
from docVerification import generateDocVerification
from individualReference import generateIndividualReference
from studentStatus import generateStudentStatus
from workReference import generateWorkReference

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

if __name__ == '__main__':
    app.run(debug=True)
