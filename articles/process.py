import json
import os
import argparse
import re

# load arguments

parser = argparse.ArgumentParser()  
parser.add_argument('--directory', type=str, default='input.json', help='input file')  
args = parser.parse_args()


if __name__ == '__main__':


    # go through all the files in the args.directory
    print(args.directory)
    for filename in os.listdir(args.directory):
        with open(f"{args.directory}/{filename}") as f:
            data = json.load(f)

        print(filename)
        # get the number of words in the paper
        with open(f"all/{filename}") as f:
            paper_txt = f.read()
            number_of_words = len(paper_txt.split())
            print(filename)
            print(number_of_words)

        title = data['title']
        abstract = data['abstract']
        body = data['body']
        doi = data['doi']


        # remove .json from filename
        filename = filename[:-5]
        # make a txt file in summerized_papers folder
        if not os.path.exists(f"processed_articles/{filename}"):
            # make directory in the splitted_papers folder
            os.makedirs(f"processed_articles/{filename}")

        if number_of_words < 5000:
            with open(f'processed_articles/{filename}/whole.txt', 'w') as f:
                f.write(str(title))
                f.write(str(abstract))
                
                for section in body:
                    section_title = section[0]
                    section_content = section[1]
                    section_content = str(section_content)

                    # delete the the "\n" in the text and if there are spaces bigger than '    ' delete them
                    # delete the word \n and spaces bigger than '    '
                    section_content = section_content.replace('\\n', '')
                    section_content = section_content.replace('    ', '')

                    if section_title == 'Main' or section_title == 'main' or section_title == 'MAIN':
                        sentences = re.split(r'(?<=[a-km-zA-KM-Z])\.', section_content)
                        # do not split if there is % right after .
                        for sentence in sentences:
                            sentence = sentence + '.'
                            f.write(str(sentence))
                            f.write('\n')    
                    if 'intro' in section_title.lower():
                        sentences = re.split(r'(?<=[a-km-zA-KM-Z])\.', section_content)
                        # do not split if there is % right after .
                        for sentence in sentences:
                            sentence = sentence + '.'
                            f.write(str(sentence))
                            f.write('\n')
                    if 'result' in section_title.lower():
                        sentences = re.split(r'(?<=[a-km-zA-KM-Z])\.', section_content)
                        # do not split if there is % right after .
                        for sentence in sentences:
                            if not any(char.isdigit() for char in sentence):
                                continue
                            else:
                                sentence = sentence + '.'
                                f.write(str(sentence))
                                f.write('\n')
                    if 'conclu' in section_title.lower():
                        continue           


        else:
            continue
            
        


