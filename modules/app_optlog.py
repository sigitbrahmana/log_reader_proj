# modules/app_optlog.py

import streamlit as st
import pandas as pd
import re
import io  # untuk membuat CSV download button

def main():    
    st.set_page_config(page_title="Sigit Optlog Parser", layout="wide")
    st.title("📄 Optlog Parser - File format yang dipakai csv")
    
    def parse_log_file(content):
        lines = content.decode('utf-8').splitlines()
        data = []
        site = ""
        cmd = ""
        operator = ""
        severity = ""
        time = ""
    
        for line in lines:
            line = line.strip()
    
            if line.startswith('"') and line.count(',') == 3:
                parts = [p.strip('"') for p in line.split(',')]
                if len(parts) == 4 and parts[0] == parts[1]:
                    site = parts[0]
    
            elif line.startswith('"Operation Command Information:'):
                cmd = re.sub(r'^"Operation Command Information:",', '', line).strip('"')
    
            elif re.match(r'^"EMS",".+?",".+?",".+?",".+?",".+?",".+?",".+?",".+?",".+?"$', line):
                parts = [p.strip('"') for p in line.split(',')]
                operator = parts[1]
                severity = parts[8]
                time = parts[5]
                status = parts[6]
    
                data.append({
                    'Site': site,
                    'Command': cmd,
                    'Operator': operator,
                    'Severity': severity,
                    'Operate Time': time,
                    'Status': status
                })
    
        df = pd.DataFrame(data)
        return df
    
    # Upload file log
    uploaded_file = st.file_uploader("Upload file log (.csv)", type=['csv'])
    
    if uploaded_file is not None:
        st.success("File berhasil diupload. Parsing dimulai...")
        try:
            df = parse_log_file(uploaded_file.read())
            st.write("📊 Hasil Parsing:")
            st.dataframe(df, use_container_width=True)
    
            # Unduh file hasil
            output = io.BytesIO()
            df.to_csv(output, index=False)
            st.download_button(
                label="📥 Download CSV",
                data=output.getvalue(),
                file_name="parsed_log.csv",
                mime="text/csv"
            )
    
        except Exception as e:
            st.error(f"Gagal memproses file: {e}")
    else:
        st.info("Silakan upload file log untuk memulai.")
