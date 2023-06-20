/* This is a GitHub App, containing multiple APIs for controling GitHub Repo REST Calls
    - Start a Workflow
    - Get all running Workflows
    - Cancel a run
    - Approve a run
    - Reject a run
*/
using Orleans;
using GitHubActions.Gates.Framework.Models.WebHooks;
using Orleans.Configuration;

var builder = WebApplication.CreateBuilder(args);
IConfiguration config = null;

// Configure the HTTP request pipeline.
if (builder.Environment.IsDevelopment())
{
    builder.Host.UseOrleans(server =>
    {
        server.UseLocalhostClustering();
    });

    // add appsettings to config
    config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .Build();
}else
{
     builder.Host.UseOrleans(builder =>
    {
        var envCnn = Environment.GetEnvironmentVariable("AZURE_STORAGE_CONNECTION_STRING");

        var connectionString = envCnn ?? throw new InvalidOperationException("Missing connection string");
        builder.UseAzureStorageClustering(options =>
            options.ConfigureTableServiceClient(connectionString))
            .AddAzureTableGrainStorage("users", options => options.ConfigureTableServiceClient(connectionString));
        builder.Configure<SiloOptions>(options =>
        {
            options.SiloName = "DeployerSilo";
        });

        builder.Configure<ClusterOptions>(options =>
        {
            options.ClusterId = "deployerCluster";
            options.ServiceId = "healthCheckService";
        });
    });
}

// add abillity to use swagger and swaggerui
builder.Services
    .AddEndpointsApiExplorer()
    .AddSwaggerGen();

var app = builder.Build();
app.UseSwagger().UseSwaggerUI(c =>
 {
     c.SwaggerEndpoint("/swagger/v1/swagger.json", "My API V1");
     c.RoutePrefix = "";
 });

var logger = app.Logger;
app.MapGet("/", () => "I am Deployer App!");

app.MapGet("/all-running-runs", async () =>
{
    var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
    var client = new GitHubActions.Gates.Framework.Clients.GitHubAppClient(installationId, logger, config);
    var octo = await client.GetOCtokit();
    var runs = await octo.Actions.Workflows.Runs.List("totosan", "GitHubIntegrationDWX");
    var active = runs.WorkflowRuns.Where(x => x.Status == Octokit.WorkflowRunStatus.InProgress).ToList();
    return Results.Ok($"{active.Count}");
});

// Start a run of a workflow (SimpleWF) with octokit
app.MapPost("/start-run", async (RunCommand cmd) =>
{
    var installationId = Convert.ToInt64(config["GHAPP_INST_ID"]);
    var client = new GitHubActions.Gates.Framework.Clients.GitHubAppClient(installationId, logger, config);
    var octo = await client.GetOCtokit();

    string yamlFile = "betterCICD.yml";
    if(cmd.IsTerminator)
    {
        yamlFile = "ringbasedCICD.yml";
    }

    await octo.Actions.Workflows.CreateDispatch("totosan", "GitHubIntegrationDWX", yamlFile, new Octokit.CreateWorkflowDispatch("master"));
    return Results.Ok();
});

// Started Workflow
app.MapPost("/payload", async (HttpContext context) =>
{
    using var reader = new StreamReader(context.Request.Body);
    var body = await reader.ReadToEndAsync();
    logger.LogInformation(body);

    var payload = await context.Request.ReadFromJsonAsync<DeploymentProtectionRuleWebHook>();

    return Results.Ok(payload);
});

app.Run();
