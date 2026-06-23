def get_first_error(e):
  err=e.errors()[0]
  field=err["loc"][0]
  msg=err['msg']
  return f"{field}:{msg}"
  