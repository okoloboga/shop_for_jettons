const TronWeb = require('tronweb');
const validator = require('web3-validator');
const solWeb3 = require('@solana/web3.js');
const { Web3 } = require('web3');
const bs58 = require('bs58');


// Web3 Connection //
const web3 = new Web3(
    new Web3.providers.HttpProvider("https://rpc2.sepolia.org")
);

// Solana Connection //
const solConnect = new solWeb3.Connection(solWeb3.clusterApiUrl("testnet"), 'confirmed');

// Fantom Connection //
const ftmWeb3 = new Web3('https://rpc.testnet.fantom.network');

// TronWeb Connection //
const HttpProvider = TronWeb.providers.HttpProvider;
const fullNode = new HttpProvider("https://nile.trongrid.io");
const solidityNode = new HttpProvider("https://nile.trongrid.io");
const eventNode = new HttpProvider("https://nile.trongrid.io");

const tronWeb = new TronWeb({
	fullNode,
	solidityNode,
	eventNode
});


// ETHEREUM //
const getEthBalance = async (address) => {
    try {
        const rawBalance = await web3.eth.getBalance(address);
        const balance = await web3.utils.fromWei(rawBalance, 'ether');
		console.log(`Service: wallet ${address} ETH balance is ${balance}\n`)
        return balance;

    } catch (error) {
		console.error(`Service: getEthBalance error ${error}\n`)
        throw error;
    }
}


const checkEthAddress = async (address) => {
	try {
		const isValid = validator.isAddress(address);
		return isValid;	
	} catch (error) {
		console.error(`Service: checkEthAddress error ${error}\n`)
		throw error;
	}
}


const sendEth = async (sender, privateKey, target, amount) => {
    try {
		const value = await web3.utils.toWei(amount, 'ether');
		const gasPrice = await web3.eth.getGasPrice();
		const nonce = await web3.eth.getTransactionCount(sender, 'pending');

		console.log(`Service: eth transaction: by ${sender} to ${target} value ${value}`)

		const transaction = {
			to: target,
			value: value,
			gas: 21000,
			gasPrice: gasPrice,
			nonce: nonce
		};
		const signedTransaction = await web3.eth.accounts.signTransaction(
			transaction, privateKey
		);
		const response = await web3.eth.sendSignedTransaction(
			signedTransaction.rawTransaction
		);
		return { 
					response: response, 
				 	hash: signedTransaction.transactionHash
				};

    } catch (error) {
		console.error(`Service: sendEth error ${error}\n`)
        throw error;
    }
}


// SOLANA //
const getSolBalance = async (address) => {
	try {
		const walletKey = new solWeb3.PublicKey(address)
		const balance = await solConnect.getBalance(walletKey);
		console.log(`Service: wallet ${address} SOL balance is ${balance}\n`)
		return balance / solWeb3.LAMPORTS_PER_SOL;
	} catch (error) {
		console.error(`Service: getSolBalance error ${error}\n`)
		throw error;
	}
};


const checkSolAddress = async (address) => {
	try {
		const isValid = new solWeb3.PublicKey(address);
		return isValid;
	} catch (error) {
		console.error(`Service: checkSolAddress error ${error}\n`)
		throw error;
	}
}


const sendSol = async (target, amount, privateKey) => {
	try {
		const key = bs58.decode(privateKey);
		const from = solWeb3.Keypair.fromSecretKey(key);
		const transaction = new solWeb3.Transaction().add(
			solWeb3.SystemProgram.transfer({
				fromPubkey: from.publicKey,
				toPubkey: new solWeb3.PublicKey(target),
				lamports: Math.floor(amount * solWeb3.LAMPORTS_PER_SOL),
			}),
		);
		const signature = await solWeb3.sendAndConfirmTransaction(
			solConnect, transaction, [from]
		);
		return signature;
	} catch (error) {
		console.error(`Service: sendSol error ${error}\n`)
		throw error;
	}
};


// FANTOM //
const getFtmBalance = async (address) => {
	try {
		const rawBalance = await ftmWeb3.eth.getBalance(address);
		const balance = await ftmWeb3.utils.fromWei(rawBalance, 'ether');
		console.log(`Service: wallet ${address} FTM balance is ${balance}\n`)
		return balance;
	} catch (error) {
		console.error(`Service: getFtmBalance error ${error}\n`)
		throw error;
	}
};


const sendFtm = async (sender, target, amount, privateKey) => {
	try {
		const nonce = await ftmWeb3.eth.getTransactionCount(sender);
		const gasPrice = await ftmWeb3.eth.getGasPrice();
		const value = await ftmWeb3.utils.toWei(amount.toString(), 'ether');

		const transaction = {
			to: target,
			value: value,
			gas: 21000,
			gasPrice: gasPrice,
			nonce: nonce.toString()
		};
		const signedTransaction = await ftmWeb3.eth.accounts.signTransaction(
			transaction, privateKey
		);
		const response = await ftmWeb3.eth.sendSignedTransaction(
			signedTransaction.rawTransaction
		);
		return response;

	} catch (error) {
		console.error(`Service: sendFtm error ${error}\n`)
		throw error;
	}
};


// TRONWEB //
const createWallet = async () => {
	try {
		const newWallet = await tronWeb.createAccount();
		return newWallet;

	} catch (error) {
		console.error(`Service: createWallet error ${error}\n`)
		throw error;
	}
};


const getTrxBalance = async (address) => {
	try {
		const balance = await tronWeb.trx.getBalance(address)
		return balance / 1000000;

	} catch (error) {
		console.error(`Service: getTrxBalance error ${error}\n`)
		throw error;
	};
};


const getTokenBalance = async (owner, token, address) => {
	try {
		await tronWeb.setAddress(owner);
		const contract = await tronWeb.contract().at(token);
		const rawBalance = await contract.balanceOf(address).call();
		const balance = await rawBalance.toString();
		return balance;

	} catch (error) {
		console.error(`Service: getTokenBalance error ${error}\n`)
		throw error;
	}
};


const sendTrx = async (target, amount, privateKey) => {
	try {
        const account = await tronWeb.address.fromPrivateKey(privateKey);
		const transaction = await tronWeb.transactionBuilder.sendTrx(
            target, amount * 1e6, account
        );
		const response = await tronWeb.trx.sendRawTransaction(
			await tronWeb.trx.sign(transaction, privateKey)
		);
		return response;

	} catch (error) {
		console.error(`Service: sendTrx error ${error}\n`)
		throw error;
	}
};


const sendToken = async (owner, token, target, amount, privateKey) => {
	try {
    	console.log(`send token to ${target},gita owner: ${owner}, amount ${amount}, to address ${target}`)
		await tronWeb.setAddress(owner)
		const transaction = await tronWeb.transactionBuilder.triggerSmartContract(
			token,
			'transfer(address,uint256)',
			{},
			[
				{
					type: 'address',
					value: target
				},
				{
					type: 'uint256',
					value: amount
				}
			]
		);
    	const signedTransaction = await tronWeb.trx.sign(
        	transaction.transaction, privateKey
    	);
		const response = await tronWeb.trx.sendRawTransaction(signedTransaction);
		return response

	} catch (error) {
		console.error(`Service: sendToken error ${error}\n`)
		throw error;
	}
};


module.exports = {
  	getEthBalance,
	checkEthAddress,
    sendEth,
	getSolBalance,
	checkSolAddress,
  	sendSol,
  	getFtmBalance,
  	sendFtm,
	createWallet,
	getTrxBalance,
	getTokenBalance,
	sendTrx,
	sendToken
};
