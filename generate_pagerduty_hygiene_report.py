#!/usr/bin/env python3
"""
For a given PagerDuty account, create a report detailing:
 - the total number of user licences in use
 - users who are not on any schedules (rotas)
 - users on schedules that are not current users (i.e. users who have been
     deleted but not removed from schedules)
 - users who have not accepted their invite to set up their PagerDuty user
"""
import os
from datetime import date
from pdpyras import APISession, PDClientError

api_key = os.environ['PD_API_KEY']
session = APISession(api_key)


def get_schedule_ids():
    schedule_ids = []
    try:
        for schedule in session.iter_all('schedules',
                                         params={'time_zone': 'UTC'}):
            schedule_ids.append(schedule['id'])

    except PDClientError as e:
        if e.response:
            raise e
        else:
            print("Non-transient network or client error")

    return schedule_ids


def get_users_on_schedules(schedule_ids):
    users_on_schedules = {}
    since = date.today()
    try:
        for id in schedule_ids:
            query_str = f"/schedules/{id}/users?since={since}"
            users = session.rget(query_str)
            for user in users:
                users_on_schedules[user['id']] = user['summary']

    except PDClientError as e:
        if e.response:
            raise e
        else:
            print("Non-transient network or client error")

    return users_on_schedules


def get_all_users():
    pdusers = {}
    try:
        for user in session.iter_all('users'):
            teams = []
            for team in user['teams']:
                teams.append(team['summary'])
            pdusers[user['id']] = {
                'name': user['summary'],
                'teams': teams,
                'invitation_sent': user['invitation_sent']
                }

    except PDClientError as e:
        if e.response:
            raise e
        else:
            print("Non-transient network or client error")

    return pdusers


def main():
    schedule_ids = get_schedule_ids()
    users_on_schedules = get_users_on_schedules(schedule_ids)
    pdusers = get_all_users()

    print('The following users have been deleted but are still on a schedule')
    print('-----------------------------------------------------------------')
    number_of_deleted_users_on_schedules = 0
    for user_id in users_on_schedules.keys():
        if user_id not in pdusers:
            number_of_deleted_users_on_schedules += 1
            print(f"User {users_on_schedules[user_id]} is on a schedule but",
                  "does not have a licence")

    print('')
    print('The following users are not on any schedules')
    print('--------------------------------------------')
    number_of_users_not_on_schedules = 0
    for user_id in pdusers:
        if user_id not in users_on_schedules:
            number_of_users_not_on_schedules += 1
            print(f"{pdusers[user_id]['name']} {pdusers[user_id]['teams']}")

    print('')
    print("The following users have not accepted their invitations")
    print('-------------------------------------------------------')
    number_of_user_not_accepted_invite = 0
    for user_id in pdusers:
        if pdusers[user_id]['invitation_sent'] is True:
            number_of_user_not_accepted_invite += 1
            print(f"{pdusers[user_id]['name']} {pdusers[user_id]['teams']}")

    print('')
    print('Some stats')
    print('----------')
    print(f"Found {len(pdusers)} licenced users in PagerDuty")
    print(f"Found {len(users_on_schedules)} users on schedules")
    print(f"Found {number_of_users_not_on_schedules} users not on any",
          "schedules")
    print(f"Found {number_of_deleted_users_on_schedules} deleted users who",
          "need to be removed from a schedule")
    print(f"Found {number_of_user_not_accepted_invite} users who have not",
          "accepted their invites")


if __name__ == '__main__':
    main()
