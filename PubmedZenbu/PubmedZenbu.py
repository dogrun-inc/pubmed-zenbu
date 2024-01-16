# encoding: utf-8
import os
import sys
import re
import argparse
import csv
import json
import xml.etree.ElementTree as ET
import requests.exceptions
import yaml
from . import eutils
from . import use_gpt

# argument parser (get config file path)
parser = argparse.ArgumentParser(
    description="This script extracts information from PubMed abstract and title using openai.")
parser.add_argument("config_path", help="path to config.yml")
args = parser.parse_args()


def load_config(config_path="config.yml"):
    """_summary_
    Args:
        config_path (str, optional): _description_. Defaults to "config.yml".
    Returns:
        _type_: _description_
    """
    with open(config_path, encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    return config


# TODO For some reason, it doesn't work when I try it on WSL2...

def main():
    """__summary__

    """
    #Create a log file
    log_file = 'log.txt'
    log_file_handler = open(log_file, 'a', encoding='utf-8')
    stdout_original = sys.stdout
    config = load_config(args.config_path)
    sys.stdout = stdout_original
    #Get information from config.yml
    ncbi_api_key = config['search']['ncbi_api_key']
    query_database = config['search']['query_database']
    search_query = config['search']['search_query']
    oldest_year = config['search']['search_oldest_year']
    texttouse = config['search']['which_text_to_use']
    output_path = config['openai']['output_path']
    if ncbi_api_key is None or search_query is None or oldest_year is None or texttouse is None:
        print(f"please fill in your config file at {args.config_path}")
    else:
        pass
    #Retrieve a list of pmids using esearch
    years_list = eutils.get_yearlist(oldest_year)
    ids_alllist = []
    for a_year in years_list:
        a_year = int(a_year)
        #Retrieve ids
        print(a_year)

        if query_database == "pubmed":
            id_res = eutils.call_esearch(search_query, a_year)
        elif query_database == "pmc":
            id_res = eutils.call_esearch_pmc(search_query, a_year)
        else:
            print("Invalid query_database value. It should be either 'pubmed' or 'pmc'.")
            break
        # print(id_res)  
        count = eutils.get_text_by_tree("./Count", id_res)
        count = int(count)
        # print(count)
        if count > 10000:
            print(
                f"ID has exceeded 10000 for {a_year} in this search query. Consider to change your search query keywords. Otherwise, please use EDirect to obtain IDs (NCBI recommended)")
            print(f"the number of ids: {count}")
            break
        else:
            pass
        # Get ID list using esearch
        for article_id in id_res.findall("./IdList/Id"):
            idlist = article_id.text
            ids_alllist.append(idlist)

########## Get Pubmed information ##########

#Retrieved abstract and title using epost and efetch
    if query_database == "pubmed":
        pmids_alllist = list(set(ids_alllist))
        # print(pmids_alllist)
        print(f"number of pmids: {len(pmids_alllist)}")
        list_of_chunked_pmids = eutils.generate_chunked_id_list(pmids_alllist, 190)
        extracted_data = []

        for a_chunked_pmids in list_of_chunked_pmids:
            # print(a_chunked_pmids)
            pmid_str = a_chunked_pmids
            pmid_str = ",".join(a_chunked_pmids)

            epost_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed&id={}&api_key={}"
            api1 = epost_params.format(pmid_str, ncbi_api_key)
            print(api1)
            print("connected to epost...")

            tree1 = eutils.use_eutils(api1)
            webenv = ""
            webenv = tree1.find("WebEnv").text
            esummary_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&WebEnv={}&query_key=1&api_key={}&retmode=xml"
            api2 = esummary_params.format(webenv, ncbi_api_key)
            print("connected to efetch...")
            print(api2)
            try:
                tree2 = eutils.use_eutils(api2)
            except (requests.exceptions.RequestException, ET.ParseError) as e:
                print(f"error at {api2}, error message: {e}")

        for element in tree2.iter("PubmedArticle"):
            for_join = []
            pmid = eutils.get_text_by_tree("./MedlineCitation/PMID", element)
            print(f"\npmid: {pmid}....")
            element_title = element.find(
                "./MedlineCitation/Article/ArticleTitle")
            title = "".join(element_title.itertext())
            if config['openai']['use_openai']:
                prompt = config['openai']['prompt']
                for_join.append(prompt)
                title = "\n'" + title
                for_join.append(title)
            else:
                for_join.append(title)

            if texttouse == "title":
                print("title only")
                input = ",".join(for_join)
            elif texttouse == "abstract":
                print("title and abstract")
                element_abstract = element.find(
                    "./MedlineCitation/Article/Abstract"
                )
                try:
                    abstract = "".join(element_abstract.itertext())
                except TypeError as error:
                    print(f"Error: {error}")
                    abstract = ""
                abstract = abstract + "'"
                for_join.append(abstract)
                input = ",".join(for_join)
            else:
                print(
                    "please choose either title or abstract for 'which_text_to_use' in your config.yml")
                # use openAI api
            if config['openai']['use_openai'] is None:
                print("Not using OpenAI. PubMed search results will be exported")
                print({"pmid": pmid, "gpt_or_PubmedResults": input})
                extracted_data.append(
                    {"pmid": pmid, "gpt_or_PubmedResults": input})
            else:
                print("using OpenAI. stdout will be written in log.txt as a backup")
                sys.stdout = open(log_file, 'a', encoding='utf-8')
                try:
                    openai_result = use_gpt.gpt4_api(
                        input, config['openai']['openai_api_key'])
                    print({"pmid": pmid, "gpt_or_PubmedResults": openai_result})
                    #Output intermediate results as a backup in case the program suddenly stops
                    extracted_data.append(
                        {"pmid": pmid, "gpt_or_PubmedResults": openai_result})
                except (requests.exceptions.RequestException, ET.ParseError) as e:
                    print(f"error at {api2}, error message: {e}")
        # output the log file
        log_file_handler.close()
        #export the result as csv
        field_name = [
            "pmid",
            "gpt_or_PubmedResults",
        ]

########## Get PMC information ##########

#Retrieved information using epost and efetch
    elif query_database == "pmc":
        pmcids_alllist = list(set(ids_alllist))
        print(f"number of PMCids: {len(pmcids_alllist)}")
        list_of_chunked_pmcids = eutils.generate_chunked_id_list(pmcids_alllist, 190)
        extracted_pmc_data = []

        for a_chunked_pmcids in list_of_chunked_pmcids:
            pmcids_str = a_chunked_pmcids
            pmcids_str = ",".join(a_chunked_pmcids)

            # Get Webenv
            epost_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pmc&id={}&api_key={}"
            pmc_api1 = epost_params.format(pmcids_str, ncbi_api_key)
            print("connected to epost for PMC...")
            print(pmc_api1)
            tree1 = eutils.use_eutils(pmc_api1)
            webenv = tree1.find("WebEnv").text
            # Use Webenv to get information
            efetch_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&WebEnv={}&query_key=1&api_key={}&retmode=xml"
            pmc_api2 = efetch_params.format(webenv, ncbi_api_key)
            print("connected to efetch for PMC...")
            print(pmc_api2)

            try:
                tree2 = eutils.use_eutils(pmc_api2)
            except (requests.exceptions.RequestException, ET.ParseError) as e:
                print(f"error at {pmc_api2}, error message: {e}")
        # search PMC ID tag
                        
        for element in tree2.iter("article"):
            for_join = []
            pmcid = eutils.get_text_by_tree(
                './front/article-meta/article-id[@pub-id-type="pmc"]', element)
            print(f"\npmcid: {pmcid}....")
            element_title_pmc = element.find(
                './front/article-meta/title-group/article-title') # PMC XML tag
            pmc_title = "".join(element_title_pmc.itertext()) # The function to use the use_gpt function for titles is omitted.
            
            # retrieve from article body
            # 1.introduction
            if texttouse == "introduction":
                print("Getting an Introduction section...")
                # Preferentially searches for "sec-type" tags
                element_introduction = element.find('./body/sec[@sec-type="intro"]')
                if element_introduction is not None:
                    body_text = "".join(element_introduction.itertext()).replace("\n", "")# Remove line breaks
                else:
                    print('"sec-type" tag not found. Searching for "sec" tags...')
                    for sec in element.findall('./body/sec'):
                        title = sec.find('./title')
                        if title is not None and re.search("Introduction",
                                                           title.text,
                                                           re.IGNORECASE): # Ignore case (e.g., introduction, Introduction)
                            body_text = "".join(sec.itertext()).replace("\n", "") # Remove line breaks
                            break
            else:
                print(
                    "please choose section")
                break
            #use openAI api
            if config['openai']['use_openai']:
                print("using OpenAI. stdout will be written in log.txt as a backup")
                sys.stdout = open(log_file, 'a', encoding='utf-8')
                try:
                    processed_text = use_gpt.gpt4_api(body_text, config['openai']['openai_api_key'])
                    extracted_pmc_data.append({"PMCID": pmcid, 
                                            "Article_title": pmc_title, 
                                            "description": processed_text})
                except (requests.exceptions.RequestException, ET.ParseError) as e:
                    print(f"error at {api2}, error message: {e}")
            else:
                print("Not using OpenAI. PMC search results will be exported")
                extracted_pmc_data.append({"PMCID": pmcid, 
                                          "Article_title": pmc_title, 
                                          "description": body_text})
            log_file_handler.close()
            field_name_pmc = ["PMCID",
                              "Article_title", 
                              "description"]  
    
    else:
        print(f"Error: '{query_database}' is not a valid database option. Please choose 'pubmed' or 'pmc'.")

    _, file_extension = os.path.splitext(output_path) # Get the extension of the output file
    if file_extension.lower() == ".json":
        print("exporting as json...")
        with open(output_path, "w", encoding="utf-8") as jsonfile:
            if query_database == "pubmed":
                json.dump(extracted_data, jsonfile, ensure_ascii=False, indent=4)
            elif query_database == "pmc":
                json.dump(extracted_pmc_data, jsonfile, ensure_ascii=False, indent=4)
    elif file_extension.lower() == ".csv":
        print("exporting as csv...")
        with open(output_path, "w", encoding="utf-8") as csvfile:
            if query_database == "pubmed":
                writer = csv.DictWriter(csvfile, fieldnames=field_name)
                writer.writeheader()
                writer.writerows(extracted_data)
            elif query_database == "pmc":
                writer = csv.DictWriter(csvfile, fieldnames=field_name_pmc)
                writer.writeheader()
                writer.writerows(extracted_pmc_data)

if __name__ == "__main__":
    main()
