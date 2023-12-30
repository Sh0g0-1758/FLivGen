SYFT_VERSION = ">=0.8.2.b0,<0.9"
package_string = f'"syft{SYFT_VERSION}"'

import syft as sy
sy.requires(SYFT_VERSION)
from syft import autocache
import pandas as pd

# Launch a fresh domain server named "test-domain-1" in dev mode on the local machine
node = sy.orchestra.launch(name="test-domain-1", port="auto", dev_mode=True, reset=True)

domain_client = node.login(email="info@openmined.org", password="changethis")

data_subjects = domain_client.data_subject_registry.get_all()
print(data_subjects)

country = sy.DataSubject(name="Country", aliases=["country_code"])
canada = sy.DataSubject(name="Canada", aliases=["country_code:ca"])
germany = sy.DataSubject(name="Germany", aliases=["country_code:de"])
spain = sy.DataSubject(name="Spain", aliases=["country_code:es"])
france = sy.DataSubject(name="France", aliases=["country_code:fr"])
japan = sy.DataSubject(name="Japan", aliases=["country_code:jp"])
uk = sy.DataSubject(name="United Kingdom", aliases=["country_code:uk"])
usa = sy.DataSubject(name="United States of America", aliases=["country_code:us"])
australia = sy.DataSubject(name="Australia", aliases=["country_code:au"])
india = sy.DataSubject(name="India", aliases=["country_code:in"])

country.add_member(canada)
country.add_member(germany)
country.add_member(spain)
country.add_member(france)
country.add_member(japan)
country.add_member(uk)
country.add_member(usa)
country.add_member(australia)
country.add_member(india)

country.members
response = domain_client.data_subject_registry.add_data_subject(country)
print(response)
# Lets look at the data subjects added to the data
data_subjects = domain_client.data_subject_registry.get_all()
print(data_subjects)
assert len(data_subjects) == 10

canada_dataset_url = "https://github.com/OpenMined/datasets/blob/main/trade_flow/ca%20-%20feb%202021.csv?raw=True"
df = pd.read_csv(autocache(canada_dataset_url))
print(df)

# private data samples
ca_data = df[0:10]
ca_data
# Mock data samples
mock_ca_data = df[10:20]
mock_ca_data

dataset = sy.Dataset(name="Canada Trade Value")
dataset.set_description("Canada Trade Data")
dataset.add_citation("Person, place or thing")
dataset.add_url("https://github.com/OpenMined/datasets/tree/main/trade_flow")
dataset.add_contributor(name="Andrew Trask", 
                        email="andrew@openmined.org",
                        note="Andrew runs this domain and prepared the dataset metadata.")

dataset.add_contributor(name="Madhava Jay", 
                        email="madhava@openmined.org",
                        note="Madhava tweaked the description to add the URL because Andrew forgot.")
dataset.contributors
assert len(dataset.contributors) == 2