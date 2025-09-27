import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import base64

st.set_page_config(
    page_title='Ship Trips',
    page_icon='✌',
    layout="wide"
)


st.title("Secure Authentication App")




def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    image_base64 = get_base64_image("ahmed_sarhan.jpg")
except FileNotFoundError:
    st.error("صورة الملف الشخصي (ahmed_sarhan.jpg) غير موجودة. يرجى التأكد من أنها في نفس مجلد التطبيق.")
    st.stop()


with st.container():
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f'<div class="profile-image" style="background-image: url(data:image/jpeg;base64,{image_base64});"></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="profile-text">
                <h2>Ahmed Sarhan</h2>
                <p><strong>Data Analyst</strong></p>
                <p>Faculty of Computer and Data Science</p>
                <div class="social-links">
                    <a href="https://www.linkedin.com/in/ahmed-sarhan-026b73359?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank">
                        <i class="fab fa-linkedin fa-2x"></i>
                    </a>
                    <a href="https://github.com/ahmedsarhan-sudo" target="_blank">
                        <i class="fab fa-github fa-2x"></i>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<style>
.profile-container {{
    background: linear-gradient(135deg, #2c3a50, #1f2735);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    border: 1px solid #3d4a60;
}}
.profile-image {{
    width: 150px;
    height: 150px;
    background-size: cover;
    background-position: center;
    border-radius: 50%;
    border: 4px solid #00c6ff;
    box-shadow: 0 0 15px rgba(0, 198, 255, 0.5);
}}
.profile-text {{
    margin-left: 20px;
    color: #f0f2f6;
}}
.profile-text h2 {{
    font-size: 2rem;
    font-weight: 700;
    color: #f0f2f6;
    margin: 0;
}}
.profile-text p {{
    font-size: 1rem;
    margin: 0;
    color: #a0a0a0;
}}
.social-links {{
    margin-top: 15px;
}}
.social-links a {{
    color: #00c6ff;
    margin-right: 15px;
    transition: color 0.3s;
}}
.social-links a:hover {{
    color: #0072ff;
}}
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)



particles_html = """
<div id="particles-js"></div>
<style>
#particles-js {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: -1;
}
</style>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
    "color": {"value": "#00c6ff"},
    "shape": {"type": "circle", "stroke": {"width": 0, "color": "#000"}},
    "opacity": {"value": 0.5},
    "size": {"value": 3},
    "line_linked": {"enable": true, "distance": 150, "color": "#00c6ff", "opacity": 0.4, "width": 1},
    "move": {"enable": true, "speed": 3, "direction": "none", "out_mode": "bounce"}
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {"enable": true, "mode": "grab"},
      "onclick": {"enable": true, "mode": "push"},
      "resize": true
    }
  },
  "retina_detect": true
});
</script>
"""
components.html(particles_html, height=1000, scrolling=False)



st.title('Ship Trips Dashboard')

df = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)

st.header("Overview")
st.map(df)

st.write("This is a placeholder for detailed analysis and data visualizations.")
