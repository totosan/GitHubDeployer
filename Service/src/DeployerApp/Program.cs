/* This is a GitHub App, containing multiple APIs for controling GitHub Repo REST Calls
    - Start a Workflow
    - Get all running Workflows
    - Cancel a run
    - Approve a run
    - Reject a run
*/
using Orleans;

var builder = WebApplication.CreateBuilder(args);

// Configure the HTTP request pipeline.
if (!builder.Environment.IsDevelopment())
{
    builder.Host.UseOrleansClient(client =>{
        client.UseLocalhostClustering();
    });
}
// add abillity to use swagger and swaggerui
builder.Services
    .AddEndpointsApiExplorer()
    .AddSwaggerGen();

var app = builder.Build();
app.UseSwagger().UseSwaggerUI();


app.MapGet("/", () => "I am Deployer App!");

// Start a Workflow
app.MapPost("/start", async (HttpContext context) => {
    var workflow = await context.Request.ReadFromJsonAsync<Workflow>();
    var client = context.RequestServices.GetRequiredService<IClusterClient>();
    var deployer = client.GetGrain<IDeployerGrain>(0);
    var result = await deployer.StartWorkflow(workflow);
    await context.Response.WriteAsJsonAsync(result);
});

app.Run();
