using Orleans.Hosting;
using Orleans.Configuration;

var builder = WebApplication.CreateBuilder(args);


// Configure the HTTP request pipeline.
if (builder.Environment.IsDevelopment())
{
    builder.Host.UseOrleans(siloBuilder =>
    {
        siloBuilder
            .UseLocalhostClustering()
            .Configure<ClusterOptions>(options =>
            {
                options.ClusterId = "DeployerApp";
                options.ServiceId = "Terminator";
            });
        siloBuilder.AddMemoryGrainStorage("wfStore");
    }).ConfigureLogging(logging =>
    {
       logging.AddConsole();
       logging.SetMinimumLevel(LogLevel.Warning);
    });
}
var app = builder.Build();
app.MapGet("/", () => "I am Deployer Silo!");
app.MapPost("/payload", (HttpContext context) =>
{
    
});
app.Run();
