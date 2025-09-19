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
    #input file is in this format:
    '''
    1. 
    First paragraph of the transcript.
    2.
    Second paragraph of the transcript.
    3.
    Third paragraph of the transcript.
    4.
    Fourth paragraph of the transcript.
    5.
    Fifth paragraph of the transcript.
    '''
    with open(file,"r",encoding="utf-8") as f:
        transcript=f.read()
    prompt = """
    You are a transcript parser. 
    I will give you a transcript of 5 paragraphs containing messy phrasing and incomplete sentences. 

    Format of the transcript:
    1. 
    First paragraph of the transcript.
    2.
    Second paragraph of the transcript.
    3.
    Third paragraph of the transcript.
    4.
    Fourth paragraph of the transcript.
    5.
    Fifth paragraph of the transcript.

    Your task is to extract and rewrite the text into a clean list of simple propositional statements. 

    Rules:
    - Statements must be SHORT and DIRECT.
    - Use formats like: "I will do X.", "I will not do X.", "I have Y years of experience.", "I managed this.", "I code in Y.", etc.
    - DO NOT summarize. DO NOT add extra meaning. 
    - RETAIN every claim made in the transcript, EVEN IF CONTRADICTORY TO PREVIOUS STATEMENTS.
    - If the speaker is uncertain, add "(uncertainty because of the 'word')" at the end of the statement.
    - If the speaker is denying something, make sure to include that as a separate statement.
    
    Example Input:
    1.
    I'm a seasoned DevOps engineer specializing in Kubernetes. For the past year, I've been in the trenches, managing our production clusters, personally responsible for our entire networking and security posture.
    2.
    Why Calico? Ha! What else would you use? It's the only serious choice for network policy enforcement at scale. I wrote all our policies from scratch to ensure total service isolation.
    3.
    I'd check the logs. Then maybe the core DNS logs. I'd probably just restart the pod, that usually fixes things.
    4.
    The senior engineer usually handles the network debugging, I just deploy the yaml files he gives me.
    5.
    Okay, it was an internship, it was a summer internship, and I mostly just watched the senior engineers work. I ran some scripts they gave me. I'm not a DevOps engineer, I just want to be one.

    Example Output: 
    1.
    I am a seasoned DevOps engineer specializing in Kubernetes.
    I managed Production clusters since a year.
    I am responsible for our entire networking and security posture.
    2.
    I use Calico for network policy enforcement.
    I wrote all our policies from scratch.
    3.
    I check logs and core dns logs. (uncertainty because of the "maybe")
    I restart pods. (uncertainty because of "probably")
    4.
    The senior engineer handles network debugging.
    I deploy yaml files.
    5.
    I was an intern during a summer internship.
    I just watched senior engineers work.
    I ran scripts given to me.
    I am not a devops engineer.
    I want to be a devops engineer.

    Transcript:
    """ + transcript
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
    