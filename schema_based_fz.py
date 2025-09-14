import pandas as pd
import os
import json
from rapidfuzz import process
from sentence_transformers import SentenceTransformer, util

# === Step 1: Load schema to get correct column order ===
schema_path = "PREDEFINED_EXCELSHEET.xlsx"  # schema excel sheet
schema_df = pd.read_excel(schema_path, sheet_name=0)
schema_columns = schema_df.columns.tolist()

# === Step 2: Folder containing new Excel/CSV files ===
folder_path = r"testing_sheets"  # folder with excel/csv files

# === Step 3: Initialize embedding model ===
model = SentenceTransformer("all-MiniLM-L6-v2")  # light & fast

def map_column(col_name, schema_columns, fuzzy_threshold=80, embed_threshold=0.65):
    """Map one incoming column to schema using fuzzy + embeddings"""
    # 1. Fuzzy match
    match, score, _ = process.extractOne(col_name, schema_columns)
    if score >= fuzzy_threshold:
        return match

    # 2. Semantic similarity (embeddings)
    col_emb = model.encode(col_name, convert_to_tensor=True)
    schema_emb = model.encode(schema_columns, convert_to_tensor=True)
    sims = util.cos_sim(col_emb, schema_emb)[0]
    best_idx = sims.argmax().item()
    best_score = sims[best_idx].item()
    if best_score >= embed_threshold:
        return schema_columns[best_idx]

    # 3. No good match
    return None

def auto_map_columns(incoming_columns, schema_columns):
    mapping = {}
    for col in incoming_columns:
        mapped = map_column(col, schema_columns)
        mapping[col] = mapped
        print(f"🔹 Mapped '{col}' → '{mapped}'")  # log mapping
    return mapping


# === Step 4: Collect all data ===
all_data = []
excel_count = 0
csv_count = 0

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    if file.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)
        excel_count += 1
    elif file.endswith(".csv"):
        df = pd.read_csv(file_path, encoding="latin1", on_bad_lines="warn")
        csv_count += 1
    else:
        continue

    # ✅ Auto-map columns
    mapping = auto_map_columns(df.columns.tolist(), schema_columns)
    df = df.rename(columns=mapping)

    # ✅ Drop duplicate columns (keep first)
    df = df.loc[:, ~df.columns.duplicated()]

    # ✅ Align to schema
    df = df.reindex(columns=schema_columns, fill_value="not found")

    all_data.append(df)

# === Step 5: Combine all into one dataframe ===
final_df = pd.concat(all_data, ignore_index=True)

# === Step 6: Save combined file (Excel & JSON) ===
final_df.to_excel("combined_output.xlsx", index=False)
final_df.to_json("combined_output.json", orient="records", indent=4)

# === Step 7: Print summary ===
print(f"✅ Processing complete.")
print(f"Excel files processed: {excel_count}")
print(f"CSV files processed: {csv_count}")
print("Output saved: combined_output.xlsx & combined_output.json")
