# web3-station

## Run

Create a `.env` with the following content at the root of the repository
```env
WEB3_PRIVATE_KEY=0x8777c5433381215bb87adb8f92076da014bd789184ef85b2444bb34bbaafa707
WEB3_PUBLIC_KEY=0xbA8DCA496adc3Dc6af79bDA27e547024b11465ce
```
WARNING: This private key is publicly known, change it

Run a docker container with ganache-cli
```
docker run -d -p 8545:8545 trufflesuite/ganache-cli --chainId 1337 --account="$WEB3_PRIVATE_KEY,115792089237316195423570985008687907853269984665640564039457584007913129639935000000000000000000"
```

Run the software
```
python3 pip3 install -r requirements.txt
python3 main.py
```
