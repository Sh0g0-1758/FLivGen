import syft as sy
sy.requires(">=0.8.3,<0.8.4")
node = sy.orchestra.launch(name="my-domain", port=8080, dev_mode=True, reset=True)

guest_domain_client = node.client
# Print this to see the few commands that are available for the guest client
print(guest_domain_client)
# This will return the public credentials of the guest client
guest_credentials = guest_domain_client.credentials
print(guest_credentials)