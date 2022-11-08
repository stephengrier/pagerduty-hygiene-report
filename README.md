# pagerduty-hygiene-report
Generate hygiene reports for a PagerDuty account

The `generate-pagerduty-hygiene-report.py` script generates a report for a given
PagerDuty account detailing:
 - the total number of user licences in use
 - users who are not on any schedules (rotas)
 - users on schedules that are not current users (i.e. users who have been
     deleted but not removed from schedules)
 - users who have not accepted their invite to set up their PagerDuty user

## Install requirements

The `generate-pagerduty-hygiene-report.py` script needs the pdpyras library.
Install it like so:

```
pip3 install -r requirements.txt
```

## Running

The `generate-pagerduty-hygiene-report.py` script needs an API token to be able
to authenticate to your PagerDuty account. It will take this from the
`PD_API_KEY` environment variable.

You can run the script like so:

```bash
PD_API_KEY=XXXXXXXXXX python3 generate_pagerduty_hygiene_report.py
```

## Output

The report generated looks something like this:

```
The following users have been deleted but are still on a schedule
-----------------------------------------------------------------
User Bob Smith is on a schedule but does not have a licence

The following users are not on any schedules
--------------------------------------------
Harry Jones ['Infrastructure','Developers']
Jenny Hughes ['Developers']

The following users have not accepted their invitations
-------------------------------------------------------
Tony Bertram ['Frontend Devs']

Some stats
----------
Found 27 licenced users in PagerDuty
Found 26 users on schedules
Found 2 users not on any schedules
Found 1 deleted users who need to be removed from a schedule
Found 4 users who have not accepted their invites
```
