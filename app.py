import os,read_conf
from flask import Flask,render_template,request,redirect,url_for,session

app = Flask(__name__)

# Default page is to load basic html file for the user upload the switch configuration file
@app.route('/')
def read():
    return render_template("basic.html")

## After uploading the SW file, it will run the function to read the file
@app.route('/Result_config_checker', methods=["POST", "GET"])
def result():
    ## Capture the Catalyst configuration file
    uploaded_file = request.files['file']
    ## Uploading the Catalyst file to the files folder under static
    dir = os.path.join(os.getcwd(),"static/files")
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(dir,uploaded_file.filename))
    sw_file = os.path.join(dir,uploaded_file.filename)

    # Run the function in read_conf to get the list of features configured on the switch (supported and not)
    the_list,unsupported_features,More_info = read_conf.read.Checking_featuers(sw_file)

    can_list =[]
    not_list = {}
    more = {}

    # Go through the outcome from the read_conf functions and split the supported and unsupported features as well as the supported links
    x = 0
    while x < (len(the_list)-1):
        if the_list[x] not in unsupported_features.keys():
            can_list.append(the_list[x])
            x +=1
        if the_list[x] in unsupported_features.keys():
            not_list[the_list[x]] = unsupported_features[the_list[x]]
            more[the_list[x]] = More_info[the_list[x]]
            x +=1
    # Returning to the user check_comp html page with the variables of the features supported and not as wel ass the URLs attached to each unsupported features
    return render_template("check_comp.html", can_list =can_list, not_list=not_list, more=more)

if __name__ == '__main__':
    app.run(port=5000)
