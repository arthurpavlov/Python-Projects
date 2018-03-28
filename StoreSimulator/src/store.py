"""Assignment 1 - Grocery Store Models (Task 1)

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
# This module is used to read in the data from a json configuration file.
import json


class GroceryStore:
    """A grocery store.

    A grocery store that contains customers and checkout lines.

    === Attributes ===
    @type customer_count: int
        Total number of customer that visited the store.
    @type max_wait: int
        The maximum amount of time a single customer waited in the store.
    @type config: dict[str,int]
        A dictionary with information about the number of lines
        we should open in the grocery store and the maximum number of customers
        a line can have at one time.
    """
    # === Private attributes ===
    # @type _cashiers: list[StandardCheckout, ExpressCheckout, SelfCheckout]
    #    A list representing all the checkout lines in the store. List contains
    #    the specified amount of StandardCheckout, ExpressCheckout and SelfCheckout
    #    objects.
    #

    # === Representation invariants ===
    # Each item in the list _cashiers must be a type of checkout line
    # There is always at least one open line that has space for a customer

    def __init__(self, filename):
        """Initializes a GroceryStore from a configuration file <filename>.

        @type self: GroceryStore
        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """
        self._cashiers = []
        self.customer_count = 0
        self.max_wait = 0

        with open(filename, 'r') as file:
            self.config = json.load(file)
        # <config> is now a dictionary with the keys 'cashier_count',
        # 'express_count', 'self_serve_count', and 'line_capacity'.
        # create instances of StandardCheckout class according to 'cashier_count
        # and 'line_capacity' from <config>
        i = 0
        while i < self.config['cashier_count']:
            self._cashiers.append(
                StandardCheckout(self.config['line_capacity']))
            i += 1
        # create instances of ExpressCheckout class according to 'cashier_count'
        # and 'line_capacity' from <config>
        i = 0
        while i < self.config['express_count']:
            self._cashiers.append(ExpressCheckout(self.config['line_capacity']))
            i += 1
        # create instances of SelfCheckout class according to 'cashier_count'
        # and 'line_capacity' from <config>
        i = 0
        while i < self.config['self_serve_count']:
            self._cashiers.append(SelfCheckout(self.config['line_capacity']))
            i += 1

    def assign_line(self, customer):
        """ Return the line index that a given customer should join.

        @type self: GroceryStore
        @type customer: Customer
            The customer is of type Customer.
        @rtype: int
            Represents the index of the line in list _cashiers that the
            given customer should join.
        """
        if not customer.num_items > 0:
            raise ZeroItemError
        else:
            # line_index represents the best line for <customer>
            line_index = None
            # check if <customer> has less than 8 items
            if customer.num_items < 8:
                # iterate through the list of cashiers
                for line in self._cashiers:
                    # check if a line is available
                    if line.open and line.curr_cap <= line.max_cap:
                        # if it's the first line we're checking
                        if line_index is None:
                            # update line_index
                            line_index = self._cashiers.index(line)
                        else:
                            # we compare the iterated line with the line at
                            # line_index
                            # current_cap represents the amount of customers
                            # in the line at line_index
                            current_cap = self._cashiers[line_index].curr_cap
                            # if capacities are the same
                            if line.curr_cap == current_cap:
                                # compare indices
                                # if the iterated line has a lower index
                                if self._cashiers.index(line) < line_index:
                                    # its index becomes line_index
                                    line_index = self._cashiers.index(line)
                            # if a iterated line has a lower capacity than
                            # current_cap
                            elif line.curr_cap < current_cap:
                                # its index becomes line_index
                                line_index = self._cashiers.index(line)
            # customer has 8 or more items
            else:
                for line in self._cashiers:
                    # customer cannot join an ExpressCheckout line
                    if line.open and line.curr_cap != line.max_cap and \
                                    type(line) != ExpressCheckout:
                        if line_index is None:
                            line_index = self._cashiers.index(line)
                        else:
                            current_cap = self._cashiers[line_index].curr_cap
                            if line.curr_cap == current_cap:
                                if self._cashiers.index(line) < line_index:
                                    line_index = self._cashiers.index(line)
                            elif line.curr_cap < current_cap:
                                line_index = self._cashiers.index(line)
        return line_index

    def is_empty(self, line_index):
        """ Return True iff the line is empty.

        @type line_index: int
            The index of the cashier line we are checking.
        @rtype: bool
        """
        return len(self._cashiers[line_index]._customers) == 0

    def add_customer(self, cid, num_items, line_index):
        """ Add a customer to a checkout line specified by <line_index> in the
        grocery store.

        @type cid: str
            The unique id given to a customer.
        @type num_items: int
            The number of items the customer is carrying.
        @type line_index: int
            The index of the line we are adding the customer to.
            Is always going to be referencing an available line since its value
            is calculated using the assign_line method.
        @rtype: None
        """
        # if the line at the given index is empty
        if self.is_empty(line_index):
            # find line at <line_index>
            line = self._cashiers[line_index]
            # initialize an instance of customer with <cid> and <num_items>
            # add customer to the specified line
            line._customers.append(Customer(cid, num_items))
        # if the line is not empty
        else:
            # find line at <line_index>
            line = self._cashiers[line_index]
            # update the <next> attribute of the last customer at specified line
            # to point to the <cid> of the customer we are adding
            line._customers[-1].next = cid
            # add the customer to the specified line
            line._customers.append(Customer(cid, num_items))
        # increment the customer_count of the store by 1
        self.customer_count += 1
        # increment the <customer_count> of the GroceryStore by 1
        line.curr_cap += 1
        # increment the <curr_cap> of the specified line by 1

    def find_customer(self, cid):
        """ Returns the Customer object using the <cid> attribute.

        @type cid: str
            The unique str id of the customer.
        @rtype: Customer
            The actual Customer object the <cid> references.
        """
        # iterate through cashiers
        for cashier in self._cashiers:
            # iterate through customers
            for customer in cashier._customers:
                # if the name of the customer matches <cid>
                if cid == customer.cid:
                    return customer

    def find_cashier_line_index(self, cid):
        """ Return the index of the line the customer is currently in.

        @type cid: str
            The unique str id of the customer.
        @rtype: int
            The index of the line the customer is currently in.
        """
        # iterate through cashiers
        for i in range(len(self._cashiers)):
            # iterate through customers
            for customer in self._cashiers[i]._customers:
                # if customer name matches <cid>
                if cid == customer.cid:
                    # return index
                    return i

    def find_cashier_line(self, index):
        """Returns the Cashier object in GroceryStore with the given index.

        @type index: int
            The index of the checkout line.
        @rtype: StandardCheckout | ExpressCheckout | SelfCheckout

        """
        return self._cashiers[index]

    def remove_customer_front(self, line_index):
        """ Removes the customer at the front of the line specified by <line_index>.

        @type line_index: int
            The index of the checkout line.
        @return: None
        """
        # find the customer at the front of the line at <line_index>
        customer = self._cashiers[line_index]._customers[0]
        # calculate the customer's wait time using his <finish_time> and
        # <join_time> attributes
        wait_time = customer.finish_time - customer.join_time
        # if the customer is the first to finish checkout
        if self.max_wait == 0:
            # his/her wait_time becomes max_wait
            self.max_wait = wait_time
        # compare wait_time
        else:
            # if customer's wait_time is larger than max_wait
            if self.max_wait < wait_time:
                # max_wait becomes customer's wait_time
                self.max_wait = wait_time
        # find the line from which we are removing the customer
        line = self._cashiers[line_index]
        # remove customer from <_customers> list of the specified line
        line._customers.remove(line._customers[0])
        # subtract 1 from the <curr_cap> of the specified line
        line.curr_cap -= 1

    def remove_customer_back(self, line_index):
        """ Removes the customer from the back of the line specified by <line_index>.

        @type line_index: int
            The index of the checkout line.
        @rtype: None
        """
        # find the line at <line_index>
        line = self._cashiers[line_index]
        # remove the customer at the end of the specified line
        line._customers.pop()
        # set the <next> attribute of the last person to point to None
        line._customers[-1].next = None
        # subtract 1 from the <curr_cap> of the specified line
        line.curr_cap -= 1
        # subtract 1 from the <customer_count> attribute of GroceryStore
        self.customer_count -= 1

    def close_c(self, line_index):
        """ Close the checkout line specified by the <line_index>.

        @type line_index: int
            The index of the checkout line.
        @return: None
        """
        # list_customers is list of customer that needs to be sent to a new line
        list_customers = []
        # find line at <line_index>
        line = self._cashiers[line_index]
        # change the line attribute <open> to False
        line.open = False
        # iterate through the list of customers until only 1 customer remains
        while len(line._customers) > 1:
            # find the last customer
            last_customer = line._customers[-1]
            # add the last customer to list_customers
            list_customers.append(last_customer)
            # remove the last customer from the line
            self.remove_customer_back(line_index)
        return list_customers

    def process_c(self, line_index):
        """ Return the time it takes for the cashier to process the customer at
        the front of the line specified by <line_index>.

        @type line_index: int
            The index of the checkout line.
        @rtype: int
            The value representing the processing time of the customer
            at the front of the line.
        """
        processing_time = None
        # find the line object at <line_index>
        line = self._cashiers[line_index]
        # if line is of type StandardCheckout
        if type(line) == StandardCheckout:
            # update processing_time
            processing_time = line._customers[0].num_items + 7
        # if line is of type ExpressCheckout
        elif type(line) == ExpressCheckout:
            # update processing_time
            processing_time = line._customers[0].num_items + 4
        # if line is of type SelfCheckout
        elif type(line) == SelfCheckout:
            # update processing_time
            processing_time = 2 * (line._customers[0].num_items) + 1
        return processing_time

    def set_join_time(self, customer, timestamp):
        """ Update the <join_time> attribute of the <customer> object. Should
        not be called on a <customer> that has an already modified <join_time>
        attribute.

        @type customer: Customer
        @type timestamp: int
            The time customer joined the line.
        @rtype: None
        """
        # make sure that the customer's <join_time> is set to None
        if customer.join_time is None:
            # update customer's <join_time>
            customer.join_time = timestamp

    def set_finish_time(self, customer, timestamp):
        """ Update the <finish_time> attribute of the <customer> object.
        Should not be called on a <customer> that has an already modified
        <finish_time> attribute.

        @type customer: Customer
        @type timestamp: int
            The time customer finished checking out.
        @rtype: None
        """
        # make sure that the customer's <finish_time> is set to None
        if customer.finish_time is None:
            # update customer's <finish_time>
            customer.finish_time = timestamp


class StandardCheckout:
    """ A standard checkout line.

    === Attributes ===
    @type max_cap: int
        The maximum capacity of the line.
    @type curr_cap: int
        The current capacity of the line.
    @type open: bool
        Whether or not the line is available for customers to join.
    """
    # === Private attributes ===
    # @type _customers : list[Customer]
    #    This list keeps track of the customers currently present at the line.

    def __init__(self, max_cap):
        """ Initializes a StandardCheckout line.

        @type self: StandardCheckout
        @type max_cap: int
            The maximum capacity of the line.

        >>> c = StandardCheckout(10)
        >>> c.max_cap
        10
        >>> c.curr_cap
        0
        >>> c.open
        True
        >>> c = StandardCheckout(9)
        >>> c.max_cap
        9
        >>> c.curr_cap
        0
        >>> c.open
        True
        """

        self._customers = []
        self.max_cap = max_cap
        self.curr_cap = 0
        self.open = True


class ExpressCheckout:
    """ An express checkout line.

    === Attributes ===
    @type max_cap: int
        The maximum capacity of the line.
    @type curr_cap: int
        The current capacity of the line.
    @type open: bool
        Whether or not the line is available for customers to join.
    """
    # === Private attributes ===
    # @type _customers: list[Customer]
    #    This list keeps track of the customers currently present at the line.

    def __init__(self, max_cap):
        """ Initializes an ExpressCheckout line.

        @type self: ExpressCheckout
        @type max_cap: int
            The maximum capacity of the line.

        >>> c = ExpressCheckout(10)
        >>> c.max_cap
        10
        >>> c.curr_cap
        0
        >>> c.open
        True
        >>> c = ExpressCheckout(9)
        >>> c.max_cap
        9
        >>> c.curr_cap
        0
        >>> c.open
        True
        """
        self._customers = []
        self.max_cap = max_cap
        self.curr_cap = 0
        self.open = True


class SelfCheckout:
    """ A self-serve checkout line.

    === Attributes ===
    @type max_cap: int
        The maximum capacity of the line.
    @type curr_cap: int
        The current capacity of the line.
    @type open: bool
        Whether or not the line is available for customers to join.
    """
    # === Private attributes ===
    # @type _customers: list[Customer]
    #    This list keeps track of the customers currently present at the line.

    def __init__(self, max_cap):
        """ Initializes a SelfCheckout line.

        @type self: SelfCheckout
        @type max_cap: int
            The maximum capacity of the line.

        >>> c = SelfCheckout(10)
        >>> c.max_cap
        10
        >>> c.curr_cap
        0
        >>> c.open
        True
        >>> c = SelfCheckout(9)
        >>> c.max_cap
        9
        >>> c.curr_cap
        0
        >>> c.open
        True
        """
        self._customers = []
        self.max_cap = max_cap
        self.curr_cap = 0
        self.open = True


class Customer:
    """ A customer.

    === Attributes ===
    @type cid: str
        The unique string assigned to a customer.
    @type num_items: int
        The number of items the customer is carrying.
    @type join_time: int
        The time at which the customer joined a checkout line.
    @type finish_time: int
        The time at which the customer finished checking out.
    @type next: None | str
        Points to the <cid> of the customer standing behind.
        Points to None if no customer is standing behind.
    """

    def __init__(self, cid, num_items):
        """ Initializes a Customer.

        @type cid: str
            The unique string representing a customer.
        @type num_items: int
            The number of items the customer is carrying.

        >>> jerry = Customer('jerry', 8)
        >>> jerry.num_items
        8
        >>> jerry.cid
        'jerry'
        """
        self.cid = cid
        self.num_items = num_items
        self.join_time = None
        self.finish_time = None
        self.next = None


class ZeroItemError(Exception):
    pass
