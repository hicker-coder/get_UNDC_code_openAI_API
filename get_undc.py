import pandas as pd
import openai
import concurrent.futures
import random
import time
import os
from constants import API_KEY_ENV_VAR,SYSTEM_PROMPT,OUTPUT_FINAL_FILE,OUTPUT_PROGRESS_FILE,EXCEL_FILE



# Set the OpenAI API key from environment variable
openai.api_key ="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"

def extract_product_info(df, index):
    """
    Extracts product name from the dataframe at the given index.
    """
    return df.iloc[index]['Product Name Splitted']


def chat_get_keyword(product_name):  # this function is used to send the query and get the answer from the chatbot
    # Construct the conversation

    conversation = [
        SYSTEM_PROMPT,
        # Try not to make this too long or will cost a lot more since the tokens are repeated every request.
        {"role": "user",
         "content": f"Think step by step and get for the following product  "
                    f" Find the the most likely match in the following levels Family , Class , commodity in UNSPSC. classification. "
                    f" output format: Family Name ,Class Name , Commodity Name (be precise and acccurate)   (* GIVE NAMES ONLY , NO CODES *), "
                    f" Example of desired output : DO THIS : (Dairy products and eggs , Cheese , Processed cheese) , "
                    f" DO NOT DO THIS (Family Name : Dairy products and eggs , Class Name : Cheese , Commodity Name : Processed cheese)"
                    f":'{product_name}'"}

    ]

    # Make API call
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview", temperature=0.1,
        # Temperature lets you control the randomness of the output. Lowering the the temp will make it more consistent with output.
        messages=conversation
    )

    # Extract the HS code from the response
    product = response.choices[0].message.content

    return product, conversation

def chat_get_keyword_external(product_name):
    """
    Wraps chat_get_keyword within a timeout mechanism.
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(chat_get_keyword, product_name)
            return future.result(timeout=60)
    except concurrent.futures.TimeoutError:
        return "Timeout", None

def main():
    """
    Main function to process the dataframe and interact with OpenAI API.
    """
    df = pd.read_excel(EXCEL_FILE)
    error_log = []
    start_index = 0

    for index in range(start_index, len(df)):
        product_name = extract_product_info(df, index)
        try:
            print(f"Picked {product_name}, index: {index}")

            answer, conversation = chat_get_keyword_external(product_name)
            time.sleep(0.1)
            df.at[index, 'Model_Answer'] = answer

            print(f"Chose '{answer}' for {product_name}")
            print("------------------------------")

            if index % 5 == 0:
                df.to_excel(OUTPUT_PROGRESS_FILE)

        except Exception as e:
            print(f"Error with product {product_name} at index {index}: {e}")
            error_log.append((index, str(e)))

    df.to_excel(OUTPUT_FINAL_FILE)

if __name__ == "__main__":
    main()

