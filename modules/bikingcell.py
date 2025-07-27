import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
import geopandas as gpd
from shapely.geometry import Polygon
import os

def main():
    st.title("🧱 Create Gcell")
    st.write("Halaman ini untuk membuat Gcell.")
    
# ---------------------- Konfigurasi Halaman ----------------------
st.set_page_config(page_title="📡 Visualisasi Cakupan Antena", layout="wide")
st.title("📡 Visualisasi Cakupan Antena LTE dari CSV")

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
uploaded = st.file_uploader("📤 Upload CSV Engineering Parameter", type=['csv'])

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

            for col in [col_x, col_y, col_azimuth, col_bw, col_radius]:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df.dropna(inplace=True)
            df["radius_deg"] = df[col_radius] / 111.0

            # ---------------------- Visualisasi Cakupan ----------------------
            if st.button("📊 Tampilkan Visualisasi"):
                if df.empty:
                    st.warning("Tidak ada data valid setelah pembersihan.")
                else:
                    fig, ax = plt.subplots(figsize=(10, 10))
                    ax.set_aspect('equal')
                    all_x = df[col_x].values
                    all_y = df[col_y].values
                    max_r = df["radius_deg"].max()

                    if len(all_x) > 1:
                        ax.set_xlim(all_x.min() - max_r, all_x.max() + max_r)
                        ax.set_ylim(all_y.min() - max_r, all_y.max() + max_r)
                    else:
                        ax.set_xlim(all_x[0] - max_r * 2, all_x[0] + max_r * 2)
                        ax.set_ylim(all_y[0] - max_r * 2, all_y[0] + max_r * 2)

                    for i, row in df.iterrows():
                        label = row[col_id] if col_id != "(Tidak ada)" else f"Antenna_{i+1}"
                        ax.plot(row[col_x], row[col_y], 'ro', markersize=6)
                        create_antenna_sector(ax, row[col_x], row[col_y], row["radius_deg"],
                                              row[col_azimuth], row[col_bw])

                    ax.set_xlabel("Longitude")
                    ax.set_ylabel("Latitude")
                    ax.set_title("Visualisasi Cakupan Antena LTE")
                    ax.grid(True)
                    st.pyplot(fig)

            # ---------------------- Ekspor Polygon ----------------------
            st.markdown("---")
            st.subheader("💾 Ekspor Polygon Cakupan (GeoJSON & MapInfo TAB)")

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

            geojson_bytes = gdf.to_json().encode('utf-8')
            st.download_button("🌐 Download GeoJSON", data=geojson_bytes,
                               file_name="antena_sectors.geojson", mime="application/geo+json")

            with st.spinner("📦 Mengekspor ke MapInfo TAB..."):
                try:
                    tab_path = "antena_output.tab"
                    gdf.to_file(tab_path, driver="MapInfo File")
                    with open(tab_path, 'rb') as f:
                        tab_bytes = f.read()
                    st.download_button("🗺️ Download MapInfo TAB", data=tab_bytes,
                                       file_name="antena_sectors.tab", mime="application/octet-stream")
                    os.remove(tab_path)
                except Exception as e:
                    st.error(f"Gagal ekspor ke TAB: {e}")
    else:
        st.warning("⚠️ Silakan pilih semua kolom wajib sebelum memulai proses.")
