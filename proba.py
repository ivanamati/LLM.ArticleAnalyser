from langchain_community.document_loaders import UnstructuredURLLoader

# loader = UnstructuredURLLoader(urls=["https://www.foi.unizg.hr/hr/karijera-na-foiju#block-block-75"])
# loader = UnstructuredURLLoader(urls=["https://www.yourfirm.de/job/ascon-systems-holding-gmbh/ai-solutions-engineer-gn/yf24686680/?utm_source=linkedin_de&utm_medium=unpaid-partner&utm_campaign=free"])


link="https://blog.google/products/gemini/google-gemini-new-features-july-2024/"
loader = UnstructuredURLLoader(urls=[link])

data = loader.load()
print(data[0])


# from bs4 import BeautifulSoup
# import requests

# url = "https://www.foi.unizg.hr/hr/karijera-na-foiju#block-block-75"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
