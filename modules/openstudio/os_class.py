# -*- coding: utf-8 -*-

import datetime

from gluon import *


class Class:
    """
        Class that gathers useful functions for a class in OpenStudio
    """
    def __init__(self, clsID, date):
        self.clsID = clsID
        self.date = date

        db = current.db
        self.cls = db.classes(self.clsID)


    def get_name(self, pretty_date=False):
        """
            Returns class name formatted for general use
        """
        db = current.db
        T = current.T
        TIME_FORMAT = current.TIME_FORMAT
        DATE_FORMAT = current.DATE_FORMAT

        if pretty_date:
            date = self.date.strftime('%d %B %Y')
        else:
            date = self.date.strftime(DATE_FORMAT)


        record = self.cls
        location = db.school_locations[record.school_locations_id].Name
        classtype = db.school_classtypes[record.school_classtypes_id].Name
        class_name =  date + ' ' + \
                      record.Starttime.strftime(TIME_FORMAT) + ' - ' + \
                      classtype + ' ' + location

        return class_name


    def get_name_shop(self):
        """
            Returns class name formatted for use in customer profile and shop
        """
        db = current.db
        T = current.T
        TIME_FORMAT = current.TIME_FORMAT

        record = self.cls
        location = db.school_locations[record.school_locations_id].Name
        classtype = db.school_classtypes[record.school_classtypes_id].Name
        class_name =  self.date.strftime('%d %B %Y') + ' ' + '<br><small>' + \
                      record.Starttime.strftime(TIME_FORMAT) + ' - ' + \
                      record.Endtime.strftime(TIME_FORMAT) + ' ' + \
                      classtype + ' ' + \
                      T('in') + ' ' + location + '</small>'

        return class_name


    def get_prices(self):
        """
            Returns the price for a class
        """
        db = current.db

        query = (db.classes_price.classes_id == self.clsID) & \
                (db.classes_price.Startdate <= self.date) & \
                ((db.classes_price.Enddate >= self.date) |
                 (db.classes_price.Enddate == None))
        prices = db(query).select(db.classes_price.ALL,
                                  orderby=db.classes_price.Startdate)

        if prices:
            prices = prices.first()
            dropin = prices.Dropin or 0
            trial  = prices.Trial or 0
            dropin_membership = prices.DropinMembership or 0
            trial_membership = prices.TrialMembership or 0

            trial_tax = db.tax_rates(prices.tax_rates_id_trial)
            dropin_tax = db.tax_rates(prices.tax_rates_id_dropin)
            trial_tax_membership = db.tax_rates(prices.tax_rates_id_trial_membership)
            dropin_tax_membership = db.tax_rates(prices.tax_rates_id_dropin_membership)

            try:
                trial_tax_rates_id    = trial_tax.id
                dropin_tax_rates_id   = dropin_tax.id
                trial_tax_percentage  = trial_tax.Percentage
                dropin_tax_percentage = dropin_tax.Percentage
            except AttributeError:
                trial_tax_rates_id    = None
                dropin_tax_rates_id   = None
                trial_tax_percentage  = None
                dropin_tax_percentage = None

            try:
                trial_tax_rates_id_membership = trial_tax_membership.id
                dropin_tax_rates_id_membership = dropin_tax_membership.id
                trial_tax_percentage_membership = trial_tax_membership.Percentage
                dropin_tax_percentage_membership = dropin_tax_membership.Percentage
            except AttributeError:
                trial_tax_rates_id_membership = None
                dropin_tax_rates_id_membership = None
                trial_tax_percentage_membership = None
                dropin_tax_percentage_membership = None

        else:
            dropin = 0
            trial  = 0
            trial_tax_rates_id    = None
            dropin_tax_rates_id   = None
            trial_tax_percentage  = None
            dropin_tax_percentage = None
            dropin_membership = 0
            trial_membership = 0
            trial_tax_rates_id_membership = None
            dropin_tax_rates_id_membership = None
            trial_tax_percentage_membership = None
            dropin_tax_percentage_membership = None


        return dict(
            trial  = trial,
            dropin = dropin,
            trial_tax_rates_id   = trial_tax_rates_id,
            dropin_tax_rates_id   = dropin_tax_rates_id,
            trial_tax_percentage  = trial_tax_percentage,
            dropin_tax_percentage = dropin_tax_percentage,
            trial_membership = trial_membership,
            dropin_membership = dropin_membership,
            trial_tax_rates_id_membership = trial_tax_rates_id_membership,
            dropin_tax_rates_id_membership = dropin_tax_rates_id_membership,
            trial_tax_percentage_membership = trial_tax_percentage_membership,
            dropin_tax_percentage_membership = dropin_tax_percentage_membership,
        )


    def get_prices_customer(self, cuID):
        """
            Returns the price for a class
            :param cuID: db.auth_user.id
            :return: dict of class prices
        """
        from openstudio.os_customer import Customer

        db = current.db
        customer = Customer(cuID)
        has_membership = customer.has_membership_on_date(self.date)


        query = (db.classes_price.classes_id == self.clsID) & \
                (db.classes_price.Startdate <= self.date) & \
                ((db.classes_price.Enddate >= self.date) |
                 (db.classes_price.Enddate == None))
        prices = db(query).select(db.classes_price.ALL,
                                  orderby=db.classes_price.Startdate)

        if prices:
            prices = prices.first()

            if not has_membership:
                dropin = prices.Dropin or 0
                trial = prices.Trial or 0

                trial_tax = db.tax_rates(prices.tax_rates_id_trial)
                dropin_tax = db.tax_rates(prices.tax_rates_id_dropin)

                try:
                    trial_tax_rates_id = trial_tax.id
                    dropin_tax_rates_id = dropin_tax.id
                    trial_tax_percentage = trial_tax.Percentage
                    dropin_tax_percentage = dropin_tax.Percentage
                except AttributeError:
                    trial_tax_rates_id = None
                    dropin_tax_rates_id = None
                    trial_tax_percentage = None
                    dropin_tax_percentage = None
            else: # has membership
                dropin = prices.DropinMembership or 0
                trial = prices.TrialMembership or 0

                trial_tax = db.tax_rates(prices.tax_rates_id_trial_membership)
                dropin_tax = db.tax_rates(prices.tax_rates_id_dropin_membership)

                try:
                    trial_tax_rates_id = trial_tax.id
                    dropin_tax_rates_id = dropin_tax.id
                    trial_tax_percentage = trial_tax.Percentage
                    dropin_tax_percentage = dropin_tax.Percentage
                except AttributeError:
                    trial_tax_rates_id = None
                    dropin_tax_rates_id = None
                    trial_tax_percentage = None
                    dropin_tax_percentage = None

        else:
            dropin = 0
            trial  = 0
            trial_tax_rates_id    = None
            dropin_tax_rates_id   = None
            trial_tax_percentage  = None
            dropin_tax_percentage = None


        return dict(
            trial  = trial,
            dropin = dropin,
            trial_tax_rates_id   = trial_tax_rates_id,
            dropin_tax_rates_id   = dropin_tax_rates_id,
            trial_tax_percentage  = trial_tax_percentage,
            dropin_tax_percentage = dropin_tax_percentage,
        )


    def get_full(self):
        """
            Check whether or not this class is full
        """
        db = current.db

        spaces = self.cls.Maxstudents

        query = (db.classes_attendance.classes_id == self.clsID) & \
                (db.classes_attendance.ClassDate == self.date) & \
                (db.classes_attendance.BookingStatus != 'cancelled')
        filled = db(query).count()

        full = True if filled >= spaces else False

        return full


    def get_full_bookings_shop(self):
        """
            Check whether there are spaces left for online bookings
        """
        db = current.db

        spaces = self.cls.MaxOnlineBooking
        query = (db.classes_attendance.classes_id == self.clsID) & \
                (db.classes_attendance.ClassDate == self.date) & \
                (db.classes_attendance.online_booking == True) & \
                (db.classes_attendance.BookingStatus != 'cancelled')
        filled = db(query).count()

        full = True if filled >= spaces else False

        return full


    def get_invoice_order_description(self, attendance_type):
        """        
            :return: string with a description of the class 
        """
        DATE_FORMAT = current.DATE_FORMAT
        TIME_FORMAT = current.TIME_FORMAT

        db = current.db
        T  = current.T

        prices = self.get_prices()
        if attendance_type == 1:
            price = prices['trial']
            tax_rates_id = prices['trial_tax_rates_id']
            at = T('Trial')
        elif attendance_type == 2:
            price = prices['dropin']
            tax_rates_id = prices['dropin_tax_rates_id']
            at = T('Drop in')


        location =  db.school_locations(self.cls.school_locations_id)
        classtype = db.school_classtypes(self.cls.school_classtypes_id)

        description = self.date.strftime(DATE_FORMAT) + ' ' + \
                      self.cls.Starttime.strftime(TIME_FORMAT) + ' ' + \
                      classtype.Name + ' ' + \
                      location.Name + ' ' + \
                      '(' + at + ')'

        return description


    def add_to_shoppingcart(self, cuID, attendance_type=2):
        """
            Add a workshop product to the shopping cart of a customer
            attendance_type can be 1 for trial class or 2 for drop in class
        """
        db = current.db

        db.customers_shoppingcart.insert(
            auth_customer_id = cuID,
            classes_id = self.clsID,
            ClassDate = self.date,
            AttendanceType = attendance_type
        )


    def is_on_correct_weekday(self):
        """
            Checks if self.date.isoweekday() == self.cls.Week_day
        """
        if self.date.isoweekday() == self.cls.Week_day:
            return True
        else:
            return False


    def is_past(self):
        """
            Return True if NOW_LOCAL > Class start else return False
        """
        import pytz

        db = current.db
        now = current.NOW_LOCAL
        TIMEZONE = current.TIMEZONE

        cls_time = self.cls.Starttime

        class_dt = datetime.datetime(year=self.date.year,
                                     month=self.date.month,
                                     day=self.date.day,
                                     hour=cls_time.hour,
                                     minute=cls_time.minute)
        # localize the class datetime so it can be compared to now
        # class_dt = pytz.utc.localize(class_dt)
        class_dt = pytz.timezone(TIMEZONE).localize(class_dt)

        if class_dt < now:
            return True
        else:
            return False


    def is_cancelled(self):
        """
            Return True if the class is cancelled, else return False
        """
        db = current.db
        query = (db.classes_otc.classes_id == self.clsID) & \
                (db.classes_otc.ClassDate == self.date) & \
                (db.classes_otc.Status == 'cancelled')

        cancelled = True if db(query).count() else False
        return cancelled


    def is_holiday(self):
        """
            Return True if the class is within a holiday, else return False
        """
        db = current.db

        # Query school_holidays table to see if there's a holiday for this location
        left = [db.school_holidays_locations.on(db.school_holidays.id ==
                                                db.school_holidays_locations.school_holidays_id)]
        query = (db.school_holidays.Startdate <= self.date) & \
                (db.school_holidays.Enddate >= self.date) & \
                (db.school_holidays_locations.school_locations_id == self.cls.school_locations_id)

        rows = db(query).select(db.school_holidays.id,
                                left=left)

        holiday = True if len(rows) else False
        return holiday


    def is_taking_place(self):
        """
             Check if the class is not in past, cancelled or in a holiday
             Return True if not in past, cancelled or in holiday, else return False
        """
        correct_weekday = self.is_on_correct_weekday()
        past = self.is_past()
        cancelled = self.is_cancelled()
        holiday = self.is_holiday()

        if not past and not cancelled and not holiday and correct_weekday:
            return True
        else:
            return False


    def is_booked_by_customer(self, cuID):
        """
        :param cuID: db.auth_user.id
        :return: Boolean

        Check if the class is booked by this customer or not
        """
        db = current.db

        query = ((db.classes_attendance.BookingStatus == 'booked') |
                 (db.classes_attendance.BookingStatus == 'attending')) & \
                (db.classes_attendance.classes_id == self.clsID) & \
                (db.classes_attendance.ClassDate == self.date) & \
                (db.classes_attendance.auth_customer_id == cuID)

        rows = db(query).select(db.classes_attendance.id)
        if len(rows) > 0:
            return True
        else:
            return False


    def has_recurring_reservation_spaces(self):
        """
        Check whether a class has space for more recurring reservations
        :param date: datetime.date
        :return: Boolean
        """
        db = current.db

        spaces = self.cls.MaxReservationsRecurring

        query = (db.classes_reservation.classes_id == self.clsID) & \
                (db.classes_reservation.ResType == 'recurring') & \
                (db.classes_reservation.Startdate <= self.date) & \
                ((db.classes_reservation.Enddate >= self.date) |
                 (db.classes_reservation.Enddate == None))

        reservations = db(query).count()

        if reservations >= spaces:
            return False
        else:
            return True


    def get_trialclass_allowed_in_shop(self):
        """
        Check whether trial classes in the shop are allowed or not
        :return: Boolean
        """
        if self.cls.AllowShopTrial:
            return True
        else:
            return False


    def get_attendance_count(self):
        """
        :return: integer ; count of customers attending this class
        """
        db = current.db

        query = (db.classes_attendance.classes_id == self.clsID) & \
                (db.classes_attendance.ClassDate == self.date) & \
                (db.classes_attendance.BookingStatus != 'cancelled')

        return db(query).count()


    def get_teachers(self):
        """
        Teachers for class
        :return:
        """
        db = current.db

        query = (db.classes_teachers.classes_id == self.clsID) & \
                ((db.classes_teachers.Startdate <= self.date) &
                 ((db.classes_teachers.Enddate >= self.date) |
                  (db.classes_teachers.Enddate == None)))
        rows = db(query).select(db.classes_teachers.ALL)

        teachers = rows.first()

        cotc = db.classes_otc(
            classes_id = self.clsID,
            ClassDate = self.date
        )

        teacher = db.auth_user(teachers.auth_teacher_id)
        if cotc:
            if cotc.auth_teacher_id:
                teacher = db.auth_user(cotc.auth_teacher_id)



        teacher2 = teacher2 = db.auth_user(teachers.auth_teacher_id2)
        if cotc:
            if cotc.auth_teacher_id2:
                teacher2 = db.auth_user(cotc.auth_teacher_id2)

        return dict(
            teacher = teacher,
            teacher2 = teacher2
        )


    def get_teacher_payment(self):
        """
        Returns amount excl. VAT
        :return: { amount: float, tax_rates_id: db.tax_rates.id }
        """
        T = current.T
        db = current.db

        #TODO: check which payment method is used here. fixed rate or attendance based
        # It now defaults to attendance based

        # Get list for class type
        cltID = self.cls.school_classtypes_id
        tpalst = db.teachers_payment_attendance_lists_school_classtypes(
            school_classtypes_id = cltID
        )

        # Check if we have a payment, if not insert it with Status 'not_verified"
        tpac = db.teachers_payment_attendance_classes(
            classes_id = self.clsID,
            ClassDate = self.date
        )

        if tpalst:
            list_id = tpalst.teachers_payment_attendance_lists_id

            list = db.teachers_payment_attendance_lists(1)
            tax_rates_id = list.tax_rates_id

            attendance_count = self.get_attendance_count()

            query = (db.teachers_payment_attendance_lists_rates.teachers_payment_attendance_lists_id == list_id) & \
                    (db.teachers_payment_attendance_lists_rates.AttendanceCount == attendance_count)
            row = db(query).select(db.teachers_payment_attendance_lists_rates.Rate)

            try:
                rate = row.first().Rate
            except AttributeError:
                rate = 0

            if not tpac and tpalst:
                tpaID = db.teachers_payment_attendance_classes.insert(
                    classes_id = self.clsID,
                    ClassDate = self.date,
                    Status = 'not_verified',
                    AttendanceCount = attendance_count,
                    Amount = rate,
                    teachers_payment_attendance_classes_list_id = list.id,
                    tax_rates_id = tax_rates_id,
                )
                tpac = db.teachers_payment_attendance_classes(tpaID)

            elif tpac and tpalst:
                tpac.AttendanceCount = attendance_count
                tpac.Amount = rate
                tpac.teachers_payment_attendance_classes_list_id = list.id
                tpac.tax_rates_id = tax_rates_id
                tpac.update_record()


            data = tpac
            status = 'success'
        else:
            data = T('No payment list defined for this class type')
            status = 'error'


        return {
            'data':data,
            'status': status
        }