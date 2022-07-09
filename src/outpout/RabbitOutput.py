## TODO :: actually implement logging

from .Output import Output
import pika

class RabbitOutput(Output):
  def __init__(
    self,
    _host          = None,
    _port          = None,
    _vhost         = None,
    _credentials   = None,
    _rabbit_params = None
  ) -> None:
    self.host  = _host
    self.port  = _port
    self.vhost = _vhost
    if not (_host and _port and _vhost):
      raise Exception("[RabbitOutput.init] requires Pika parameter to initiate connection.")

    if not _credentials:
      self.credentials = pika.PlainCredentials('', '')
    else:
      self.credentials = _credentials

    if not _rabbit_params:
      self.rabbit_params = {}
    else:
      self.rabbit_params = _rabbit_params

    self.params = pika.ConnectionParameters(
      self.host,
      self.port,
      self.vhost,
      self.credentials
    )


  def send(self, _target, _rabbit_specific_params = None):
    self.conn = pika.BlockingConnection(self.params)
    self.channel = self.conn.channel()
    if _rabbit_specific_params:
      self.channel.basic_publish(
        exchange = _rabbit_specific_params['exchange'],
        routing_key = _rabbit_specific_params['routing_key'],
        body = _target
      )
    else:
      self.channel.basic_publish(
        exchange = self.rabbit_params['exchange'],
        routing_key = self.rabbit_params['routing_key'],
        body = _target
      )
    self.channel.close()
    self.conn.close()