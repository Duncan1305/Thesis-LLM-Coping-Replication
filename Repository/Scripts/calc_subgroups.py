import pandas as pd
import numpy as np
import os
import re

# ==========================================
# 1. CONFIGURATIE (PADEN)
# ==========================================

PATH_ORIGINAL_CSV = r"OSF_data/relevance/relevance_by_combination.csv"
PATH_BASELINE = r"results/PROMPT_BASELINE/full/llm_raw_results.xlsx"
PATH_COT = r"results/PROMPT_CHAIN_OF_THOUGHT/full/llm_raw_results.xlsx"
PATH_PERSONA = r"results/PROMPT_SYNTHETIC_POPULATION/full/llm_raw_results.xlsx"

# ==========================================
# 2. FUNCTIE VOOR BEREKENING
# ==========================================

def calculate_group_correlations(name, path_llm, df_ground_truth):
    print(f"\n" + "="*60)
    print(f" RESULTATEN VOOR: {name}")
    print("="*60)
    
    if not os.path.exists(path_llm):
        print(f"⚠️ BESTAND NIET GEVONDEN: {path_llm}")
        return

    # Laad LLM resultaten
    df_llm = pd.read_excel(path_llm)
    
    # We zorgen dat de dataframes gelijk lopen (indien test_mode aan stond)
    limit = min(len(df_llm), len(df_ground_truth))
    df_llm = df_llm.iloc[:limit].reset_index(drop=True)
    df_gt = df_ground_truth.iloc[:limit].reset_index(drop=True)

    # Maak een gecombineerde dataframe voor analyse
    # We gebruiken de kolomnamen die we net in het vorige script hebben vastgelegd
    data = pd.DataFrame({
        'Group_Barrier': df_gt['barrier_group'],
        'Group_Coping': df_gt['Category'],
        # Ground Truth (User)
        'GT_Always': df_gt['Rel_Always'].astype(float),
        'GT_Conditions': df_gt['Rel_CC'].astype(float),
        'GT_Never': df_gt['Rel_Never'].astype(float),
        # LLM Scores
        'LLM_Always': df_llm['Score_Always'].astype(float),
        'LLM_Conditions': df_llm['Score_Conditions'].astype(float),
        'LLM_Never': df_llm['Score_Never'].astype(float)
    })

    def print_corrs(group_col, label):
        groups = data[group_col].dropna().unique()
        print(f"\n>>> Correlaties per {label}:")
        print(f"{'Subgroep':<45} | {'Always':<8} | {'Cond':<8} | {'Never':<8}")
        print("-" * 80)
        
        results = []
        for g in groups:
            subset = data[data[group_col] == g]
            if len(subset) < 3: continue # Te weinig data voor correlatie

            # Pearson r berekenen
            # .fillna(0) vangt gevallen op waar er geen variatie is
            r_always = subset['GT_Always'].corr(subset['LLM_Always'])
            r_cond = subset['GT_Conditions'].corr(subset['LLM_Conditions'])
            r_never = subset['GT_Never'].corr(subset['LLM_Never'])
            
            print(f"{g[:43]:<45} | {r_always:7.2f} | {r_cond:7.2f} | {r_never:7.2f}")
            results.append({'subgroup': g, 'always': r_always, 'cond': r_cond, 'never': r_never})
        
        # Bereken ook even het gemiddelde van de subgroepen
        avg_always = np.nanmean([res['always'] for res in results])
        print(f"{'GEMIDDELDE VAN SUBGROEPEN':<45} | {avg_always:7.2f} | {'-':<8} | {'-':<8}")

    # Voer de berekening uit voor Barrier groepen en Coping groepen
    print_corrs('Group_Barrier', 'BARRIÈRE CATEGORIE')
    print_corrs('Group_Coping', 'COPING STRATEGIE CATEGORIE')

# ==========================================
# 3. UITVOEREN
# ==========================================
if __name__ == "__main__":
    print("Bezig met laden van data...")
    try:
        df_gt = pd.read_csv(PATH_ORIGINAL_CSV)
        print(f"✅ Grond truth geladen: {len(df_gt)} combinaties.")
    except Exception as e:
        print(f"❌ Fout bij laden CSV: {e}")
        exit()

    # Roep de functie aan voor de 3 condities
    calculate_group_correlations("1. BASELINE (Pure Intuïtie)", PATH_BASELINE, df_gt)
    calculate_group_correlations("2. CHAIN OF THOUGHT (Redenering)", PATH_COT, df_gt)
    calculate_group_correlations("3. SYNTHETIC POPULATION (Diversiteit)", PATH_PERSONA, df_gt)