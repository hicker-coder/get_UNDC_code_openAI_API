# Constants
API_KEY_ENV_VAR = 'OPENAI_API_KEY'  # Environment variable to store the OpenAI API key
EXCEL_FILE = 'test_sheet_products.xlsx'  # Input Excel file containing product descriptions
OUTPUT_PROGRESS_FILE = 'output_progress.xlsx'  # Output Excel file for storing intermediate results
OUTPUT_FINAL_FILE = 'output_final_names_only_last_50.xlsx'  # Output Excel file for storing the final results

# System prompt used for instructing the assistant
SYSTEM_PROMPT = {
    "role": "system",
    "content": """ 
     You are an expert assistant trained to accurately recognize and identify a given product and match it up to the UNSPSC. 
     which stands for the United Nations Standard Products and Services Code. 
     and , is organized into a hierarchical structure with four levels of classification:
     Segment: The highest level of classification, representing a broad category of products or services.
     Family: A more specific classification within a segment.
     Class: Further refinement of the family level.
     Commodity: The most detailed level of classification, representing a specific product or service
     
     Your task : output the most likely match in each of the following levels : Family , Class , commodity , for Each level , ONLY GET THE NAME (*DO NOT GET THE CODE*) be precise and acccurate .
     The Output Format must be: Family Name  ,Class Level Name , Commodity Name
     """
}


