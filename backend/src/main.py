from classes.database import Database
from miner import JobScraper
from analysis import update_analytics
from utils.service_key import get_service_account_key
from badge_generator import update_job_count_badge


def rebase_stats() -> None:
    """
    After DELETING the `statistics` collection in main database manually,
    call this function to recalculate all statistics and sync with
    `frontend-db`.

    No scraping takes place when this function is called. Statistics are
    calculated from existing scraped jobs.

    WARNING: This function heavily impacts read and write quotas.
    """
    # load main database.
    my_database = Database(get_service_account_key(True))

    # get all jobs stored in database
    all_jobs = my_database.get_dataframe().to_dict('records')

    # update general stats
    my_database.update_metadata(len(all_jobs))

    if (len(all_jobs) == 0):
        sync_stats(my_database)
        return

    # get data to be analysed in a list
    job_details_list = [job['job_details'] for job in all_jobs]
    salary_list = [job['salary'] for job in all_jobs]
    location_list = [job['location'] for job in all_jobs]
    job_title_list = [job['job_title'] for job in all_jobs]

    # process data and updates statistics
    update_analytics(my_database, job_title_list,
                     job_details_list, location_list, salary_list)

    # serve stats to frontend
    sync_stats(my_database)

    # update job count in readme
    # update_job_count_badge(len(all_jobs))


def sync_stats(main_db: Database):
    """
    Clones statistics found in `main_db` to `frontend_db`

    Args:
        main_db (Database): database containing scraped data
    """
    frontend_db = Database(get_service_account_key(), "frontend_db")
    x = main_db.export_collection(main_db.stats_collection_ref)
    frontend_db.import_collection(frontend_db.stats_collection_ref, x)


def backup_to_drive():
    """
    Saves all jobs in main database to google drive in json format.
    """
    main_db = Database(get_service_account_key(True))
    df = main_db.get_dataframe()
    df.to_json('sample_jobs.json', orient='records')


def main():

    # setup database and scraper.
    main_db = Database(get_service_account_key(True))
    my_scraper = JobScraper(main_db.get_recent_urls())

    # fetch new jobs from myjob.mu
    new_jobs = my_scraper.scrape()

    # if no new jobs found exit
    if (len(new_jobs) == 0):
        return

    # get data to be analysed in a list
    job_details_list = [job['job_details'] for job in new_jobs]
    salary_list = [job['salary'] for job in new_jobs]
    location_list = [job['location'] for job in new_jobs]
    job_title_list = [job['job_title'] for job in new_jobs]

    # print some info about new jobs found
    print(len(new_jobs), ' new jobs found!')
    print(job_title_list[:5])

    # update database general stats such as size and last update dates
    new_db_size = main_db.get_size() + len(new_jobs)
    main_db.update_metadata(new_db_size)

    # save new jobs to database
    for job in new_jobs:
        main_db.add_job(job)

    # extract statistics from newly scraped data and update
    # statistics collection
    update_analytics(main_db, job_title_list,
                     job_details_list, location_list, salary_list)

    # send updated statistics to frontend db
    sync_stats(main_db)

    # update job count in readme
    update_job_count_badge(new_db_size)


if __name__ == "__main__":
    # main()
    # print(JobScraper([], 1).scrape())
    # rebase_stats()
    # my_database = Database(get_service_account_key(True))
    # all_jobs = my_database.get_dataframe().to_dict('records')
    # job_title_list = list(set([job['job_title'] for job in all_jobs]))
    # print('\n'.join(job_title_list))
    rebase_stats()
