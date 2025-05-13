from job_filter_GCP import get_job_links, send_email


def job_notify(request):
    from job_filter_GCP import get_job_links, send_email

    links = get_job_links(24)
    if links:
        send_email(links)
    return "Job search complete found"
