import time

from .Input import Input
import pika

class RabbitInput(Input):
  def __init__(
    self,
    _username,
    _password,
    _queue,
    _host,
    _port,
    _virtual_host,
    _on_message = None,
    _num_msgs = 10
  ) -> None:
    super().__init__()
    if _username and _password:
      self.credentials = pika.PlainCredentials(
        _username,
        _password
      )


    self.connection_parameters = pika.ConnectionParameters(
      host = _host,
      port = _port,
      virtual_host = _virtual_host
    )
    if self.credentials:
      self.connection_parameters.credentials = self.credentials

    self.on_message = _on_message
    self.num_msgs = _num_msgs
    self.queue = _queue

  def replenish_queue(self):
    self.connection = pika.BlockingConnection(self.connection_parameters)
    self.channel = self.connection.channel()
    for _ in range(self.num_msgs):
      method_frame, header_frame, body = self.channel.basic_get(self.queue)
      if method_frame:
        self.input_queue.append(body)
        self.channel.basic_ack(method_frame.delivery_tag)
    self.connection.close()
