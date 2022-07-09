class Headers:
  @classmethod
  def default_request_headers(request):
    request.headers['Accept-Encoding'] = "gzip, deflate, sdch"
    request.headers['Connection']      = 'keep-alive'
    request.headers['Accept']          = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    request.headers['Referrer']        = 'https://www.google.com'
    request.headers['Accept-Language'] = 'en-US,en;q=0.8'
    request.headers['User-Agent']      = 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'