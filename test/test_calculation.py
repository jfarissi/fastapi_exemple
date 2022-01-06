from app.calculation import add,substract,divide,Multiply , BankAccount,InsufficientFound
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected",[
(2,3,5),
(7,2,9),
(15,3,18)
])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected
    
def test_substract():
    assert substract(5,3) == 2


def test_miltiply():
    assert Multiply(5,3) == 15

def test_divide():
    assert divide(10,2) == 5

def test_bank_initiale_amount(bank_account):
    # balanceaccount = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # defaultamount = BankAccount()
    assert zero_bank_account.balance == 0

def test_witdraw_amount(bank_account):
    # defaultamount = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_diposit_amount(bank_account):
    # defaultamount = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_interest_amount(bank_account):
    # defaultamount = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited,withdrew,expected",[
(200,100,100),
(700,200,500),
(1500,300,1200)
])
def test_transaction_bank_account(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_InsuffisientFound(bank_account):
    with pytest.raises(InsufficientFound):
        bank_account.withdraw(200)