using System;
using System.Collections.Generic;
[Serializable]
public class Reviewer
{
    public int id { get; set; }
    public string node_id { get; set; }
    public string url { get; set; }
    public string html_url { get; set; }
    public string name { get; set; }
    public string slug { get; set; }
    public string description { get; set; }
    public string privacy { get; set; }
    public string notification_setting { get; set; }
    public string permission { get; set; }
    public string members_url { get; set; }
    public string repositories_url { get; set; }
    public object parent { get; set; }
    public string login { get; set; }
    public string avatar_url { get; set; }
    public string gravatar_id { get; set; }
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
[Serializable]
public class WfEnvironment
{
    public int id { get; set; }
    public string node_id { get; set; }
    public string name { get; set; }
    public string url { get; set; }
    public string html_url { get; set; }
}

[Serializable]
public class PendingRun
{
    public WfEnvironment environment { get; set; }
    public int wait_timer { get; set; }
    public string wait_timer_started_at { get; set; }
    public bool current_user_can_approve { get; set; }
    public List<Reviewer> reviewers { get; set; }
}
