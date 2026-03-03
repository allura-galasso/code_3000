import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    quasi_identifiers = ['age', 'gender', 'zip3']
    # Merge datasets on the quasi-identifiers
    merged = pd.merge(anon_df, aux_df, on=quasi_identifiers, how='inner')
    # Identify records that are unique on BOTH sides (1:1 matches)
    # This prevents counting ambiguous matches as successful re-identifications
    match_counts_anon = merged.groupby('anon_id')['anon_id'].transform('count')
    match_counts_aux = merged.groupby('name')['name'].transform('count')
    # Filter for uniqueness
    unique_matches = merged[(match_counts_anon == 1) & (match_counts_aux == 1)].copy()
    # Rename 'name' to 'matched_name' as per docstring requirements
    return unique_matches[['anon_id', 'name']].rename(columns={'name': 'matched_name'})

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(anon_df) == 0:
        return 0.0
    return len(matches_df) / len(anon_df)
