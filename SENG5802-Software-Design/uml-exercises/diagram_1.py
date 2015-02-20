import datetime


class Flight(object):
    def __init__(self, flight_no):
        self.flight_no = None
        self.departure_time = None
        self.flight_duration = None

    def delay_flight(self, number_minutes):
        return datetime.date()

    def get_arrival_time(self):
        return datetime.date()