FROM jupyter/scipy-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

#install python 2 Tensorflow
RUN conda install --quiet --yes -n python2 'tensorflow=1.0.1'
