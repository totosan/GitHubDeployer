/* This is a GitHub App, containing multiple APIs for controling GitHub Repo REST Calls
    - Start a Workflow
    - Get all running Workflows
    - Cancel a run
    - Approve a run
    - Reject a run
*/

using Deployer.Callbacks.Abstractions;
using Deployer.Callbacks.CustomProtection;
using Orleans.Configuration;
using Orleans.Hosting;
using System.Text.Json;
using System.Text.Json.Nodes;

var builder = WebApplication.CreateBuilder(args);
IConfiguration config = null;

// Configure the HTTP request pipeline.
if (builder.Environment.IsDevelopment())
{
    builder.Host.UseOrleans(server =>
    {
        server.UseLocalhostClustering();
        server.AddMemoryGrainStorage("wfStore");
        server.UseInMemoryReminderService();
    });

    // add appsettings to config
    config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .Build();
}
else
{
    builder.Host.UseOrleans(builder =>
   {
       var envCnn = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");
       Console.WriteLine(envCnn);

       var connectionString = envCnn ?? throw new InvalidOperationException("Missing connection string");
       builder.UseAzureStorageClustering(options =>
           options.ConfigureTableServiceClient(connectionString))
           .AddAzureTableGrainStorage("wfStore", options => options.ConfigureTableServiceClient(connectionString))
           .UseAzureTableReminderService(options => options.ConfigureTableServiceClient(connectionString));
       builder.Configure<SiloOptions>(options =>
       {
           options.SiloName = "DeployerSilo";
       });

       builder.Configure<ClusterOptions>(options =>
       {
           options.ClusterId = "deployerCluster";
           options.ServiceId = "healthCheckService";
       }).ConfigureLogging(logging =>
       {
           logging.AddConsole();
           logging.SetMinimumLevel(LogLevel.Error);
       });
   });

    // add appsettings to config
    config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .Build();
    builder.Services
        .Configure<IConfiguration>(config)
        .AddLogging(logging =>
        {
            logging.AddConsole();
            logging.SetMinimumLevel(LogLevel.Warning);
        });
}

// add abillity to use swagger and swaggerui
builder.Services
    .AddEndpointsApiExplorer()
    .AddSwaggerGen()
    .AddLogging(logging =>
    {
        logging.AddConsole();
        logging.SetMinimumLevel(LogLevel.Warning);
    });
//add logging configuration to the service to be injected in a grain on a silo
builder.Services.AddSingleton<ILogger>(sp =>
{
    var logger = sp.GetService<ILogger<Program>>();
    return logger;
});

var app = builder.Build();
app.UseSwagger().UseSwaggerUI(c =>
 {
     c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
     c.RoutePrefix = "";
 });

var logger = app.Logger;
app.MapGet("/", () => "Hello World!");

app.MapGet("/all-running-runs", async () =>
{
    var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
    var client = new GitHubActions.Gates.Framework.Clients.GitHubAppClient(installationId, logger, config);
    var octo = await client.GetOCtokit();
    var runs = await octo.Actions.Workflows.Runs.List("totosan", "GitHubIntegrationDWX");
    var active = runs.WorkflowRuns.Where(x => x.Status == Octokit.WorkflowRunStatus.Pending || x.Status == Octokit.WorkflowRunStatus.Waiting).ToList();
    return Results.Ok(new { RunId = active.Select(x => x.Id), RunName = active.Select(x => x.Name), RunStatus = active.Select(x => x.Status) });
});

// Start a run of a workflow (SimpleWF) with octokit
app.MapPost("/start-run", async (RunCommand cmd) =>
{
    var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
    var client = new GitHubActions.Gates.Framework.Clients.GitHubAppClient(installationId, logger, config);
    var octo = await client.GetOCtokit();

    string yamlFile = "betterCICD.yml";
    if (cmd.IsTerminator)
    {
        yamlFile = "ringbasedCICD.yml";
    }

    await octo.Actions.Workflows.CreateDispatch("totosan", "GitHubIntegrationDWX", yamlFile, new Octokit.CreateWorkflowDispatch("master"));
    return Results.Ok();
});

//approve a run
app.MapPost("/approve-run", async (IGrainFactory grainFactory, long RunId) =>
{
    var run = grainFactory.GetGrain<IRunGrain>(RunId);
    await run.SendApprovalDecisionAsync("approved", "Approved by the user");
    return Results.Accepted();
});
//reject a run
app.MapPost("/reject-run", async (IGrainFactory grainFactory, long RunId) =>
{
    var run = grainFactory.GetGrain<IRunGrain>(RunId);
    await run.SendApprovalDecisionAsync("rejected", "Rejected by the user");
    return Results.Accepted();
});

//cancel a run
app.MapPost("/cancel-run", async (IGrainFactory grainFactory, long RunId) =>
{
    var run = grainFactory.GetGrain<IRunGrain>(RunId);
    await run.CancelRun();
    return Results.Accepted();
});

app.MapGet("/cancel-reminder", async (IGrainFactory grainFactory, long RunId) =>
{
    var run = grainFactory.GetGrain<IRunGrain>(RunId);
    await run.CancelReminder();
    return Results.Accepted();
});

// Started Workflow
app.MapPost("/payload", async (HttpContext context, IGrainFactory grainFactory) =>
{

    using var reader = new StreamReader(context.Request.Body);
    var bodyString = await reader.ReadToEndAsync();
    reader.Close();

    Console.WriteLine("1####################");
    Console.WriteLine(bodyString);
    Console.WriteLine("2####################");

    DeploymentStatusCallback payload = null;
    try
    {
        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        var json = JsonObject.Parse(bodyString);
        var action = json["action"];
        if (action != null && action.ToString() == "created" && json["deployment_status"] != null)
        {
            payload = JsonSerializer.Deserialize<DeploymentStatusCallback>(bodyString, options);
        }
        else
        {
            return Results.Accepted();
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.Message);
        return Results.Accepted();
    }
    //if already a grain with the run id, just update the grain
    if (await grainFactory.GetGrain<IRunGrain>(payload.workflow_run.id).GetStatus() != null)
    {
        var current = grainFactory.GetGrain<IRunGrain>(payload.workflow_run.id);
        await current.SetRun(bodyString);
        return Results.Ok(payload.workflow_run.status);
    }
    logger.LogInformation($"This is Run {payload.workflow_run.id} payload");

    var run = grainFactory.GetGrain<IRunGrain>(payload.workflow_run.id);
    await run.SetRun(bodyString);
    return Results.Accepted();
});

app.Run();
