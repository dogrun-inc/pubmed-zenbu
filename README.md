# pubmed-zenbu
1. This tool collects literature data (title_only or title_and_abstract) of your interest.
2. This tool also extracts metadata from literature data using ChatGPT if you set the parameters.

## How to use 
- `conda create -n pubmedzenbu python=3.9` or `pip install PubmedZenbu`
- Create a `config.yml` 

## Sample config.yml (1) (When making inquiries to PubMed...)

```YAML
search:
  ncbi_api_key: YOUR_NCBI_API_KEY # (Required) NCBI API Key
  query_database: pubmed # (Required) 
  search_query: prime+editing+AND+pig # (Required) Search query to obtain the PubMed articles of your interest
  search_oldest_year: 2010  # (Required) How far back in time you want to search. 
  which_text_to_use: title # (Required) `title` or `abstract`. If choose `abstract`, it means you get the joined string of title and abstract.
openai:
  use_openai: yes # (Required) if use, add 'yes'. If not, keep it empty.
  model: gpt3.5 # (Optional) gpt3.5(gpt-3.5-turbo-instruct) or gpt4(gpt-4-1106-preview)
  openai_api_key: YOUR_OPENAI_API_KEY   # (Optional) if use_openai is true, add your openai_api_key. Otherwise, keep it empty.
  prompt: "extract gene and species from the following text \n"  # (Optional) Prompt to ask ChatGPT. If you don't use it, keep it empty.
  output_path: ./extract_result_20231004.csv   # (Required) Set the output path. If use_openai is false, literature data will be written out. CSV format or JSON format.
```

## Sample config.yml (2) (When making inquiries to PMC...)

```YAML
search:
  ncbi_api_key: YOUR_NCBI_API_KEY # (Required) NCBI API Key
  query_database: pmc # (Required)
  search_query: prime+editing+AND+pig # (Required) Search query to obtain the PubMed articles of your interest
  search_oldest_year: 2010  # (Required) How far back in time you want to search. 
  which_text_to_use: introduction # (Required) introduction, materials and methods, results, or discussion
openai:
  use_openai: yes # (Required) if use, add 'yes'. If not, keep it empty.
  model: gpt4 # (Optional) gpt3.5(gpt-3.5-turbo-instruct) or gpt4(gpt-4-1106-preview)
  openai_api_key: YOUR_OPENAI_API_KEY   # (Optional) if use_openai is true, add your openai_api_key. Otherwise, keep it empty.
  prompt: "extract gene and species from the following text \n"  # (Optional) Prompt to ask ChatGPT. If you don't use it, keep it empty.
  output_path: ./extract_result_20231004.json   # (Required) Set the output path. If use_openai is false, literature data will be written out. CSV format or JSON format.
```

## How to run
- `pubmedzenbu <PATH_TO_YOUR_config.yml_FILE>`