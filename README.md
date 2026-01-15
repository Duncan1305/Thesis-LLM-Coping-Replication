# Thesis-LLM-Coping-Replication
Replication package for Master's Thesis: Optimizing LLM-Generated Coping Plans (Ghent University 2026).
--------------------------------------------------------------------------------
1. OVERVIEW
--------------------------------------------------------------------------------
This repository contains the source code, system prompts, and raw output data for the master's thesis: 
"The Effectiveness of Prompt Engineering for Optimizing LLM-Generated Coping Plans".

The project systematically evaluates the alignment between GPT-4o-mini and human experts/users regarding the relevance of coping strategies for physical activity barriers. It specifically investigates the "paradox of reasoning" by comparing three prompt engineering conditions:
1. Baseline (Zero-Shot)
2. Chain-of-Thought (CoT)
3. Synthetic Population (Persona Simulation)

Total combinations analyzed: N = 1,564.

--------------------------------------------------------------------------------
2. CONTENTS
--------------------------------------------------------------------------------
/Scripts
   - generate_LLM_scores_OVERALL.py   : Main pipeline. iteraties over the dataset, sends prompts to OpenAI API, and saves responses.
   - analysis_metrics.py              : (Optional) Scripts used to calculate Pearson correlations and generating distribution plots.
   - requirements.txt                 : List of required Python libraries (pandas, numpy, openai, matplotlib, etc.).

/Prompts
   - prompts.txt                      : The exact system instructions used for the three experimental conditions.

/Output_Data
   - experiment1_baseline.csv         : Raw output data (Scores 0-100) for the Baseline condition.
   - experiment2_cot.csv              : Raw output including generated rationales for the CoT condition.
   - experiment3_synthetic.csv        : Raw output including aggregated persona perspectives.

--------------------------------------------------------------------------------
3. DATA AVAILABILITY (GROUND TRUTH)
--------------------------------------------------------------------------------
This study utilizes the "COPPER" dataset and user ratings from Braun et al. (2024) as the ground truth benchmark. 
Due to licensing and privacy protocols, the input data is NOT hosted in this repository.

To reproduce this study, you must acquire the user ratings file:
1. Refer to the work of Braun et al. (2024) or the associated repository: https://github.com/stvsever/MappingComparison_UsersLLM
2. Locate the file: `relevance_by_combination.csv`
3. Place this file in the local directory: `/OSF_data/relevance/`

--------------------------------------------------------------------------------
4. EXPERIMENTAL CONDITIONS & FINDINGS
--------------------------------------------------------------------------------
The study tested three distinct prompting strategies on GPT-4o-mini. 
Summary of findings included in this package:

- **Baseline:** Achieved moderate alignment (r = .35 for 'Always Relevant').
- **Chain-of-Thought:** Resulted in a performance drop (r = .22), indicating "over-rationalization" of pragmatic tasks.
- **Synthetic Population:** Recovered baseline performance (r = .34) and increased variance, but introduced some stereotypical hallucinations.

--------------------------------------------------------------------------------
5. HOW TO RUN
--------------------------------------------------------------------------------
Prerequisites:
- Python 3.9+
- OpenAI API Key (with access to gpt-4o-mini)

Setup:
1. Install dependencies:
   pip install -r requirements.txt

2. Environment Variable:
   Create a .env file or export your key:
   export OPENAI_API_KEY='sk-...'

3. Execution:
   To run a specific condition, modify the `PROMPT_SELECTION` variable in the script to match the desired ID in `prompts.txt`.
   
   python generate_LLM_scores_OVERALL.py

--------------------------------------------------------------------------------
6. ETHICAL DECLARATION
--------------------------------------------------------------------------------
No personal data from the original participants was sent to the OpenAI API. 
All inputs were anonymized, generic, aggregated descriptions of barriers and behavior change techniques. 
The generated data consists purely of synthetic AI judgments.

