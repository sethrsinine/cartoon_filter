import cv2
import streamlit as st
import numpy as np
from PIL import Image

def cartoonization(img, option):  # 修改参数名称为option
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = img.copy()  # 创建新变量存储处理结果

    if option == "Pencil Sketch":
        value = st.sidebar.slider('Tune the brightness of your sketch (the higher the value, the brighter your sketch)',
                                0.0, 300.0, 250.0)
        kernel = st.sidebar.slider(
            'Tune the boldness of the edges of your sketch (the higher the value, the bolder the edges)', 1, 99, 25,
            step=2)
        gray_blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
        output = cv2.divide(gray, gray_blur, scale=value)

    elif option == "Detail Enhancement":  # 改为elif确保单选
        smooth = st.sidebar.slider(
            'Tune the smoothness level of the image (the higher the value, the smoother the image)', 3, 99, 5, step=2)
        kernel = st.sidebar.slider('Tune the sharpness of the image (the lower the value, the sharper it is)', 1, 21, 3,
                                 step=2)
        edge_preserve = st.sidebar.slider(
            'Tune the color averaging effects (low: only similar colors will be smoothed, high: dissimilar color will be smoothed)',
            0.0, 1.0, 0.5)
        gray = cv2.medianBlur(gray, kernel)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
        color = cv2.detailEnhance(img, sigma_s=smooth, sigma_r=edge_preserve)
        output = cv2.bitwise_and(color, color, mask=edges)

    elif option == "Pencil Edges":
        kernel = st.sidebar.slider('Tune the sharpness of the sketch (the lower the value, the sharper it is)', 1, 99,
                                 25, step=2)
        laplacian_filter = st.sidebar.slider(
            'Tune the edge detection power (the higher the value, the more powerful it is)', 3, 9, 3, step=2)
        noise_reduction = st.sidebar.slider(
            'Tune the noise effects of your sketch (the higher the value, the noisier it is)', 10, 255, 150)
        gray = cv2.medianBlur(gray, kernel)
        edges = cv2.Laplacian(gray, -1, ksize=laplacian_filter)
        edges_inv = 255 - edges
        dummy, output = cv2.threshold(edges_inv, noise_reduction, 255, cv2.THRESH_BINARY)

    elif option == "Bilateral Filter":
        smooth = st.sidebar.slider(
            'Tune the smoothness level of the image (the higher the value, the smoother the image)', 3, 99, 5, step=2)
        kernel = st.sidebar.slider('Tune the sharpness of the image (the lower the value, the sharper it is)', 1, 21, 3,
                                 step=2)
        edge_preserve = st.sidebar.slider(
            'Tune the color averaging effects (low: only similar colors will be smoothed, high: dissimilar color will be smoothed)',
            1, 100, 50)
        gray = cv2.medianBlur(gray, kernel)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, smooth, edge_preserve, smooth)
        output = cv2.bitwise_and(color, color, mask=edges)

    return output

# ... 以下Streamlit代码保持不变 ...

###############################################################################
# ... 保持前面的导入和函数定义不变 ...

###############################################################################

st.write("""
          # Cartoonize Your Image!
          """
         )

st.write("This is an app to turn your photos into cartoon")

file = st.sidebar.file_uploader("Please upload an image file", type=["jpg", "png"])

if file is None:
    st.text("You haven't uploaded an image file")
else:
    image = Image.open(file)
    img = np.array(image)

    option = st.sidebar.selectbox(
        'Which cartoon filters would you like to apply?',
        ('Pencil Sketch', 'Detail Enhancement', 'Pencil Edges', 'Bilateral Filter'))

    # 创建左右两列布局
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Cartoonized Image")
        cartoon = cartoonization(img, option)
        st.image(cartoon, use_container_width=True)
