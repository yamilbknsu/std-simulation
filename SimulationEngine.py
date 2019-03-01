# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 08:44:54 2019

@author: rodel
"""
import numpy as np


class AbstractSimulator(object):
    def __init__(self):
        self.events = None

    def insert(self, e):  # Insert an abstract event
        self.events.insert(e)

    def cancel(self, e):  # AbstractEvent
        raise NotImplementedError("Method not implemented")


class Event:
    def __init__(self):
        self.time = None

    def __lt__(self, y):
        if isinstance(y, Event):
            return self.time < y.time
        else:
            raise ValueError('This is not an event')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Simulator(AbstractSimulator):
    def __init__(self):
        super().__init__()
        self.time = None

    def now(self):
        return self.time

    def do_all_events(self):
        while self.events.size() > 0:
            e = self.events.remove_first()
            print('the EVENT being dequed is {} for subjectID {} at time {}'.format(e.command, e.id, e.time))
            self.time = e.time
            e.execute(self)


class ListQueue:
    elements = list()

    def insert(self, x):
        i = 0
        while i < len(self.elements) and self.elements[i] < x:
            i += 1
        self.elements.insert(i, x)

    def remove_first(self):
        if len(self.elements) == 0:
            return None
        x = self.elements.pop(0)
        return x

    def remove(self, x):
        for i in range(len(self.elements)):
            if self.elements[i] == x:
                return self.elements.pop(i)
        return None

    def size(self):
        return len(self.elements)


class Random(object):
    def __init__(self):
        pass

    @staticmethod
    def exponential(mean):
        return -mean * np.log(np.random.rand())

    @staticmethod
    def bernulli(p):
        return np.random.rand() < p


class Message(Event):
    def __init__(self, message_handler, command=None):
        self.messageHandler = message_handler
        self.command = command
        self.simulator = None
        self.id = None

    def set_(self, command, time, sID):
        self.command = command
        self.time = time
        self.id = sID

    def execute(self, simulator):
        self.simulator = simulator
        if self.command and self.messageHandler:
            self.messageHandler.handle(self)


class SexualPerson:
    memberID = 0

    display = None
    population = list()
    countSusceptible = 0
    countInfectious = 0
    countRecovered = 0
    countPartnerships = 0
    meanInfectiousDuration = 2
    meanPartnershipDuration = 0.5
    meanInterContactTime = 1
    meanInterPartnershipTime = 0.3
    probabilityOfExtrapartnershipContact = 0.1

    SUSCEPTIBLE = 0
    INFECTIOUS = 1
    RECOVERED = 2

    def __init__(self, disease_state=None):
        SexualPerson.memberID += 1
        self.subjectID = SexualPerson.memberID
        self.diseaseState = disease_state
        print('I am subjectID {} being created with disease state {}'.format(self.subjectID, self.diseaseState))
        self.partnershipMessage = Message(self)
        self.diseaseMessage = Message(self)
        self.contactMessage = Message(self)
        self.partner = None
        self.incrementCount()
        SexualPerson.population.append(self)

    def infectiousDuration(self):
        return Random.exponential(SexualPerson.meanInfectiousDuration)

    def interContactTime(self):
        return Random.exponential(SexualPerson.meanInterContactTime)

    def partnershipDuration(self):
        return Random.exponential(SexualPerson.meanPartnershipDuration)

    def interPartnershipTime(self):
        return Random.exponential(SexualPerson.meanInterPartnershipTime)

    def incrementCount(self):
        if self.diseaseState == SexualPerson.SUSCEPTIBLE:
            SexualPerson.countSusceptible += 1
            print("HIT INCREMENT Susceptible number {} and subjetID {} ".format(SexualPerson.countSusceptible,
                                                                                self.subjectID))
        elif self.diseaseState == SexualPerson.INFECTIOUS:
            SexualPerson.countInfectious += 1
            print("HIT INCREMENT Infectious number {} and subjetID {}".format(SexualPerson.countInfectious,
                                                                              self.subjectID))
        else:
            SexualPerson.countRecovered += 1
            print(
                "HIT INCREMENT recovered number {} and subjetID {}".format(SexualPerson.countRecovered, self.subjectID))

    def decrementCount(self):
        if self.diseaseState == SexualPerson.SUSCEPTIBLE:
            SexualPerson.countSusceptible -= 1
            print("HIT DECREMENT Susceptible number {} and subjetID {} ".format(SexualPerson.countSusceptible,
                                                                                self.subjectID))
        elif self.diseaseState == SexualPerson.INFECTIOUS:
            SexualPerson.countInfectious -= 1
            print("HIT DECREMENT Infectious number {} and subjetID {}".format(SexualPerson.countInfectious,
                                                                              self.subjectID))
        else:
            SexualPerson.countRecovered -= 1
            print(
                "HIT DECREMENT recovered number {} and subjetID {}".format(SexualPerson.countRecovered, self.subjectID))

    def changeDiseaseState(self, diseaseState):
        self.decrementCount()
        self.diseaseState = diseaseState
        self.incrementCount()

    def handle(self, message):
        # print(message.command)
        if message.command == "recover":
            self.recover(message.simulator)
        elif message.command == "contact":
            self.contact(message.simulator)
        elif message.command == "endPartnership":
            self.endPartnership(message.simulator)
        elif message.command == "beginPartnership":
            self.beginPartnership(message.simulator)
        elif message.command == "recover":
            self.recover(message.simulator)
        else:
            print("Unknown command ", message.command)
        if SexualPerson.display != None:
            SexualPerson.display.handle(message)

    def infect(self, simulator):
        print("++++++++++++++++")
        print("INFECTEE subjetID {}".format(self.subjectID))
        self.changeDiseaseState(SexualPerson.INFECTIOUS)
        self.diseaseMessage.set_('recover', simulator.now() + self.infectiousDuration(), self.subjectID)
        print("I am subject {} and I will {} by time {}".format(self.subjectID, self.diseaseMessage.command,
                                                                self.diseaseMessage.time))
        simulator.insert(self.diseaseMessage)
        self.contactMessage.command = 'contact'
        self.contactMessage.time = simulator.now() + self.interContactTime()
        print("I am subject {} and I will {} someone by time {}".format(self.subjectID, self.contactMessage.command,
                                                                        self.contactMessage.time))
        simulator.insert(self.contactMessage)

    def contact(self, simulator):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$')
        contactee = None
        if self.partner == None:
            contactee = SexualPerson.selectFromPopulation()
            print(
                "I am subjectID {} and I DO NOT have partner and I was contacted by a partner with subjectID {}".format(
                    contactee.subjectID, self.subjectID))
        else:
            if Random.bernulli(SexualPerson.probabilityOfExtrapartnershipContact):
                contactee = SexualPerson.selectFromPopulation()
                print("I am subjectID {} and I was contacted by subjectID {} to have an AFFAIR".format(
                    contactee.subjectID, self.subjectID))

            else:
                contactee = self.partner
                print("I am subjectID {} and I have been contacted by my partner with subjectID {}".format(
                    contactee.subjectID, self.subjectID))

        if contactee.diseaseState == SexualPerson.SUSCEPTIBLE:
            contactee.infect(simulator)

    def recover(self, simulator):
        print('-------------------------')
        print("I am {} and I am happy because I have recovered by time {}".format(self.subjectID, simulator.now()))
        simulator.cancel(self.contactMessage)
        self.changeDiseaseState(SexualPerson.RECOVERED)

    def beginPartnership(self, simulator):
        person = None
        while person == None or person == self:
            person = SexualPerson.selectFromPopulation()
        self.partner = person
        # print('I am member {} and beeing selected to have a partner'.format(self.partner.subjectID))
        self.partner.beginPartnershipWith(self, simulator)
        self.partnershipMessage.set_('endPartnership', simulator.now() + self.partnershipDuration(), self.subjectID)
        simulator.insert(self.partnershipMessage)
        SexualPerson.countPartnerships += 1

    def beginPartnershipWith(self, person, simulator):
        self.partner = person
        # print('I am {} and my partner is {}'.format(self.subjectID, self.partner.subjectID))
        simulator.cancel(self.partnershipMessage)

    def endPartnership(self, simulator):
        self.partner.endPartnershipWith(self, simulator)
        self.partner = None
        self.partnershipMessage.set_('beginPartnership', simulator.now() + self.interPartnershipTime(), self.subjectID)
        simulator.insert(self.partnershipMessage)
        SexualPerson.countPartnerships -= 1

    def endPartnershipWith(self, person, simulator):
        self.partner = None
        self.partnershipMessage.set_('beginPartnership', simulator.now() + self.interPartnershipTime(), self.subjectID)
        simulator.insert(self.partnershipMessage)

    @staticmethod
    def clearPopulation():
        SexualPerson.population = list()
        SexualPerson.countSusceptible = 0
        SexualPerson.countInfectious = 0
        SexualPerson.countRecovered = 0
        SexualPerson.countPartnerships = 0

    @staticmethod
    def selectFromPopulation():
        return SexualPerson.population[int(len(SexualPerson.population) * np.random.rand())]

    @staticmethod
    def printSummary(simulator):
        info = {'time': '{:.2f}'.format(simulator.now()), 'susceptible': SexualPerson.countSusceptible,
                'infectious': SexualPerson.countInfectious, 'recovered': SexualPerson.countRecovered,
                'partnership': SexualPerson.countPartnerships}
        print(
            "At simulation time {time} there are {susceptible} susceptible, {infectious} infectious, {recovered} recovered and {partnership} partnerships".format(
                **info))


class PrintDisplay:
    def handle(self, message):
        SexualPerson.printSummary(message.simulator)


class SexualDiseaseSimulator(Simulator):
    SexualPerson.display = PrintDisplay()

    def __init__(self, events, initialSusceptible, initialInfectious, initialRecovered, initialPartnerships):
        super().__init__()
        self.events = events
        self.initialSusceptible = initialSusceptible
        self.initialInfectious = initialInfectious
        self.initialRecovered = initialRecovered
        self.initialPartnerships = initialPartnerships
        self.time = 0

        SexualPerson.clearPopulation()

        for i in range(self.initialSusceptible):
            SexualPerson(SexualPerson.SUSCEPTIBLE)
        for i in range(self.initialInfectious):
            person = SexualPerson(SexualPerson.INFECTIOUS)
            person.infect(self)
        for i in range(self.initialPartnerships):
            person = SexualPerson.selectFromPopulation()
            # print('I am member {} and beeing selected to have a partner'.format(person.subjectID))
            if person.partner == None:
                person.beginPartnership(self)

    def cancel(self, e):
        return self.events.remove(e)


if __name__ == "__main__":
    sim = SexualDiseaseSimulator(ListQueue(), 25, 5, 0, 0)
    sim.do_all_events()

# set PATH=%PATH%;C:\users\rodel\anaconda3\envs\py35\lib\site-packages\multinetx\
# set PATH=%PATH%;C:\users\rodel\anaconda3\envs\py35\lib\site-packages\pymnet
# set PATH=%PATH:C:\users\rodel\anaconda3\envs\py35\lib\site-packages\pymnet;=%
