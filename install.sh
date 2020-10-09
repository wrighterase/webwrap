if [ "$(id -u)" != "0" ]; then
    echo "Please, run as root."
    exit 1
fi

apt update && apt install rlwrap;

git clone https://github.com/mxrch/webwrap /opt/webwrap;
cd /opt/webwrap/ && chmod 755 webwrap install.sh
python3 -m pip install -r /opt/webwrap/requirements.txt;
ln -s /opt/webwrap/webwrap /usr/bin/webwrap;
echo "\nWebwrap is installed !\nTry :\n$ webwrap";
