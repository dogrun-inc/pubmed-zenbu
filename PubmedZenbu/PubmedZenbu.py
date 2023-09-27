# encoding: utf-8
import requests
import argparse
import subprocess
import xml.etree.ElementTree as ET
import csv
import eutils
import use_gpt
import os
import pandas as pd
import yaml

with open('config.yml', 'r') as yml:
    config = yaml.safe_load(yml)

ncbi_api_key = config['pubmed_search']['ncbi_api_key']
search_query = config['pubmed_search']['search_query']
oldest_year = config['pubmed_search']['search_oldest_year']
texttouse = config['pubmed_search']['which_text_to_use']

if ncbi_api_key == None or search_query == None or oldest_year == None or texttouse == None:
    config_path = os.path.abspath('./config.yml')
    print(f"please fill in your config file at {config_path}")
else:
    pass


# parser = argparse.ArgumentParser(description="This script extracts information from PubMed abstract and title using openai.")
# parser.add_argument("arguments.csv", help="arguments csv file") 
# # parser.add_argument("prompt", help="your prompt for openai")
# args = parser.parse_args()

# TODO WSL2で試したらなぜかうまくいかない。。

    
    
def main():
    """
    """
    # esearchを使ってpmidのリストを取得する
    years_list = eutils.get_yearlist(oldest_year)
    pmids_alllist = []
    for a_year in years_list:
        a_year = int(a_year)
        # id取得
        print(a_year)
        id_res = eutils.call_esearch(search_query, a_year)
        count = eutils.get_text_by_tree("./Count", id_res)
        if count > 10000:
            print(f"PMID has exceeded 10000 for {a_year} in this search query. Consider to change your search query keywords. Otherwise, please use EDirect to obtain PMIDs (NCBI recommended)")
            print(f"the number of pmids: {count}")
            break
        else:
            pass

        for id in id_res.findall("./IdList/Id"):
            pmid = id.text
            pmids_alllist.append(pmid)

    pmids_alllist = list(set(pmids_alllist))
    # print(pmids_alllist)
    # epostとefetchを使ってabstractとtitleを取得する
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
        except:
            print("error at {}".format(api2))
            continue

        # AbstractとTitleの文章を取得して、結合する
        for element in tree2.iter("PubmedArticle"):
            for_join = []
            pmid = eutils.get_text_by_tree("./MedlineCitation/PMID", element)
            print(f"\npmid: {pmid}....")
            element_title = element.find("./MedlineCitation/Article/ArticleTitle")
            prompt = config['openai']['prompt']
            for_join.append(prompt)
            title = "".join(element_title.itertext())
            title = "\n'" + title
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
                except:
                    abstract = ""      
                abstract = abstract + "'" 
                for_join.append(abstract)
                input = ",".join(for_join)
            else:
                print("please choose either title or abstract for 'which_text_to_use' in your config.yml")
                # use openAI api
            
            if config['openai']['openai_api_key'] == None:
                print("Not using OpenAI. PubMed search results will be exported")
                print({"pmid":pmid,"gpt_or_PubmedResults":input})
                extracted_data.append({"pmid":pmid,"gpt_or_PubmedResults":openai_result})
            else:
                try:
                    openai_result = use_gpt.gpt_api(input, config['openai']['openai_api_key'])
                    print({"pmid":pmid,"gpt_or_PubmedResults":openai_result})
                    # プログラムが急停止してしまう事態のバックアップとして、途中経過を出力する
                    extracted_data.append({"pmid":pmid,"gpt_or_PubmedResults":openai_result})
                except:
                    print("error at openai_api: {}".format(pmid))
        
    # export the result as csv
    field_name = [
        "pmid",
        "gpt_or_PubmedResults",
    ]

    with open(
        f"./extract_result_{config.date}.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(extracted_data)

if __name__ == "__main__":
    main()
