SYFT_VERSION = ">=0.8.2.b0,<0.9"
package_string = f'"syft{SYFT_VERSION}"'
# %pip install {package_string} -q
import syft as sy
sy.requires(SYFT_VERSION)

jane_client = sy.login(email="info@openmined.org", password="changethis")
print(jane_client)

results = jane_client.datasets.get_all()
print(results)
# Test
assert len(results) == 1

dataset = results[0]
print(dataset)

