public interface IRunGrain : Orleans.IGrainWithIntegerKey
{
    /*
    add following methods:
    GetStatus
    cancelRun
    approveRun
    rejectRun
    */
    Task<string> GetStatus();
    Task CancelRun();
    Task ApproveRun();
    Task RejectRun();
    Task<string> GetApprovalState();
    Task SetRun(string? run);
}