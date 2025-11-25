cd src

cd meta
cd ts
tsc

cd ..
cd ..

rm -r build
rm -r dist
rm -r meta.egg-info
python3 setup.py install