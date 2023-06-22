using System.Text;
using System.Text.Json;
using GitHubActions.Gates.Framework.Clients;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Orleans.Runtime;
using Orleans.Reminders;

public class RunGrain : IGrain, IGrainBase, IRunGrain
{
    IPersistentState<GitHubRunCallback> _state;
    private GitHubAppClient _client;
    private IGrainReminder _reminder;

    public IGrainContext GrainContext { get; }

    public RunGrain(IGrainContext grainContext ,[PersistentState("wfStore", "wfStore")] IPersistentState<GitHubRunCallback> state, IConfiguration config, ILogger logger)
    {
        _state = state;
        var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
        _client = new GitHubAppClient(installationId, logger, config);
        this.GrainContext = grainContext;
    }

    public Task OnActivateAsync(CancellationToken cancellationToken)
    {
        return Task.CompletedTask;
    }

    public Task OnDeactivateAsync(DeactivationReason reason, CancellationToken token)
    {
        return Task.CompletedTask;
    }


    public async Task<string> GetApprovalState()
    {
        // var octo = await _client.GetOCtokit();
        // var state = await octo.(_state.State.repository.owner.login, _state.State.repository.name, _state.State.workflow_run.id);
        // var status = state.Status;
        // return status;

        return "";
    }
    public async Task ApproveRun()
    {
        var environmentName = _state.State.deployment_status.environment;
        var octo = await _client.SetApprovalDecision($"{_state.State.workflow_run.url}/deployment_protection_rule","approved", environmentName ,"Looks good to mee!");
        if (octo == System.Net.HttpStatusCode.OK)
        {
            _state.State.deployment_status.state = "approved";
            await _state.WriteStateAsync();
        }
    }
    public async Task RejectRun()
    {
        var environmentName = _state.State.deployment_status.environment;
        var octo = await _client.SetApprovalDecision($"{_state.State.workflow_run.url}/deployment_protection_rule","rejected", environmentName ,"Health state is not ok!");
        if (octo == System.Net.HttpStatusCode.OK)
        {
            _state.State.deployment_status.state = "rejected";
            await _state.WriteStateAsync();
        }
        await CancelReminder();
    }
    public async Task CancelRun()
    {
        var octo = await _client.GetOCtokit();
        await octo.Actions.Workflows.Runs.Cancel(_state.State.repository.owner.login, _state.State.repository.name, _state.State.workflow_run.id);
        await this.UnregisterReminder(_reminder);

        return;
    }

    public async Task CancelReminder(){
        if(_reminder == null)
            return;
        await this.UnregisterReminder(_reminder);
        _reminder = null;
    }

    public Task<string> GetStatus()
    {
        var stateOfRun = _state.State.deployment_status?.state;
        return Task.FromResult(stateOfRun);
    }

    public async Task SetRun(string? run)
    {
        if (run != null)
        {
            var payload = JsonSerializer.Deserialize<GitHubRunCallback>(run);
            _state.State = payload;
            await _state.WriteStateAsync();
            _reminder = await this.RegisterOrUpdateReminder(this.GetPrimaryKeyString(), TimeSpan.FromSeconds(30), TimeSpan.FromMinutes(1));
        }
    }

    public async Task ReceiveReminder(string reminderName, TickStatus status)
    {
        Console.WriteLine($"Reminder to approve run {status.CurrentTickTime}");
        //await ApproveRun();
    }

    //get reminder status
    public async Task<string> GetReminderStatus()
    {
        var reminderStatus = await this.GetReminder(_reminder.ReminderName);
        return "";
    }
}