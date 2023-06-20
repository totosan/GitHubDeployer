using Microsoft.Extensions.Configuration;

public static class Config
    {
        public const string WEBHOOKSECRETNAME = "GHAPP_WEBHOOKSECRET";
        public const string GHAPPPEMCERTIFICATENAME = "GHAPP_PEMCERTIFICATE";
        public const string GHAPPID = "GHAPP_ID";
        public static IConfiguration GetConfig()
        {
            return new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();
        }
    }

