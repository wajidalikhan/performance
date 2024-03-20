ARG BASEIMAGE=gitlab-registry.cern.ch/linuxsupport/alma9-base:latest
FROM --platform=linux/amd64 ${BASEIMAGE}

SHELL [ "/bin/bash", "-c" ]

RUN dnf install -y bash && \
    dnf install -y automake bzip2 bzip2-libs bzip2-devel coreutils-single cmake3 e2fsprogs \
    e2fsprogs-libs perl file file-libs fontconfig freetype gcc-c++ git glibc krb5-libs \
    libaio libcom_err libcom_err-devel libgomp libICE \
    libSM libX11 libX11-devel libxcrypt libXcursor libXext \
    libXext-devel libXft libXft-devel libXi libXinerama \
    libXmu libXpm libXpm-devel libXrandr libXrender \
    libglvnd-opengl libtirpc mesa-libGL mesa-libGLU mesa-libGLU-devel \
    java-1.8.0-openjdk-devel libtool m4 make \
    ncurses ncurses-libs ncurses-devel nspr nss nss-devel nss-util \
    openssl openssl-devel openssl-libs \
    patch popt popt-devel python3 python3-pip ninja-build readline readline-devel rpm-build \
    rsync tcl tcsh time tk wget which zlib zsh tcl-devel tk-devel krb5-devel \
    bc strace tar zip unzip hostname nano libnsl procps-ng environment-modules && \
    dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm &&\
    dnf install -y voms-clients-cpp krb5-workstation python3-psutil myproxy apptainer \
        python3-requests &&\
    dnf update -y ca-certificates &&\
    dnf install -y dnf-plugins-core &&\
    ([ "@EXTRA_PACKAGES@" != "" ] && dnf -y install @EXTRA_PACKAGES@ || true) &&\
    yum clean all

RUN groupadd -g 1000 cmsusr && adduser -u 1000 -g 1000 -G root cmsusr && \
    echo "cmsusr ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers

# Make Images grid/singularity compatible
RUN mkdir -p /cvmfs /afs /eos /pool /code && \
    chmod 1777 /afs /eos /pool /code && \
    chown -R cmsusr:cmsusr /code

USER cmsusr
WORKDIR /code
COPY . /code/

RUN source install.sh && \
    sed -i 's/"Rho_fixedGridRhoFastjetAll"/"Rho"/g' bamboo/bamboo/analysisutils.py && \
    sed -i 's/"Rho_fixedGridRhoFastjetAll"/"Rho"/g' bamboovenv/lib/python3.9/site-packages/CMSJMECalculators/utils.py && \
    sed -i 's/JRDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py && \
    sed -i 's/JECDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py && \
    sed -i '/cms-jet\/jme-validation/s/$/ branch="main",/' bamboo/bamboo/analysisutils.py && \
    sed -i 's/heads\/master"/heads\/"+self.branch/g' bamboovenv/lib/python3.9/site-packages/CMSJMECalculators/jetdatabasecache.py && \
    sed -i 's/idxs=defCache(self.rng)/idxs=defCache(self.rng).replace("IndexRange<std::size_t>{","IndexRange<std::size_t>{static_cast<unsigned long>(").replace("}",")}")/g' bamboo/bamboo/treeoperations.py
