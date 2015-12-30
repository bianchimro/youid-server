from channels import Group
#from hub.decorators import http_token_user

#@http_token_user
def ws_add(message):
    print message.content
    
