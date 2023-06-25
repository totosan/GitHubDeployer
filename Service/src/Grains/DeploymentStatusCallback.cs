using Deployer.Callbacks.Abstractions;

namespace Deployer.Callbacks.CustomProtection;
    [GenerateSerializer]
    public class Actor
    {
        public string login { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string avatar_url { get; set; }
        public string gravatar_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string followers_url { get; set; }
        public string following_url { get; set; }
        public string gists_url { get; set; }
        public string starred_url { get; set; }
        public string subscriptions_url { get; set; }
        public string organizations_url { get; set; }
        public string repos_url { get; set; }
        public string events_url { get; set; }
        public string received_events_url { get; set; }
        public string type { get; set; }
        public bool site_admin { get; set; }
    }

    [GenerateSerializer]
    public class CheckRun
    {
        public long id { get; set; }
        public string name { get; set; }
        public string node_id { get; set; }
        public string head_sha { get; set; }
        public string external_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string details_url { get; set; }
        public string status { get; set; }
        public object conclusion { get; set; }
        public DateTime started_at { get; set; }
        public object completed_at { get; set; }
    }

    [GenerateSerializer]
    public class Creator
    {
        public string login { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string avatar_url { get; set; }
        public string gravatar_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string followers_url { get; set; }
        public string following_url { get; set; }
        public string gists_url { get; set; }
        public string starred_url { get; set; }
        public string subscriptions_url { get; set; }
        public string organizations_url { get; set; }
        public string repos_url { get; set; }
        public string events_url { get; set; }
        public string received_events_url { get; set; }
        public string type { get; set; }
        public bool site_admin { get; set; }
    }

    [GenerateSerializer]
    public class Deployment
    {
        public string url { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string task { get; set; }
        public string original_environment { get; set; }
        public string environment { get; set; }
        public object description { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public string statuses_url { get; set; }
        public string repository_url { get; set; }
        public Creator creator { get; set; }
        public string sha { get; set; }
        public string @ref { get; set; }
        public Payload payload { get; set; }
        public bool transient_environment { get; set; }
        public bool production_environment { get; set; }
        public object performed_via_github_app { get; set; }
    }

    [GenerateSerializer]
    public class DeploymentStatus
    {
        public string url { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string state { get; set; }
        public Creator creator { get; set; }
        public string description { get; set; }
        public string environment { get; set; }
        public string target_url { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public string deployment_url { get; set; }
        public string repository_url { get; set; }
        public string environment_url { get; set; }
        public string log_url { get; set; }
        public object performed_via_github_app { get; set; }
    }

    [GenerateSerializer]
    public class Installation
    {
        public int id { get; set; }
        public string node_id { get; set; }
    }

    [GenerateSerializer]
    public class Owner
    {
        public string login { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string avatar_url { get; set; }
        public string gravatar_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string followers_url { get; set; }
        public string following_url { get; set; }
        public string gists_url { get; set; }
        public string starred_url { get; set; }
        public string subscriptions_url { get; set; }
        public string organizations_url { get; set; }
        public string repos_url { get; set; }
        public string events_url { get; set; }
        public string received_events_url { get; set; }
        public string type { get; set; }
        public bool site_admin { get; set; }
    }

    [GenerateSerializer]
    public class Payload
    {
    }

    [GenerateSerializer]
    public class Repository
    {
        public int id { get; set; }
        public string node_id { get; set; }
        public string name { get; set; }
        public string full_name { get; set; }
        public bool @private { get; set; }
        public Owner owner { get; set; }
        public string html_url { get; set; }
        public object description { get; set; }
        public bool fork { get; set; }
        public string url { get; set; }
        public string forks_url { get; set; }
        public string keys_url { get; set; }
        public string collaborators_url { get; set; }
        public string teams_url { get; set; }
        public string hooks_url { get; set; }
        public string issue_events_url { get; set; }
        public string events_url { get; set; }
        public string assignees_url { get; set; }
        public string branches_url { get; set; }
        public string tags_url { get; set; }
        public string blobs_url { get; set; }
        public string git_tags_url { get; set; }
        public string git_refs_url { get; set; }
        public string trees_url { get; set; }
        public string statuses_url { get; set; }
        public string languages_url { get; set; }
        public string stargazers_url { get; set; }
        public string contributors_url { get; set; }
        public string subscribers_url { get; set; }
        public string subscription_url { get; set; }
        public string commits_url { get; set; }
        public string git_commits_url { get; set; }
        public string comments_url { get; set; }
        public string issue_comment_url { get; set; }
        public string contents_url { get; set; }
        public string compare_url { get; set; }
        public string merges_url { get; set; }
        public string archive_url { get; set; }
        public string downloads_url { get; set; }
        public string issues_url { get; set; }
        public string pulls_url { get; set; }
        public string milestones_url { get; set; }
        public string notifications_url { get; set; }
        public string labels_url { get; set; }
        public string releases_url { get; set; }
        public string deployments_url { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public DateTime pushed_at { get; set; }
        public string git_url { get; set; }
        public string ssh_url { get; set; }
        public string clone_url { get; set; }
        public string svn_url { get; set; }
        public object homepage { get; set; }
        public int size { get; set; }
        public int stargazers_count { get; set; }
        public int watchers_count { get; set; }
        public object language { get; set; }
        public bool has_issues { get; set; }
        public bool has_projects { get; set; }
        public bool has_downloads { get; set; }
        public bool has_wiki { get; set; }
        public bool has_pages { get; set; }
        public bool has_discussions { get; set; }
        public int forks_count { get; set; }
        public object mirror_url { get; set; }
        public bool archived { get; set; }
        public bool disabled { get; set; }
        public int open_issues_count { get; set; }
        public object license { get; set; }
        public bool allow_forking { get; set; }
        public bool is_template { get; set; }
        public bool web_commit_signoff_required { get; set; }
        public List<object> topics { get; set; }
        public string visibility { get; set; }
        public int forks { get; set; }
        public int open_issues { get; set; }
        public int watchers { get; set; }
        public string default_branch { get; set; }
    }
    [GenerateSerializer]
    public class DeploymentStatusCallback
    {
        public DeploymentStatus deployment_status { get; set; }
        public Deployment deployment { get; set; }
        public CheckRun check_run { get; set; }
        public Workflow workflow { get; set; }
        public WorkflowRun workflow_run { get; set; }
        public string action { get; set; }
        public Repository repository { get; set; }
        public Sender sender { get; set; }
        public Installation installation { get; set; }
    }

    [GenerateSerializer]
    public class Sender
    {
        public string login { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string avatar_url { get; set; }
        public string gravatar_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string followers_url { get; set; }
        public string following_url { get; set; }
        public string gists_url { get; set; }
        public string starred_url { get; set; }
        public string subscriptions_url { get; set; }
        public string organizations_url { get; set; }
        public string repos_url { get; set; }
        public string events_url { get; set; }
        public string received_events_url { get; set; }
        public string type { get; set; }
        public bool site_admin { get; set; }
    }

    [GenerateSerializer]
    public class TriggeringActor
    {
        public string login { get; set; }
        public int id { get; set; }
        public string node_id { get; set; }
        public string avatar_url { get; set; }
        public string gravatar_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string followers_url { get; set; }
        public string following_url { get; set; }
        public string gists_url { get; set; }
        public string starred_url { get; set; }
        public string subscriptions_url { get; set; }
        public string organizations_url { get; set; }
        public string repos_url { get; set; }
        public string events_url { get; set; }
        public string received_events_url { get; set; }
        public string type { get; set; }
        public bool site_admin { get; set; }
    }

    [GenerateSerializer]
    public class Workflow
    {
        public int id { get; set; }
        public string node_id { get; set; }
        public string name { get; set; }
        public string path { get; set; }
        public string state { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public string badge_url { get; set; }
    }

    [GenerateSerializer]
    public class WorkflowRun:IWorkflowRun
    {
        public long id { get; set; }
        public string name { get; set; }
        public string node_id { get; set; }
        public string head_branch { get; set; }
        public string head_sha { get; set; }
        public string path { get; set; }
        public string display_title { get; set; }
        public int run_number { get; set; }
        public string @event { get; set; }
        public string status { get; set; }
        public object conclusion { get; set; }
        public int workflow_id { get; set; }
        public long check_suite_id { get; set; }
        public string check_suite_node_id { get; set; }
        public string url { get; set; }
        public string html_url { get; set; }
        public List<object> pull_requests { get; set; }
        public DateTime created_at { get; set; }
        public DateTime updated_at { get; set; }
        public Actor actor { get; set; }
        public int run_attempt { get; set; }
        public List<object> referenced_workflows { get; set; }
        public DateTime run_started_at { get; set; }
        public TriggeringActor triggering_actor { get; set; }
    }

