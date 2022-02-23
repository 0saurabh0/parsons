import logging

logger = logging.getLogger(__name__)

class Events:
    """A class for interacting with PDI events via PDIs API"""

    def __init__(self):
        self.events_url = self.base_url + '/events'
        self.calendars_url = self.base_url + '/calendars'
        self.eventactivities_url = self.base_url + '/eventActivities'
        self.activites_url = self.base_ur +'/activities'

        super().__init__()

    def get_activity(self, activity_id):
        """Get details for a specific activity using the activity id

        `Args:`
            activity_id: int
                The activity id that you'd like to retrieve details for
        `Returns:`
            A dictionary with the activity id, activityName, and activityAddress
        """

        return self._request(self.activities_ur + f'/{activity_id}', req_type='GET')

    def create_event(self, calendar_id: str, location_id: str, event_name: str, start_datetime: str,
                     end_datetime: str, description=None,all_day=False, recurrencetype=None,
                     recurrence_end_datetime=None, host_phone=None, host_email=None, website=None):
        """Create event in a specified calendar

        `Args:`
            calendar_id: str
                The calendar in which you'd like to create an event
            location_id: str
                The unique ID of the PDI location this event took place/is to take place at
            event_name: str
                The name of your event
            description: str
                A short description for your event
            start_datetime: str
                The start datetime of the event in UTC timezone formatted as
                yyyy-MM-ddThh:mm:ss.fffZ
            end_datetime: str
                The end date formatted like start_datetime
            is_all_day = bool
                set to True if event is an all day event. Defaults to False
            recurrencetype: str
                Either 'daily', 'weekly', or 'monthly'. Defaults to None
            recurrence_end_datetime: str
                The end time of the last recurrence of the event formatted as
                yyyy-MM-ddThh:mm:ss.fffZ
            host_phone: str
                An optional contact phone number for the host. Defaults to None
            host_email: str
                An optional contact email for the host. Defaults to None
            website: str
                An optional website for the event. Defualts to None

        `Returns:`
            dict
                Response from PDI in dictionary object

            """

        payload = {
          "locationId": location_id,
          "recurrenceType": recurrencetype,
          "name": event_name,
          "description": description,
          "startDateTimeUtc": start_datetime,
          "endDateTimeUtc": end_datetime,
          "isAllDay": str(all_day).lower(),
          "recurrenceEndDateTimeUtc": recurrence_end_datetime,
          "phone": host_phone,
          "contactEmail": host_email,
          "website": website
        }

        response = self._request(self.calendars_url + f'/{calendar_id}' + '/events',
                                 req_type='POST', post_data=payload)
        event_id = response['id']
        logger.info(f'Created event {event_name} (id: {event_id})')

        return response

    def create_event_with_activity(self, calendar_id: str, location_id: str, activity_id: str,
                                   event_name: str, activity_name: str, start_datetime: str,
                                   end_datetime: str, description=None, all_day=False,
                                   recurrencetype=None, recurrence_end_datetime=None, host_phone=None,
                                   host_email=None, website=None, signup_goal=None):
        """Create event in a specified calendar with an associated activity. The activty will
            be assigned the same start, end time, and recurrance settings as the event.

                `Args:`
                    calendar_id: str
                        The unique ID of the calendar in which you'd like to create an event
                    location_id: str
                        The unique ID of the PDI location whek this event took place/is to take
                        place
                    activity_id:
                        The unique ID of the activity type you'd like to add to the event
                    event_name: str
                        The name of your event
                    activity_name: str
                        The name of your activity. e.g. 'Pictionary!'
                    description: str
                        A short description for your event
                    start_datetime: str
                        The start datetime of the event in UTC timezone formatted as
                        yyyy-MM-ddThh:mm:ss.fffZ
                    end_datetime: str
                        The end date formatted like start_datetime
                    is_all_day = bool
                        set to True if event is an all day event. Defaults to False
                    recurrencetype: str
                        Either 'daily', 'weekly', or 'monthly'. Defaults to None
                    recurrence_end_datetime: str
                        The end time of the last recurrence of the event formatted as
                        yyyy-MM-ddThh:mm:ss.fffZ
                    host_phone: str
                        An optional contact phone number for the host. Defaults to None
                    host_email: str
                        An optional contact email for the host. Defaults to None
                    website: str
                        An optional website for the event. Defualts to None
                    signup_goal: int
                        The goal of how many people you want to complete the activity
                `Returns:`
                    dict
                        Response from PDI in dictionary object
                    """
        event_data = self.create_event(calendar_id, location_id, event_name, start_datetime,
                                       end_datetime, description, all_day, recurrencetype,
                                       recurrence_end_datetime, host_phone, host_email, website)
        event_id = event_data['id']
        logger.info(f'Created event {event_name} (id: {event_id})')

        event_activity_payload = {
            "CalendarId": calendar_id,
            "EventId": event_id,
            "ActivityId": activity_id,
            "LocationId": location_id,
            "RecurrenceType": recurrencetype,
            "Name": activity_name,
            "Description": None,
            "StartDateTimeUtc": start_datetime,
            "EndDateTimeUtc": end_datetime,
            "CountGoal": signup_goal,
            "RecurrenceEndDateTimeUtc": recurrence_end_datetime
        }

        response = self._request(self.eventactivities_url, req_type='POST',
                                 post_data=event_activity_payload)
        logger.info(f'Created activity {activity_name} for event {event_name} (id: {event_id})')

        return response

    def create_event_activity(self, calendar_id: str, event_id: str, activity_id: str,
                              location_id: str, activity_name: str, start_datetime: str,
                              end_datetime: str, description=None, recurrencetype=None,
                              recurrence_end_datetime=None, signup_goal=None):
        """Create event in a specified calendar with an associated activity

                `Args:`
                    calendar_id: str
                        The unique ID of the calendar in which you'd like to create an event
                    event_id: str
                        The unique ID of the event this activity is to be associated with
                    activity_id:
                        The unique ID of the activity type you'd like to add to the event
                    location_id: str
                        The unique ID of the PDI location where this event took place/is to take
                        place
                    activity_name: str
                        The name of your activity. e.g. 'Pictionary!'
                    description: str
                        A short description for your event activity
                    start_datetime: str
                        The start datetime of the event in UTC timezone formatted as
                        yyyy-MM-ddThh:mm:ss.fffZ
                    end_datetime: str
                        The end date formatted like start_datetime
                    recurrencetype: str
                        Either 'daily', 'weekly', or 'monthly'. Defaults to None
                    recurrence_end_datetime: str
                        The end time of the last recurrence of the event formatted as
                        yyyy-MM-ddThh:mm:ss.fffZ
                    signup_goal: int
                        The goal of how many people you want to complete the activity


                `Returns:`
                    dict
                        Response from PDI in dictionary object
                    """

        event_activity_payload = {
            "CalendarId": calendar_id,
            "EventId": event_id,
            "ActivityId": activity_id,
            "LocationId": location_id,
            "RecurrenceType": recurrencetype,
            "Name": activity_name,
            "Description": description,
            "StartDateTimeUtc": start_datetime,
            "EndDateTimeUtc": end_datetime,
            "CountGoal": signup_goal,
            "RecurrenceEndDateTimeUtc": recurrence_end_datetime
        }

        response = self._request(self.eventactivities_url, req_type='POST',
                                 post_data=event_activity_payload)
        logger.info(f'Created activity {activity_name} for event {event_id})')

        return response

    def create_invitation(self, event_id: str, contact_id: str, status: str, attended: bool,
                          confirmed=False, specific_occurrence_start=None):
        """Create a PDI event invitation indicating a contact has been registered for an event

            `Args:`
                event_id: str
                    The ID of the event to write the RSVP to
                contact_id: str
                    The ID of the contact to which the invitation belongs
                status: str
                    Options are: "Yes", "No", "Maybe", "Scheduled", "Invited", "Cancelled",
                    "No-Show", "Completed", and ""
                attended: boolean
                    Indicates whether contact attended event
                confirmed: boolean
                    Indicates whether invitation confirmed they will attend the event. Defaults to
                    False
                specific_occurrence_start: str
                    If invitation is for a specific occurrence of a recurring event, then the start
                    datetime of the event in UTC formatted as yyyy-MM-ddTHH:mm:ss.fffZ
            `Returns:`
                dict
                    Response from PDI in dictionary object
        """

        event_invitation_payload ={
                "contactId": contact_id,
                "rsvpStatus": status,
                "isConfirmed": confirmed,
                "attended": attended
            }

        if specific_occurrence_start:
            event_invitation_payload["specificOcurrenceStartUtc"] = specific_occurrence_start

        response = self._request(self.events_url + f'/{event_id}/invitations',
                                 req_type='POST', post_data=event_invitation_payload)
        return response


    def update_invitation(self, invitation_id: str, event_id: str, contact_id: str, status=None,
                          attended=None, confirmed=None, specific_occurrence_start=None):
        """Modify a PDI event invitation

            `Args:`
                invitation_id: str
                    The ID of the event invitation
                event_id: str
                    The ID of the event that corresponds to the invitation
                contact_id: str
                    The ID of the contact to which the invitation belongs
                status: str
                    Options are: "Yes", "No", "Maybe", "Scheduled", "Invited", "Cancelled",
                    "No-Show", "Completed", and ""
                attended: boolean
                    Indicates whether contact attended event
                confirmed: boolean
                    Indicates whether invitation confirmed they will attend the event
                specific_occurrence_start: str
                    If invitation is for a specific occurrence of a recurring event, then the start
                    datetime of the event in UTC formatted as yyyy-MM-ddTHH:mm:ss.fffZ
            `Returns:`
                dict
                    Response from PDI in dictionary object
        """

        event_invitation_payload = {
            "contactId": contact_id
        }

        if status:
            event_invitation_payload['rsvpStatus'] = status
        if confirmed is not None:
            event_invitation_payload['isConfirmed'] = confirmed
        if attended is not None:
            event_invitation_payload['attended'] = attended
        if specific_occurrence_start:
            event_invitation_payload["specificOcurrenceStartUtc"] = specific_occurrence_start

        response = self._request(self.events_url + f'/{event_id}/invitations/{invitation_id}',
                                 req_type='PUT', post_data=event_invitation_payload)
        return response