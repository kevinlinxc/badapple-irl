import streamlit as st
import os
from pathlib import Path
from PIL import Image  # https://github.com/streamlit/streamlit/issues/1294#issuecomment-1488435694

# dupes found by find_duplicate_frames.py
dupes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 242, 283, 288, 292, 296, 299, 306, 363, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 558, 559, 560, 561, 562, 565, 567, 574, 579, 581, 582, 584, 586, 590, 609, 611, 612, 665, 666, 667, 669, 670, 681, 687, 690, 691, 692, 696, 698, 704, 709, 716, 717, 718, 719, 720, 737, 739, 740, 741, 1420, 1424, 1529, 2345, 2348, 2349, 2350, 2351, 2352, 2388, 2390, 2391, 2392, 2399, 2401, 2402, 2403, 2405, 2407, 2415, 2449, 2455, 2457, 2544, 2551, 2555, 2595, 2596, 2598, 2599, 2603, 2606, 2609, 2610, 2613, 2615, 2617, 2627, 2740, 2741, 2742, 2743, 2744, 2745, 2746, 2747, 2748, 2749, 2750, 2751, 2752, 2753, 2754, 2755, 2756, 2757, 2758, 2759, 2760, 2761, 2762, 2763, 2764, 2765, 2766, 2767, 2768, 2769, 2770, 2771, 2772, 2773, 2774, 2775, 2776, 2777, 2778, 2864, 2880, 2896, 3019, 3038, 3042, 3047, 3050, 3051, 3053, 3055, 3057, 3058, 3060, 3062, 3064, 3065, 3072, 3073, 3074, 3076, 3080, 3090, 3095, 3182, 3183, 3184, 3185, 3186, 3187, 3188, 3189, 3190, 3191, 3192, 3193, 3195, 3196, 3197, 3199, 3200, 3245, 3246, 3250, 3251, 3317, 3318, 3319, 3320, 3321, 3322, 3323, 3324, 3325, 3326, 3327, 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343, 3344, 3345, 3346, 3347, 3348, 3349, 3355, 3357, 3602, 4028, 4029, 4060, 4083, 4087, 4092, 4093, 4100, 4115, 4121, 4122, 4123, 4124, 4125, 4126, 4128, 4129, 4130, 4131, 4132, 4133, 4134, 4165, 4168, 4169, 4170, 4171, 4173, 4187, 4189, 4190, 4192, 4193, 4194, 4195, 4196, 4197, 4198, 4199, 4200, 4201, 4202, 4203, 4204, 4205, 4224, 4319, 4320, 4326, 4432, 4566, 4567, 4568, 4569, 4570, 4571, 4579, 4585, 4592, 4593, 4594, 4595, 4596, 4597, 4605, 4709, 4710, 4712, 4713, 4714, 4724, 4727, 4883, 4904, 4910, 4913, 4921, 4922, 4948, 4950, 4985, 4986, 5046, 5048, 5049, 5061, 5062, 5063, 5064, 5065, 5066, 5067, 5069, 5072, 5074, 5075, 5077, 5082, 5083, 5084, 5085, 5087, 5088, 5089, 5090, 5119, 5356, 5357, 5358, 5393, 5780, 5890, 5903, 5917, 5918, 5920, 5989, 5992, 5997, 6003, 6006, 6010, 6011, 6012, 6013, 6014, 6017, 6020, 6022, 6023, 6024, 6027, 6029, 6030, 6033, 6036, 6039, 6041, 6044, 6202, 6203, 6208, 6218, 6224, 6233, 6513, 6514, 6515, 6516, 6517, 6518, 6519, 6520, 6521, 6522, 6523, 6524, 6525, 6526, 6527, 6528, 6529, 6530, 6531, 6532, 6533, 6534, 6535, 6536, 6537, 6538, 6539, 6540, 6541, 6542, 6543, 6544, 6545, 6546, 6547, 6548, 6549, 6550, 6551, 6552, 6553, 6554, 6555, 6556, 6557, 6558, 6559, 6560, 6561, 6562, 6563, 6564, 6565, 6566, 6567, 6568, 6569, 6570, 6571]
dupeset = set(dupes)

st.set_page_config(layout="centered")

hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# original_expander = st.expander("Original frame")
frame_number = st.number_input('Enter frame number', min_value=0, max_value=6572, value=0, step=1)

warning = st.empty()
if frame_number in dupeset:
    warning.warning("Duplicate, consider ignoring")
else:
    warning.empty()
row1_text = st.empty()
row1 = st.empty()
row2_text = st.empty()
row2 = st.empty()
# let user manually enter image number, or click next and back


# display images from real_frames, circle_frames and diff_frames based on image number
base = Path("badapple-irl").resolve()
# real_path = base / "real_frames" / f"{frame_number}.jpg"
# if os.path.exists(real_path):
#     img = Image.open(real_path)
#     original_expander.image(img)

circle_path = base / "circle_frames" / f"{frame_number}.jpg"
if os.path.exists(circle_path):
    row2_text.write(f"Frame {frame_number}")
    img = Image.open(circle_path)
    row2.image(img)


diff_path = base / "diff_frames" / f"{frame_number}.jpg"
if os.path.exists(diff_path):
    # row1_text.write(f"Frames {frame_number-1} to {frame_number} diff")
    img = Image.open(diff_path)
    row1.image(img)



