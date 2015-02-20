class Person(object):
    def __init__(self, name, phone_number, email_address, address=None):
        self._name = name
        self._phone_number = phone_number
        self._email_address = email_address
        self._address = address

    def purchase_parking_pass(self):
        pass


class Student(Person):
    @classmethod
    def is_eligible_to_enroll(self):
        pass


class Professor(Person):
    pass


class Address(object):
    def __init__(self, street, city, state, postal_code, country):
        self._street = street
        self._city = city
        self._state = state
        self._postal_code = postal_code
        self._country = country

    def validate(self):
        pass

    def output_as_label(self):
        pass

address = Address('street')
person = Student('steve', 1213, 'email.com', address)