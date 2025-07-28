import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
import geopandas as gpd
from shapely.geometry import Polygon
import os
import tempfile
import zipfile

def main():
    st.set_page_config(page_title="📡 Visualisasi Cakupan Antena", layout="wide")
    st.title("📡 Create Gcell")
    st.write("Halaman ini untuk membuat Gcell.")
    st.markdown("---")

    # ---------------------- Fungsi Visualisasi dan Polygon ----------------------
    def create_antenna_sector(ax, center_x, center_y, radius, azimuth_deg, beamwidth_deg, color='blue', alpha=0.3):
        telecom_start_angle = azimuth_deg - (beamwidth_deg / 2)
        telecom_end_angle = azimuth_deg + (beamwidth_deg / 2)
        mpl_theta1 = (90 - telecom_end_angle) % 360
        mpl_theta2 = (90 - telecom_start_angle) % 360
        if mpl_theta2 < mpl_theta1:
            mpl_theta2 += 360
        wedge = Wedge((center_x, center_y), radius, theta1=mpl_theta1, theta2=mpl_theta2,
                      facecolor=color, alpha=alpha, edgecolor='black', linewidth=0.5)
        ax.add_patch(wedge)

    def wedge_to_polygon(center_x, center_y, radius, azimuth_deg, beamwidth_deg, resolution=30):
        start_angle = azimuth_deg - beamwidth_deg / 2
        end_angle = azimuth_deg + beamwidth_deg / 2
        angles = np.linspace(start_angle, end_angle, resolution)
        points = [(center_x, center_y)]
        for angle in angles:
            rad = np.deg2rad(angle)
            x = center_x + radius * np.cos(rad)
            y = center_y + radius * np.sin(rad)
            points.append((x, y))
        points.append((center_x, center_y))
        return Polygon(points)

    # ---------------------- Upload File ----------------------
    uploaded = st.file_uploader("📤 Upload CSV Engineering Parameter (filter dulu untuk area tertentu agar proses tidak lama)", type=['csv'])

    if uploaded:
        try:
            df_raw = pd.read_csv(uploaded, encoding='latin1')
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            st.stop()

        st.subheader("🧾 Preview Data Upload")
        st.dataframe(df_raw.head(5), use_container_width=True)

        columns = df_raw.columns.tolist()

        # Kolom Wajib
        col_x = st.selectbox("🧭 Pilih kolom Longitude (X)", columns)
        col_y = st.selectbox("📍 Pilih kolom Latitude (Y)", columns)
        col_azimuth = st.selectbox("🧭 Pilih kolom Azimuth", columns)
        col_bw = st.selectbox("📶 Pilih kolom Beamwidth", columns)
        col_radius = st.selectbox("📏 Pilih kolom Radius (satuan km)", columns)

        # Kolom Opsional
        col_id = st.selectbox("🆔 Pilih kolom Site ID (opsional)", ["(Tidak ada)"] + columns)
        col_ne = st.selectbox("🏢 Pilih kolom NE Name (opsional)", ["(Tidak ada)"] + columns)
        col_eci = st.selectbox("🔢 Pilih kolom ECI (opsional)", ["(Tidak ada)"] + columns)
        col_cell = st.selectbox("📱 Pilih kolom Cell Name (opsional)", ["(Tidak ada)"] + columns)

        required_cols = [col_x, col_y, col_azimuth, col_bw, col_radius]

        if all(col in df_raw.columns for col in required_cols):
            if st.button("🚀 Mulai Proses"):
                selected_cols = required_cols.copy()
                optional_cols = {}

                for label, col in [("SiteID", col_id), ("NE_Name", col_ne), ("ECI", col_eci), ("CellName", col_cell)]:
                    if col != "(Tidak ada)":
                        selected_cols.append(col)
                        optional_cols[label] = col

                df = df_raw[selected_cols].copy()

                for col in required_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                df.dropna(inplace=True)
                df["radius_deg"] = df[col_radius] / 111.0

                # ---------------------- Ekspor Polygon ----------------------
                st.markdown("---")
                st.subheader("💾 Ekspor Gcell GeoJSON atau MapInfo TAB")
                st.markdown("_Tunggu hingga muncul tombol download._")

                polygons = []
                for _, row in df.iterrows():
                    poly = wedge_to_polygon(
                        row[col_x], row[col_y],
                        radius=row["radius_deg"],
                        azimuth_deg=row[col_azimuth],
                        beamwidth_deg=row[col_bw]
                    )
                    polygons.append(poly)

                gdf = df.copy()
                gdf["geometry"] = polygons
                gdf = gpd.GeoDataFrame(gdf, geometry="geometry", crs="EPSG:4326")

                # Download GeoJSON
                geojson_bytes = gdf.to_json().encode('utf-8')
                st.download_button("🌐 Download GeoJSON", data=geojson_bytes,
                                   file_name="antena_sectors.geojson", mime="application/geo+json")

                # Download MapInfo (ZIP)
                with st.spinner("📦 Mengekspor ke MapInfo TAB..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmpdir:
                            tab_path = os.path.join(tmpdir, "antena_sectors.tab")
                            gdf.to_file(tab_path, driver="MapInfo File")

                            zip_path = os.path.join(tmpdir, "antena_sectors_mapinfo.zip")
                            with zipfile.ZipFile(zip_path, 'w') as zipf:
                                for ext in [".tab", ".dat", ".map", ".id"]:
                                    file_path = tab_path.replace(".tab", ext)
                                    if os.path.exists(file_path):
                                        zipf.write(file_path, arcname=os.path.basename(file_path))

                            with open(zip_path, 'rb') as f:
                                zip_bytes = f.read()

                        st.download_button("🗺️ Download .TAB (ZIP)", data=zip_bytes,
                                           file_name="antena_sectors_mapinfo.zip", mime="application/zip")
                    except Exception as e:
                        st.error(f"Gagal ekspor ke TAB: {e}")
        else:
            st.warning("⚠️ Silakan pilih semua kolom wajib sebelum memulai proses.")
