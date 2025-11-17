import azure.functions as func
import qsharp
import os
import ast
import azure.quantum
from azure.identity import ManagedIdentityCredential
from scipy.optimize import minimize

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def calcExpVal(results):
    expVal = 0.0  

    for cut_s, prob in results.items():

        # convert cut to a list
        cut = ast.literal_eval(cut_s)

        # format cut into a format suitable to calculate costs 
        formatted_cut = [-1 if node == 0 else node for node in cut] 

        # calculate costs of the cut with cost function of the graph
        cost = (
            formatted_cut[0]*formatted_cut[1] +
            formatted_cut[0]*formatted_cut[5] +
            formatted_cut[1]*formatted_cut[2] +
            formatted_cut[1]*formatted_cut[5] +
            formatted_cut[2]*formatted_cut[3] +
            formatted_cut[2]*formatted_cut[4] +
            formatted_cut[3]*formatted_cut[4] +
            formatted_cut[4]*formatted_cut[5] 
        )
        
        # calculate the expectation value
        expVal += cost * prob
    return expVal


@app.route(route="runQAOA")
def runQAOA(req: func.HttpRequest) -> func.HttpResponse:

    # init Q# project 
    qsharp.init(project_root='.', target_profile=qsharp.TargetProfile.Base)

    # get managed identity credential
    mgcredential = ManagedIdentityCredential()

    # connect to workspace
    workspace = azure.quantum.Workspace(
        subscription_id = os.environ['subscriptionId'],
        name = os.environ['workspaceName'],
        resource_group = os.environ['resourceGroupName'],
        location = os.environ['location'],
        credential = mgcredential
        )

    # specify target
    MyTarget = workspace.get_targets(os.environ['target'])

    # run qaoa circuit
    def QAOAiteration(params):
        
        # cast gamma, beta as python float to ensure q# compatibility 
        gamma = float(params[0])
        beta = float(params[1])

        # submit job
        job = MyTarget.submit(qsharp.compile(
            f"QuantumLibrary.runQAOA({ gamma , beta })"), "single QAOA run", shots=500)
        
        # wait for completion 
        job.wait_until_completed() 

        # get results
        results = job.get_results()

        # calculate expectation value
        expV = calcExpVal(results)

        return expV

    # submit jobs in a session
    with MyTarget.open_session(name="QAOA session") as session:
 
        # optimize expectation value
        res = minimize(QAOAiteration, [1.0, 1.0], method='COBYLA')

        # cast gamma, beta as python float to ensure q# compatibility
        final_gamma = float(res.x[0])
        final_beta = float(res.x[1])

        # determine soultion with optimized gamma and beta
        job = MyTarget.submit(qsharp.compile(
            f"QuantumLibrary.runQAOA({ final_gamma , final_beta })"), "last run", shots=500)

    # get last job in session
    jobs_in_session = session.list_jobs()
    last_job = jobs_in_session[-1]

    return func.HttpResponse(f"Hello, results are stored under job-id: {last_job.id} ")





