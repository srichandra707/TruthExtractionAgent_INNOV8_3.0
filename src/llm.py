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
import ollama

def read_transcript_to_generate_propositions(file,llm="mistral"):
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
    prompt=f"""
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
    {transcript}
    """
    response=ollama.chat(
        model=llm,
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return response["message"]["content"]
def read_propositions_to_generate_json_summary(propositions : str,llm="mistral"):
    prompt=f"""
    You are a truth-extraction engine. 
    You will be given a list of propositional statements made by a single speaker, across 5 sessions.

    format of the propositions:
    1.
    - First propositional statement in session 1.
    ...
    2.
    - First propositional statement in session 2.
    ...
    3.
    - First propositional statement in session 3.
    ...
    4.
    - First propositional statement in session 4.
    ...
    5.
    - First propositional statement in session 5.
    ...

    The sessions have a general trend:
    • Session 1: Confident lies told with practiced ease 
    • Session 2: Small cracks appear as pressure mounts 
    • Session 3: Desperate elaboration of false stories 
    • Session 4: Truth and lies become tangled as panic sets in 
    • Session 5: Final revelations mixed with last-ditch deceptions

    Your task is to analyze the statements and based on the emotion (if any), contradictions to previous statements, and general plausibility,
    determine which are the most likely true possibilities and fill the json format given by:

    {
        "shadow_id": "string",
        "revealed_truth": {
            "programming_experience": "string",
            "programming_language": "string",
            "skill_mastery": "string",
            "leadership_claims": "string",
            "team_experience": "string",
            "skills and other keywords": "List[String]",
        },
        "deception_patterns": [{
            "lie_type": "string",
            "contradictory_claims": "List[String]",
        },...
        ],
    }

    Rules:
    - If two statements contradict (e.g., "I have 6 years of experience." vs. "I have 3 years of experience."), 
    assume the LAST one is true, and the earlier one is a lie.
    Reason: the reason we consider a later statement about a subject a fact is because it becomes degraded in value, like from “managed” and “seasoned engineer” to “intern” is a degradation, hence why we need to consider later statements that contradict with previous statements as the actual truth values.
    - If a statement is vague or uncertain (e.g., "I probably know Kubernetes."), treat it as a lie.
    - Do NOT invent facts not present.
    - Mark all non-contradictory statements as true. and use them for filling the json.

    Example Input:
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

    Example Output:
    {
        "shadow_id":"atlas_2025",
        "revealed_truth":{
            "programming_experience":"0-2 years",
            "programming_language":"calico",
            "skill_mastery":"basic-intermediate",
            "leadership_claims":"fabricated",
            "team_experience":"worked with senior managers",
            "skills and other keywords":["calico","DNS logs"]
        },
    "deception_patterns":[
        {
            "lie_type": "leadership_inflation",
            "contradictory_claims":["managed","intern"]
        },...(many more)
    ],
    }

    Statements:
    {propositions}
    """
    response=ollama.chat(
        model=llm,
        messages=[
            {"role":"user","content":prompt}
        ]
    )   
    return response["message"]["content"]

if __name__=="__main__":
    if(len(sys.argv)!=2):
        print("usage: python llm.py input_transcript.txt ; ensure input_transcript.txt is in the same directory")
        sys.exit(1)
    input_file=sys.argv[1]
    propositions=read_transcript_to_generate_propositions(input_file,"mistral")
    json_summary=read_propositions_to_generate_json_summary(propositions,"mistral")
    base,ext=input_file.rsplit('.',1)
    output_file=f"{base}_json.txt"
    with open(output_file,"w",encoding="utf-8") as f:
        f.write(json_summary)
    