# SimRank-IDE

A procedure based on iterative diagonal estimation method to compute [SimRank](http://en.wikipedia.org/wiki/SimRank) approximately.

## Installing dependencies

1. Python 2.7.9.

2. NumPy (http://www.numpy.org/), SciPy (http://www.scipy.org/), scikit-learn (http://scikit-learn.org/stable/). 

## Running 

### Ubuntu

To run a test on a Simple English Wikipedia graph run the following:
```
cd simplewiki
sh main.sh
cd ..
python main.py
python explain_lyap.py simplewiki/ d_simplewiki_2e-2.mat GNU
```

## License

If you use this code in your research, please cite 
"Linear complexity SimRank computation based on the iterative diagonal estimation" by 
I.V. Oseledets, G.V. Ovchinnikov, A. M. Katrutsa, pre-print http://arxiv.org/abs/1502.07167

If you have any questions, do not hesitate to contact authors: ovgeorge@yandex.ru, aleksandr.katrutsa@phystech.edu
