import openai
import os
import argparse


parser = argparse.ArgumentParser(description='Generate a prompt for a given paper and table.')
parser.add_argument('--prompt_path', type=str, default = 'prompts/prompt1.txt', help='Path to the prompt file.')
parser.add_argument('--api_key', type=str, default= '', help='Path to the table file.')
parser.add_argument('--output_path', type=str, help='Path to the output file.')
args = parser.parse_args()



def generate_one_shot_prompt(prompt_file, paper_txt):


    prompt = load_text_file(prompt_file)

    with open(paper_file1, 'r') as file:
        paper_txt1 = file.read()
    
    prompt = prompt.replace("[PAPER SPLIT]", paper_txt)

    return prompt

        

def generate_prompt(prompt_file, paper_txt, shots=0, paper_file1 = None, table_file1 = None):

    # read the prompt_file
    with open(prompt_file, 'r') as file:
        prompt = file.read()
        
    prompt = prompt.replace("[PAPER SPLIT]", paper_txt)
   
    return prompt



openai.api_key = args.api_key
# go through all the folders that start with L in data_processing/splitted_papers 
for folder in os.listdir('articles/processed_articles'):
    # if folder name without .json not exist in Jsons/oricessed_processed_data continue
    print(folder)
    if not os.path.exists(f'json_ground_truth/processed/{folder}'):
        continue
    else:
        print(folder)
        if f'{folder}_whole.txt' in os.listdir(args.output_path):
            continue

        # read the articles/all/folder.json file and convert it to txt
        # if 'exp.txt' exist in the folder, use the exp.txt file
        # if 'exp.txt' in os.listdir(f'data_processing/summerized_papers/{folder}'):
        #     with open(f'data_processing/summerized_papers/{folder}/exp.txt', 'r') as file:
        #         paper_txt = file.read()
        #         if len(paper_txt.split()) > 4000:
        #             continue
        #         prompt = generate_prompt(args.prompt_path, paper_txt)
        #         response = openai.ChatCompletion.create(model="gpt-4-0613", messages=[{"role": "system", "content": "You extract information from documents and return json objects"},{"role": "user", "content": prompt}])
        #         output = response["choices"][0]["message"]["content"]
        #         with open(f'{args.output_path}/{folder}_exp.txt', 'w') as file:
        #             file.write(output)
            
            
        #     with open(f'data_processing/summerized_papers/{folder}/result.txt', 'r') as file:
        #         paper_txt = file.read()
        #         # if the paper_text has more than 4000 words then continue
        #         if len(paper_txt.split()) > 4000:
        #             continue
        #         prompt = generate_prompt(args.prompt_path, paper_txt)
        #         response = openai.ChatCompletion.create(model="gpt-4-0613", messages=[{"role": "system", "content": "You extract information from documents and return json objects"},{"role": "user", "content": prompt}])
        #         output = response["choices"][0]["message"]["content"]
        #         with open(f'{args.output_path}/{folder}_result.txt', 'w') as file:
        #             file.write(output)
        # else:
        # if whole.txt does not exist in the folder then continue
        if not os.path.exists(f'articles/processed_articles/{folder}/whole.txt'):
            continue

        with open(f'articles/processed_articles/{folder}/whole.txt', 'r') as file:
            paper_txt = file.read()
            # if the paper_text has more than 4000 words then continue
            if len(paper_txt.split()) > 4000:
                continue
            prompt = generate_prompt(args.prompt_path, paper_txt)
            response = openai.ChatCompletion.create(model="gpt-4-0613", messages=[{"role": "system", "content": "You extract information from documents and return json objects"},{"role": "user", "content": prompt}])
            output = response["choices"][0]["message"]["content"]
            with open(f'{args.output_path}/{folder}_whole.txt', 'w') as file:
                file.write(output)
