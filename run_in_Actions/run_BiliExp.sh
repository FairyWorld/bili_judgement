#安装Actions需要的依赖库
sudo apt install python3-testresources
sudo -H pip3 install --upgrade setuptools >/dev/null
sudo -H pip3 install -r ./run_in_Actions/requirements.txt >/dev/null
pip install aiohttp

#将secrets映射到配置文件
\cp -f ./run_in_Actions/config.json ./config/
python3 ./run_in_Actions/secrets2config.py

if [ -n "$DELAY" ]; then    #延时
  sleep "$DELAY"
fi

#启动BiliExp
python3 BiliExp.py
