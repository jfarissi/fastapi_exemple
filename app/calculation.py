import pytest


def add(num1 : int, num2 : int):
    return num1 + num2 

def substract(num1 : int, num2 : int):
    return num1 - num2 

def Multiply(num1 : int, num2 : int):
    return num1 * num2 

def divide(num1 : int, num2 : int):
    return num1 / num2 

class InsufficientFound(Exception):
    pass

class BankAccount():
    def __init__(self,Starting_balance=0):
        self.balance = Starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self,amount):
        if(amount > self.balance):
            raise InsufficientFound("Insuffisante found in account") 
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1 
    
