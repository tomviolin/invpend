git clone git@github.com:tomviolin/invpend
cd invpend/
python3 -m venv venv
call .\venv\Scripts\activate.bat
pip install uv
uv pip install wheel
uv pip install cv2 mujoco gymnasium matplotlib numpy
uv pip install opencv-python mujoco gymnasium matplotlib numpy
uv pip install pandas torch
uv pip install seaborn imageio
