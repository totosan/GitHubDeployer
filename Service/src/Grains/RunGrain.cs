using System.Text;
using System.Text.Json;
using GitHubActions.Gates.Framework.Clients;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Orleans.Runtime;
using Orleans.Reminders;
using System.Net;
using Deployer.Callbacks.CustomProtection;
using System.Net.Http.Headers;

public class RunGrain : IGrain, IGrainBase, IRunGrain
{
    IPersistentState<DeploymentStatusCallback> _state;
    private int _timeOut;
    private string? _token;
    private GitHubAppClient _client;
    private readonly ILogger _logger;
    private IGrainReminder _reminder;

    public IGrainContext GrainContext { get; }

    public RunGrain(IGrainContext grainContext, [PersistentState("wfStore", "wfStore")] IPersistentState<DeploymentStatusCallback> state, IConfiguration config, ILogger logger)
    {
        _state = state;
        var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
        _timeOut = Convert.ToInt32(config["GHAPP_TIMEOUT"]);
        _token = config["TOKEN"];
        _client = new GitHubAppClient(installationId, logger, config);
        _logger = logger;
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
        var octo = await _client.GetOCtokit();
        var run = await octo.Actions.Workflows.Runs.Get(_state.State.repository?.owner?.login, _state.State.repository?.name, _state.State.workflow_run.id);
        if (run != null)
        {
            _state.State.deployment_status.state = run.Status.ToString();
            return run.Status.ToString();
        }
        else
        {
            // handle the case where run is null
            return "Run is null";
        }
    }
    public async Task ApproveRun()
    {
        await this.GetApprovalState();
        Console.WriteLine($"Try to approve run. Current runs state is {_state.State.deployment_status.state}");
        await ReviewDeployment(Octokit.PendingDeploymentReviewState.Approved, "Approved");
    }

    public async Task RejectRun()
    {
        await ReviewDeployment(Octokit.PendingDeploymentReviewState.Rejected, "Rejected");
    }

    /// <summary>
    /// Reviews the deployment with the specified state and comment.
    /// </summary>
    /// <param name="state">The state of the deployment review.</param>
    /// <param name="comment">The comment for the deployment review.</param>
    /// <returns>A task that represents the asynchronous operation.</returns>
    private async Task ReviewDeployment(Octokit.PendingDeploymentReviewState state, string comment)
    {
        _logger.LogInformation($"ReviewDeployment to: {state}");
        var octo = await _client.GetOCtokit();
        var callbackUrl_pendings = new Uri(_state.State.workflow_run.url + "/pending_deployments");

        var pending = await octo.Connection.Get<PendingRun[]>(callbackUrl_pendings, TimeSpan.FromSeconds(30));
        if (pending.Body.Any())
        {
            var environment_id = pending.Body[0].environment.id;
            var environmentName = pending.Body[0].environment.name;
            _logger.LogInformation($"ReviewDeployment to: {state} for environment {environmentName}");

            try
            {
                _logger.LogInformation($"ReviewDeployment to: {state} for environment {environmentName} with comment {comment}");
                string callbackUrl_custom_deployment = $"{_state.State.workflow_run.url}/deployment_protection_rule";
                _logger.LogInformation($"ReviewDeployment to: {state} for environment {environmentName} with url {callbackUrl_custom_deployment}");
                var approvalResponse = await _client.SetApprovalDecision(callbackUrl_custom_deployment,
                                                                            state.ToString().ToLower(),
                                                                            environmentName,
                                                                            comment);
                if (approvalResponse == System.Net.HttpStatusCode.OK)
                {
                    _logger.LogInformation($"Successfully set approval decision to {state} for environment {environmentName}");
                    _state.State.deployment_status.state = "rejected";
                    await _state.WriteStateAsync();
                }
            }
            catch (Octokit.ApiValidationException ex)
            {
                _logger.LogError(ex, $"Failed to set approval decision to {state} for environment {environmentName} with call to {callbackUrl_pendings.ToString()}");

                _logger.LogInformation($"Calling {callbackUrl_pendings.ToString()} with env: {environment_id} and state: {state.ToString().ToLower()}");

            }
        }
    }

    public async Task SendApprovalDecisionAsync(string state, string comment)
    {
        var callbackUrl_pendings = new Uri(_state.State.workflow_run.url + "/pending_deployments");

        var octo = await _client.GetOCtokit();
        var pending = await octo.Connection.Get<PendingRun[]>(callbackUrl_pendings, TimeSpan.FromSeconds(30));
        if (pending.Body.Any())
        {
            var environment_id = pending.Body[0].environment.id;
            var environmentName = pending.Body[0].environment.name;
            _logger.LogInformation($"ReviewDeployment to: {state} for environment {environmentName}");
            var token = _token;
            var environment_ids = new List<long> { environment_id };

            var httpClient = new HttpClient();

            httpClient.DefaultRequestHeaders.Add("Authorization", "token " + token);
            httpClient.DefaultRequestHeaders.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/vnd.github+json"));
            httpClient.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("product", "1")); //required by GitHub API

            var reviewState = new { state, comment, environment_ids };
            var json = JsonSerializer.Serialize(reviewState);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await httpClient.PostAsync(callbackUrl_pendings, content);
            var responseContent = await response.Content.ReadAsStringAsync();
            if (responseContent != null)
                Console.WriteLine(responseContent);

        }
        else
        {
            Console.WriteLine("No pending deployments found");
        }
    }

    public async Task CancelRun()
    {
        var octo = await _client.GetOCtokit();
        await octo.Actions.Workflows.Runs.Cancel(_state.State.repository.owner.login, _state.State.repository.name, _state.State.workflow_run.id);
        await this.UnregisterReminder(_reminder);
        _state.State = null;
        await _state.WriteStateAsync();
        return;
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
            var payload = JsonSerializer.Deserialize<DeploymentStatusCallback>(run);
            _state.State = payload;
            await _state.WriteStateAsync();

            if (_reminder == null)
                _reminder = await this.RegisterOrUpdateReminder(this.GetPrimaryKeyString(), TimeSpan.FromMilliseconds(-1), TimeSpan.FromMinutes(_timeOut));
        }
    }

    public async Task ReceiveReminder(string reminderName, TickStatus status)
    {
        if (_state.State == null)
        {
            await CleanupActor();
            return;
        }
        var approvalState = await this.GetApprovalState();
        if (approvalState.ToLower() == "completed")
        {
            await CleanupActor();
            return;
        }
        Console.WriteLine($"Reminder to approve run {status.CurrentTickTime}");
        await ApproveRun();
    }

    public async Task CancelReminder()
    {
        if (_reminder == null)
            return;
        await this.UnregisterReminder(_reminder);
        _reminder = null;
    }
    private async Task CleanupActor()
    {
        await this.CancelReminder();
        _state.State = null;
        await _state.ClearStateAsync();
    }
}