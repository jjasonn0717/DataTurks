import requests
import argparse
import json


WORKERS_PATH = "./workers/workers.json"
TAGS_PATH = "./data/milk_rule_based_attribute_types.txt"


def DataturksCreateUser(ip, email, password, firstname, secondname):
    # Login
    print("Creating User...")
    url = f"{ip}/dataturks/createUserWithPassword"

    payload = '''{
        "authType": "emailSignUp",
        "email": "%s",
        "firstName": "%s",
        "secondName": "%s"
    }''' % (email, firstname, secondname)
    headers = {
        'Content-Type': 'application/json',
        'password': password
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    cookie = json.loads(response.text.encode('utf8'))
    print("Worker:", firstname, secondname)
    print("Email:", email)
    print("Cookie:", cookie)
    print()
    return cookie


def DataturksLogin(ip, email, password):
    # Login
    print("Login...")
    url = f"{ip}/dataturks/login"

    headers = {
        'Content-Type': 'application/json',
        'email': email,
        'password': password
    }
    response = requests.request("POST", url, headers=headers)
    cookie = json.loads(response.text.encode('utf8'))
    print("Cookie:", cookie)
    print()
    return cookie


def DataturksCreateProject(ip, cookie, payload):
    # create project
    print("Creating a Project...")
    url = f"{ip}/dataturks/createProject"

    headers = {
        'Content-Type': 'application/json',
        'uid': cookie['id'],
        'token': cookie['token']
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    projectId = json.loads(response.text.encode('utf8'))
    print("Project ID:", projectId)
    print()
    return projectId['response']


def DataturksCreateVerifyProject(ip, cookie, proj_name, tags):
    payload = '''{
        "name": "%s",
        "taskType": "POS_TAGGING_GENERIC",
        "accessType" : "RESTRICTED",
        "shortDescription": "Verification Workflow",
        "description": "Check whether the pre-annotated attributes are correct or not by clicking the boxes on the left.",
        "rules" : "{\\"tags\\": \\"%s\\", \\"instructions\\": \\"Check whether the pre-annotated attributes are correct or not\\", \\"classification\\":[{\\"name\\": \\"isCorrect\\", \\"displayName\\": \\"Are the annotations on the right correct?\\", \\"classes\\": [\\"Correct\\", \\"Incorrect\\"]}]}"
    }''' % (proj_name, ",".join(tags))
    return DataturksCreateProject(ip, cookie, payload)


def DataturksCreateEditProject(ip, cookie, proj_name, tags):
    payload = '''{
        "name": "%s",
        "taskType": "POS_TAGGING_GENERIC",
        "accessType" : "RESTRICTED",
        "shortDescription": "Editing Workflow",
        "description": "Edit the pre-annotated attributes in the middle to make them correct annotations, and check whether the provided product name falls in the milk category by clicking boxes on the left.",
        "rules" : "{\\"tags\\": \\"%s\\", \\"instructions\\": \\"Edit the pre-annotated attributes on the right to make then correct annotations, and check whether the provided product name falls in the milk category\\", \\"classification\\":[{\\"name\\": \\"isMilk\\", \\"displayName\\": \\"Category\\", \\"classes\\": [\\"Milk\\", \\"not Milk\\"]}]}"
    }''' % (proj_name, ",".join(tags))
    return DataturksCreateProject(ip, cookie, payload)


def DataturksAddContributor(ip, cookie, proj_id, email):
    #http://localhost/dataturks/2c9180827813ebc501781840f3540002/addContributor?userEmail=shih-ting.lin%40instacart.com&role=CONTRIBUTOR
    # add contributor
    print("Addin a Contributor...")
    url = f"{ip}/dataturks/{proj_id}/addContributor?userEmail={email}&role=CONTRIBUTOR"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'uid': cookie['id'],
        'token': cookie['token']
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text.encode('utf8'))
    print("Adding Contributor Response:", response)
    print()
    return response


def DataturksUploadData(ip, cookie, proj_id, fn):
    # create project
    print("Uploading data...")
    url = f"{ip}/dataturks/{proj_id}/upload"

    payload = {}
    files = {
        'file': open(fn, 'rb')
    }
    headers = {
        'format': 'PRE_TAGGED_JSON',
        'itemStatus': 'preTagged',
        'uploadFormat': 'PRE_TAGGED_JSON',
        'uid': cookie['id'],
        'token': cookie['token']
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response = json.loads(response.text.encode('utf8'))
    print("Upload Response:", response)
    print()
    return response


def DataturksGetProjectDetails(ip, cookie, proj_id):
    # get project details
    print("Getting Project Details...")
    url = f"{ip}/dataturks/{proj_id}/getProjectDetails"

    payload  = {}
    headers = {
        'Content-Type': 'application/json',
        'uid': cookie['id'],
        'token': cookie['token']
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    projectDetails = json.loads(response.text.encode('utf8'))
    print("Project: ", proj_id)
    print("Details: ", projectDetails)
    print()
    return  projectDetails


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="create annotation tasks")
    parser.add_argument('--email', required=True, help="email of the worker")
    parser.add_argument('--workflow', required=True, nargs='+', choices=['verify', 'edit'], help="the annotation workflow to run")
    args = parser.parse_args()

    # get the worker profile
    with open(WORKERS_PATH) as f:
        worker_profiles = json.load(f)
        if not args.email in worker_profiles:
            print("ERROR: It seems %s is not registered" % args.email)
            exit()
        else:
            worker_profile = worker_profiles[args.email]
        assert worker_profile['email'] == args.email

    ip = "http://localhost"

    # workflow
    workflows = set(args.workflow)

    # worker profile
    email = worker_profile['email']
    password = worker_profile['password']
    firstname = worker_profile['firstname']
    secondname = worker_profile['secondname']
    worker_id = worker_profile['worker_id']

    # create user
    #cookie = DataturksLogin(IP, EMAIL, PASSWORD)
    cookie = DataturksCreateUser(ip, email, password, firstname, secondname)

    # get all attribute types
    with open(TAGS_PATH) as f:
        lines = f.readlines()
        assert len(lines) == 1
        all_tags = lines[0].split(', ')
        assert len(all_tags) == 66

    # create project and uplaod data for verification task (workflow 1)
    if 'verify' in workflows:
        verify_proj_name = f"Verification Task {worker_id+1}"
        verify_proj_id = DataturksCreateVerifyProject(ip, cookie, verify_proj_name, all_tags)

        response = DataturksUploadData(ip, cookie, verify_proj_id, "./data/milk_rule_based_annotations_100.jsonl")

    # create project and uplaod data for editing task (workflow 2)
    if 'edit' in workflows:
        edit_proj_name = f"Editing Task {worker_id+1}"
        edit_proj_id = DataturksCreateEditProject(ip, cookie, edit_proj_name, all_tags)

        response = DataturksUploadData(ip, cookie, edit_proj_id, "./data/milk_rule_based_annotations_100.jsonl")


    '''
    all_data = {
        '/Users/shih-tinglin/catalog-team/quality/names/attribute-extractor-milk/milk_rule_based_annotations_2.jsonl': {
            'project_id': None,
            'done': False
        },
        '/Users/shih-tinglin/catalog-team/quality/names/attribute-extractor-milk/milk_rule_based_annotations_5.jsonl': {
            'project_id': None,
            'done': False
        }
    }

    for i, fn in enumerate(all_data):
        # create project
        proj_id = DataturksCreateProject(IP, cookie, "Sample Project %d" % i)
        all_data[fn]['project_id'] = proj_id

        # upload data
        DataturksUploadData(IP, cookie, proj_id, fn)

        print("\n\n")


    for i in range(3):
        for fn in all_data:
            # get project details
            proj_details = DataturksGetProjectDetails(IP, cookie, all_data[fn]['project_id'])

            print("\n")
    '''
