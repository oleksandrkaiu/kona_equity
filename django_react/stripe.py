import stripe
from enum import Enum

from django.conf import settings


class StripeSource(Enum):
    CARD = 'card'
    BANK = 'bank_account'

class Stripe():
  stripe.api_key = settings.STRIPE_SECRET_KEY
  
  @staticmethod
  def create_customer(fullname: str, cust_email: str):
    success = False
    response = None

    try:
      customer_obj = stripe.Customer.create(
        email=cust_email,
        name=fullname,
      )
      success = True
      response = customer_obj.id
    except stripe.error.InvalidRequestError as ex:
      print(ex.error.message)
      response = ex.error.message
    except Exception as ex:
      print(vars(ex))
      response = "Something went wrong!\nTry again later!"
    return success, response

  # returns bank object if no error found
  @staticmethod
  def verify_bank(customer_id: str, source_id: str, amounts: list):
    verified_status = "verified"
    success = False
    try:
      is_success, bank_account = Stripe.get_source(customer_id, source_id)
      if not is_success:
        return success, bank_account  # error returned from get_source

      # check if already verified
      if bank_account.status == verified_status:
        return success, "Account is already verified"

      bank_account.verify(amounts=amounts)
      # check if the account verification is successful
      if bank_account.status != verified_status:
        return success, "Couldn't verify the account, please try again later!"

      # verification is successful, return bank object
      success = True
      return success, bank_account
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while verifying the bank!\nTry again later!"

  @staticmethod
  def get_source_list(customer_id: str, source_type: str, limit: int = 100):
    success = False
    try:
      source_list = stripe.Customer.list_sources(customer_id, object=source_type, limit=limit)['data']
      success = True
      return success, source_list
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while getting the sources list!\nTry again later!"

  @staticmethod
  def get_source(customer_id: str, source_id: str):
    success = False
    try:
      source = stripe.Customer.retrieve_source(customer_id, source_id)
      success = True
      return success, source
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while getting the source!\nTry again later!"

  @staticmethod
  def add_source(customer_id: str, source_token: str):
    success = False
    try:
      # remove all cards before adding any other
      # Stripe.remove_all_sources(customer_id, StripeSource.CARD.value)
      created_source = stripe.Customer.create_source(customer_id, source=source_token)
      success = True
      return success, created_source
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while adding the source!\nTry again later!"

  @staticmethod
  def update_card(customer_id: str, source_token: str, kwargs):
    success = False
    try:
      updated_source = stripe.Customer.modify_source(customer_id, source_token, **kwargs)
      success = True
      return success, updated_source
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while updating the source!\nTry again later!"

  @staticmethod
  def remove_source(customer_id: str, source_id: str):
    success = False
    try:
      removed_source = stripe.Customer.delete_source(customer_id, source_id)
      success = True
      return success, removed_source
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      return success, ex.error.message
    except Exception as ex:
      print(vars(ex))
      return success, "Something went wrong while removing the source!\nTry again later!"

  @staticmethod
  def remove_all_sources(customer_id: str, source_type: str = StripeSource.CARD.value):
    success, sources = Stripe.get_source_list(customer_id, source_type)
    if not success:
      return success, sources
    
    # remove all sources one by one
    for source in sources:
      Stripe.remove_source(customer_id, source.id)

    # return list of removed sources and success to true
    return success, sources

  @staticmethod
  def charge_payment(customer_id: str, receipt_email: str, amount: float):
    charge_amount = int(amount*100)   # stripe accepts amount as integer only
    success = False
    response = None
    
    try:
      stripe_customer = stripe.Customer.retrieve(customer_id)
      if stripe_customer.default_source != None:
        stripe_charge = stripe.Charge.create(amount=charge_amount, currency=settings.STRIPE_CURRENCY
                                  , customer=stripe_customer.id, source=stripe_customer.default_source
                                  , receipt_email=receipt_email)
        if stripe_charge.status == 'succeeded' and stripe_charge.paid:
          success = True
        else:
          # any other failure reason for charge
          response = stripe_charge.failure_message
      else:
        response = 'Please attach a card to proceed!'
    except stripe.error.CardError as ex:
      print(ex)
      response = ex.error.message
    except stripe.error.InvalidRequestError as ex:
      print(ex)
      response = ex.error.message
    except Exception as ex:
      print(vars(ex))
      response = "Something went wrong while charging the card!\nTry again later!"
    return success, response