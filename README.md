# pubmed-zenbu
1. This tool collects literature data (title_only or title_and_abstract) of your interest.
2. This tool also extracts metadata from literature data using ChatGPT if you set the parameters.

## How to use 
- `conda create -n pubmedzenbu python=3.9`
- Create a `config.yml` 
```
# Sample config.yml

pubmed_search:
  # (Required) NCBI API Key
  ncbi_api_key: YOUR_NCBI_API_KEY
  # (Required) Search query to obtain the PubMed articles of your interest
  search_query: prime editing pig
  # (Required) How far back in time you want to search. 
  search_oldest_year: 2010
  # (Required) `title` or `abstract`. If choose `abstract`, it means you get the joined string of title and abstract.
  which_text_to_use: title
openai:
  # (Required) if use, add 'yes'. If not, keep it empty.
  use_openai: yes
  # (Optional) if use_openai is true, add your openai_api_key. Otherwise, keep it empty.
  openai_api_key: YOUR_OPENAI_API_KEY
  # (Optional) Prompt to ask ChatGPT. If you don't use it, keep it empty.
  prompt: "extract gene and species from the following text \n"
  # (Required) Set the output path. If use_openai is false, literature data will be written out.
  output_path: ./extract_result_20231004.csv
```

- `pubmedzenbu PATH_TO_YOUR_config.yml_FILE`