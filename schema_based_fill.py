import pandas as pd
import os
import json

# === Step 1: Load schema to get correct column order ===
schema_path = "PREDEFINED_EXCELSHEET.xlsx"
schema_df = pd.read_excel(schema_path, sheet_name=0)
schema_columns = schema_df.columns.tolist()

# === Step 2: Folder containing new Excel/CSV files ===
folder_path = r"testexcel"

# === Step 3: Collect all data ===
all_data = []
excel_count = 0
csv_count = 0

for file in os.listdir(folder_path):    
    if file.endswith(".xlsx") or file.endswith(".xls"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)
        excel_count += 1
        

    elif file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, encoding="latin1", on_bad_lines="warn")
        csv_count += 1
        
    # ✅ Align columns to schema order
    df = df.reindex(columns=schema_columns,fill_value="not found")

    # Store in list
    all_data.append(df)
#how many excel and cs file found    
print(f"Excel file found: {file} | Total Excel files are {excel_count}")
print(f"CSV file found: {file} | Total CSV files are {csv_count}")
# === Step 4: Combine all into one dataframe ===
final_df = pd.concat(all_data, ignore_index=True)

# === Step 5: Save combined file (Excel & JSON optional) ===
final_df.to_excel("combined_output.xlsx", index=False)
final_df.to_json("combined_output.json", orient="records", indent=4)

#print("✅ Processing complete. Files saved: combined_output.xlsx & combined_output.json")

"""   # Save as new sheet inside schema workbook
        sheet_name = os.path.splitext(file)[0][:30]  # Excel limit = 31 chars
        with pd.ExcelWriter(schema_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Collect for merging later
        all_data.append(df)

# === Step 5: Merge + Remove duplicates (on Email) ===
combined_df = pd.concat(all_data, ignore_index=True)

if "Email" in combined_df.columns:
    combined_df = combined_df.drop_duplicates(subset=["Email"], keep="first")

# === Step 6: Save deduplicated data in schema workbook ===
with pd.ExcelWriter(schema_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    combined_df.to_excel(writer, sheet_name="Deduplicated_Data", index=False)

# === Step 7: Convert deduplicated data to JSON ===
json_path = "final_output.json"
combined_df.to_json(json_path, orient="records", indent=4)

print(f"✅ All sheets inserted, duplicates removed, and final JSON saved as {json_path}")"""
