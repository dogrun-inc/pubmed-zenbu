import requests
import xml.etree.ElementTree as ET

def get_yearlist(minyear:int):
    """
    Parameters:
    --------
    minyear: int

    Returns:
    --------
    years_list: list
        A list of year starting from minyear to 2024.
    """
    years_list = [str(x) for x in range(minyear, 2025)]
    return years_list


def call_esearch(query_str: str, mindate:int) -> ET.Element:
    """
    description:
    ------
    Since a maximum of 10,000 records can be retrieved at a time, the 'mindate' is specified to obtain PMIDs year by year.

    Parameters:
    ------
        query_str: str
        mindate: int

    Returns:
    ------
        tree: xml
    """
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query_str}&retmax=10000&mindate={mindate}&maxdate={mindate}"
    tree = use_eutils(url)
    return tree


def call_esearch_pmc(query_str: str, mindate:int) -> ET.Element:
    """
    description:   
    ------
    Since a maximum of 10,000 records can be retrieved at a time, the 'mindate' is specified to obtain PMCIDs year by year.

    Parameters:
    ------
        query_str: str
        retmax: int
        year: int

    Returns:
    ------
        tree: xml
    """
    pmc_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term={query_str}&retmax=10000&mindate={mindate}&maxdate={mindate}"
    tree = use_eutils(pmc_url)
    return tree


def generate_chunked_id_list(id_list, max_len) -> list:
    """
    Parameters:
    ------
    id_list: list
        A list that will be splited

    max_len: int
        Number of elements in the list after splitting

    Returns:
    ------
    list_of_id_list: list
        A list contains splited lists
    """
    return [id_list[i : i + max_len] for i in range(0, len(id_list), max_len)]


def get_text_by_tree(treepath, element):
    """
    Parameters:
    ------
    treepath: str
        path to the required information

    element: str
        tree element

    Returns:
    ------
    information: str
        parsed information from XML

    None: Null
        if information could not be parsed.

    """
    if element.find(treepath) is not None:
        return element.find(treepath).text
    else:
        return ""


def use_eutils(api_url):
    """
    function to use API

    Parameters:
    -----
    api_url: str
        URL for API

    Return:
    --------
    tree: xml
        Output in XML

    """
    req = requests.get(api_url, timeout=30) # add timeout to avoid hanging
    req.raise_for_status()
    tree = ET.fromstring(req.content)
    return tree