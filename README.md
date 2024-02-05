

![Screenshot 2024-02-05 at 18 41 23](https://github.com/owalid/web3-station/assets/28403617/d1329987-eeb9-40fb-97ab-6c7950b195f1)

## Description

This repository hosts a TCP server, which is primarily used for the deployment of CTF challenges related to Ethereum smart contracts.

You will find in this repository several folders:

- `/challenges` containing web3 challenges. Each challenge contains a .sol file with abi and bin version. A .yaml file containing the details of the challenge. And a py file containing the check to do to validate the challenges. All of these challenges are listed in the [challenges.yaml](https://github.com/owalid/web3-station/blob/main/challenges.yaml) file at the root of the repo.
- `/py_server` contains all the logic of the TCP server.

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
docker run -d -p 8545:8545 ghcr.io/foundry-rs/foundry:latest anvil
```

Run the software
```
python3 pip3 install -r requirements.txt
python3 main.py
```

## Screenshot

Once the server is started, you can query it via the nc command. A menu is then available and allows you to list the challenges, retrieve the source code, deploy etc..

![Screenshot 2024-02-05 at 18 37 55](https://github.com/owalid/web3-station/assets/28403617/4cc5735e-9511-4153-9563-9b86b2495b5c)
