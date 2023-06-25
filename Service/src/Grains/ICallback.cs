namespace Deployer.Callbacks.Abstractions
{
    public interface ICallback
    {
        IWorkflowRun workflow_run { get; set; }
    }

    public interface IWorkflowRun
    {
        long id { get; set; }
        string name { get; set; }
        string node_id { get; set; }
        string head_branch { get; set; }
        string head_sha { get; set; }
        string path { get; set; }
        string display_title { get; set; }
        int run_number { get; set; }
        string @event { get; set; }
        string status { get; set; }
        object conclusion { get; set; }
        int workflow_id { get; set; }
        long check_suite_id { get; set; }
        string check_suite_node_id { get; set; }
        string url { get; set; }
        string html_url { get; set; }
        List<object> pull_requests { get; set; }
        DateTime created_at { get; set; }
        DateTime updated_at { get; set; }
        int run_attempt { get; set; }
        List<object> referenced_workflows { get; set; }
        DateTime run_started_at { get; set; }
    }
}