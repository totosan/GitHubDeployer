public interface IRunGrain : Orleans.IGrainWithIntegerKey, IRemindable
{
    /*
    add following methods:
    GetStatus
    cancelRun
    approveRun
    rejectRun
    */
    Task<string> GetStatus();
    Task CancelReminder();
    Task CancelRun();
    Task ApproveRun();
    Task RejectRun();
    Task SetRun(string? run);
    Task<string> GetApprovalState();
    Task SendApprovalDecisionAsync(string state, string comment);
}