#in this file, i need to do two tasks where each task has this kind of workflow:
'''
- read from a .txt file named "file" from the same directory as the src code
- make a detailed prompt for a local llm, using the content of the file 
- get the response from the llm
- write the response to a new .txt file named "file_response.txt"
- save the file in the same directory
'''
import sys
import os

def read_transcript_to_generate_propositions(file,llm):
    response=None
    return response
def read_propositions_to_generate_json_summary(propositions : str,llm):
    response=None
    return response

if __name__=="__main__":
    if(len(sys.argv)!=2):
        print("usage: python llm.py input_transcript.txt ; ensure input_transcript.txt is in the same directory")
        sys.exit(1)
    input_file=sys.argv[1]
    propositions=read_transcript_to_generate_propositions(input_file,None)
    json_summary=read_propositions_to_generate_json_summary(propositions,None)
    base,ext=input_file.rsplit('.',1)
    output_file=f"{base}_json.txt"
    with open(output_file,"w",encoding="utf-8") as f:
        f.write(json_summary)
    