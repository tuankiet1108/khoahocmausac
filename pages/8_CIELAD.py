import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from skimage.color import deltaE_cie76, lab2rgb

# Giao diện Streamlit
st.set_page_config(layout="centered")
st.title("🎨 Không gian màu CIELAB ")
st.markdown("""
Biểu đồ mô tả sự chuyển dịch màu giữa hai điểm trong không gian CIELAB bằng biểu đồ vòng tròn.\n
Nhập giá trị L*, a*, b* để xem sự khác biệt màu sắc (ΔE) và hướng dịch chuyển màu.
""")

# Nhập dữ liệu từ sidebar
st.sidebar.header("🔧 Nhập màu (CIELAB)")
L1 = st.sidebar.slider("L1 (Lightness)", 0.0, 100.0, 60.0)
a1 = st.sidebar.slider("a1 (Green ←→ Red)", -128.0, 127.0, 40.0)
b1 = st.sidebar.slider("b1 (Blue ←→ Yellow)", -128.0, 127.0, 30.0)

L2 = st.sidebar.slider("L2 (Lightness)", 0.0, 100.0, 70.0)
a2 = st.sidebar.slider("a2 (Green ←→ Red)", -128.0, 127.0, 50.0)
b2 = st.sidebar.slider("b2 (Blue ←→ Yellow)", -128.0, 127.0, 40.0)

lab1 = np.array([[L1, a1, b1]])
lab2 = np.array([[L2, a2, b2]])
delta_E = deltaE_cie76(lab1, lab2)[0]

# Phân loại mức độ khác biệt
if delta_E < 1:
    note = "🔹 Sự khác biệt rất nhỏ, hầu như không thể cảm nhận."
elif delta_E < 2:
    note = "🔸 Khác biệt rất nhỏ, chỉ cảm nhận bởi người có kinh nghiệm."
elif delta_E < 3.5:
    note = "🔸 Khác biệt tương đối, có thể cảm nhận bởi người không có kinh nghiệm."
elif delta_E < 5:
    note = "🔴 Khác biệt lớn."
else:
    note = "🔴🔴 Khác biệt rất lớn."

# Tạo biểu đồ hình tròn CIELAB
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

# Vẽ nền color wheel bằng a*, b* từ -128 đến 127
res = 300
x = np.linspace(-128, 127, res)
y = np.linspace(-128, 127, res)
a_grid, b_grid = np.meshgrid(x, y)
mask = a_grid**2 + b_grid**2 <= 127**2
L_fixed = 70 * np.ones_like(a_grid)
lab_grid = np.stack([L_fixed, a_grid, b_grid], axis=-1)
rgb_grid = lab2rgb(lab_grid)
rgb_grid[~mask] = 1  # Mask vùng ngoài hình tròn bằng màu trắng

ax.imshow(rgb_grid, extent=(-128, 127, -128, 127), origin='lower')

# Vẽ trục và vòng tròn
circle = plt.Circle((0, 0), 127, color='black', fill=False, linestyle='--', lw=1)
ax.add_patch(circle)
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

# Vẽ điểm Lab1 và Lab2
ax.plot(a1, b1, 'o', color='black', label='Lab1 (tham chiếu)', markersize=10)
ax.plot(a2, b2, 'o', color='white', label='Lab2 (màu đo được)', markersize=10)
arrow = FancyArrowPatch((a1, b1), (a2, b2), arrowstyle='->', mutation_scale=15, color='black')
ax.add_patch(arrow)

ax.set_xlim([-130, 130])
ax.set_ylim([-130, 130])
ax.set_xlabel("a* (−: xanh lá, +: đỏ)")
ax.set_ylabel("b* (−: xanh dương, +: vàng)")
ax.set_title("Không gian màu CIELAB 2D hình tròn (L* = 70)")
ax.legend(loc='upper left')

st.pyplot(fig)

# Nhận xét
st.markdown(f"""
### 🔍 Nhận xét
- **ΔE = {delta_E:.2f}**
- {note}
- Mũi tên biểu diễn **hướng và độ lớn sự chuyển dịch** màu từ Lab1 sang Lab2 trong không gian CIELAB.
""")
