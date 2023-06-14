using Orleans.Runtime;
public class DeployerGrain : IGrain, IDeployerGrain
{
    IPersistentState<Workflow> _wf;
    public DeployerGrain([PersistentState("wf", "wfStore")] IPersistentState<Workflow> wf)
    {
        _wf = wf;
    }
    public Task<Workflow> GetWorkflow()
    {
        return Task.FromResult(_wf.State);
    }

    public Task SetWorkflow(Workflow workflow)
    {
        _wf.State = workflow;
        return _wf.WriteStateAsync();
    }

    public Task<object> StartWorkflow(Workflow workflow)
    {
        if (workflow.isTerminator)
        {
            return Task.FromResult<object>(new TerminatorGrain());
        }
        else
        {
            return Task.FromResult<object>(new DeployerGrain());
        }
    }
}
