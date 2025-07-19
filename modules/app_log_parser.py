import streamlit as st
import pandas as pd
import re

def main():
    st.set_page_config(page_title="Sigit", layout="wide")
    st.title("📄 Baca hasil log CR - format file wajib txt")

    uploaded_file = st.file_uploader("Upload file log (.txt)", type=["txt"])

    if uploaded_file:
        # Baca isi file baris per baris
        lines = uploaded_file.read().decode('utf-8', errors='ignore').splitlines()

        data = []
        entry = {
            "NE": "",
            "MMLCommand": "",
            "Retcode": "",
            "Retcode Detail": "",
            "Time": ""
        }

        for line in lines:
            line = line.strip()

            if line.startswith("MML Command-----"):
                entry["MMLCommand"] = line.replace("MML Command-----", "").strip()
            
            elif line.startswith("NE :"):
                entry["NE"] = line.replace("NE :", "").strip()

            elif line.startswith("Report : +++"):
                match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                if match:
                    entry["Time"] = match.group()

            elif line.startswith("RETCODE ="):
                match = re.search(r'RETCODE\s*=\s*(\d+)\s+(.*)', line)
                if match:
                    entry["Retcode"] = match.group(1)
                    entry["Retcode Detail"] = match.group(2)

            elif line.startswith("---    END"):
                if any(entry.values()):
                    data.append(entry.copy())
                entry = {
                    "NE": "",
                    "MMLCommand": "",
                    "Retcode": "",
                    "Retcode Detail": "",
                    "Time": ""
                }

        # Buat DataFrame dan tampilkan
        df = pd.DataFrame(data)
        
        if df.empty:
            st.warning("⚠️ Wes bener belum filenya?")
        else:
            st.success(f"✅ Parsing selesai. Total {len(df)} baris.")
            st.dataframe(df)

            # --- Kesimpulan Retcode Detail ---
            st.subheader("📊 Summary hasil parsing log CR")
            summary = df["Retcode Detail"].value_counts().reset_index()
            summary.columns = ["Retcode Detail", "Jumlah Baris"]
            st.dataframe(summary)

            # --- Download CSV hasil utama ---
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download jadi CSV",
                data=csv,
                file_name="parsed_log.csv",
                mime='text/csv'
            )
