
public interface IDeployerGrain : IGrainWithIntegerKey
{
    Task<Workflow> GetWorkflow();
    Task SetWorkflow(Workflow workflow);
    Task<object> StartWorkflow(Workflow workflow);
}