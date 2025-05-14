import streamlit as st
import colour
import matplotlib.pyplot as plt
from colour import SpectralShape

# Cấu hình Streamlit
st.set_page_config(layout="centered")
st.title("CIE 1931 Color Matching Functions")

# Lấy dữ liệu CMFs
cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
shape = SpectralShape(400, 700, 5)
cmfs = cmfs.copy().align(shape)

wavelengths = cmfs.wavelengths
x_bar = cmfs.values[:, 0]
y_bar = cmfs.values[:, 1]
z_bar = cmfs.values[:, 2]

# Vẽ biểu đồ (Kích thước cố định, DPI cao hơn để không vỡ hình)
fig, ax = plt.subplots(figsize=(6, 4.5), dpi=120)

# Fill mờ và vẽ đường cong
ax.fill_between(wavelengths, 0, x_bar, color='red', alpha=0.3)
ax.plot(wavelengths, x_bar, color='red', label=r"$\bar{x}(\lambda)$", linewidth=1.5)

ax.fill_between(wavelengths, 0, y_bar, color='green', alpha=0.3)
ax.plot(wavelengths, y_bar, color='green', label=r"$\bar{y}(\lambda)$", linewidth=1.5)

ax.fill_between(wavelengths, 0, z_bar, color='blue', alpha=0.3)
ax.plot(wavelengths, z_bar, color='blue', label=r"$\bar{z}(\lambda)$", linewidth=1.5)

# Tùy chỉnh trục và nhãn
ax.set_xlim(400, 700)
ax.set_ylim(0, 1.8)
ax.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
ax.set_ylabel(r"$\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)$", fontsize=12)
ax.set_title("CIE 1931 Color Matching Functions", fontsize=14, weight='bold')
ax.tick_params(axis='both', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.3)

# Giao diện 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=10, loc='upper right')

# Hiển thị biểu đồ
st.pyplot(fig)
