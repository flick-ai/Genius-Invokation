rm genius*.whl
cd ..
python setup.py bdist_wheel
cd website
cp ../dist/*.whl ./static
python app.py