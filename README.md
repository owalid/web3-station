# web3-station

## Run

ps: you can run the `docker-compose` file to not bother with the following setup.

Create a `.env` with the following content at the root of the repository
```env
WEB3_RPC_URL=http://localhost:8545
WEB3_PRIVATE_KEY=0x8777c5433381215bb87adb8f92076da014bd789184ef85b2444bb34bbaafa707
WEB3_PUBLIC_KEY=0xbA8DCA496adc3Dc6af79bDA27e547024b11465ce
SECRET_KEY=bonjour
```
WARNING: This private key is publicly known, change it

Run a docker container to host a private node using anvil
```
docker run -d -p 8545:8545 ghcr.io/foundry-rs/foundry:latest
```

Run the software
```
python3 pip3 install -r requirements.txt
python3 main.py
```

