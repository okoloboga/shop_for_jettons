const service = require('../services/service');


// ETHEREUM //
const getEthBalance = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\naddress"
            }
        })
        return;
    };
    try {
        console.log(`Controller: getEthBalance ${address}\n`)
        const ethBalance = await service.getEthBalance(address);
        console.log(`Controller: wallet ${address} ETH balance is ${ethBalance}\n`)
        res.send({ status: "OK", data: ethBalance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};



const checkEthAddress = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\naddress"
            }
        })
        return;
    };
    try {
        console.log(`Controller: checkEthAddress ${address}\n`)
        const isValid = await service.checkEthAddress(address);
        res.send({ status: "OK", data: isValid });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const sendEth = async (req, res) => {
    const body = req.query
    if ( 
        !body.sender ||
        !body.privateKey ||
        !body.target ||
        !body.amount
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                sender; privateKey; target; amount"
            }
        })
        return;
    };
    try {
        console.log(`Controller: sendEth ${JSON.stringify(body, null, 2)}\n`)
        const ethTransaction = await service.sendEth(
            body.sender, body.privateKey, body.target, body.amount
        );
        console.log(`Controller: ethTransaction Hash ${ethTransaction.hash}\n`);
        res.send({ status: "OK", hash: ethTransaction });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


/// SOLANA ///
const getSolBalance = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\naddress"
            }
        })
        return;
    };
    try {
        console.log(`Controller: getSolBalance ${address}\n`)
        const solBalance = await service.getSolBalance(address);
        console.log(`Controller: wallet ${address} SOL balance is ${solBalance}\n`)
        res.send({ status: "OK", data: solBalance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const checkSolAddress = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
        res.status(400).send({
            status: 'FAILED',
            data: { error: "One of following keys is missing or is empty in request body:\naddress" }
        })
        return;
    };
    try {
        console.log(`Controller: checkSolAddress ${address}\n`)
        const isValid = await service.checkSolAddress(address);
        res.send({ status: "OK", data: isValid });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const sendSol = async (req, res) => {
    const body = req.query
    if (
        !body.target ||
        !body.amount ||
        !body.privateKey
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                target; amount; privateKey"
            }
        })
        return;
    };
    try {
        console.log(`Controller: sendSol ${JSON.stringify(body, null, 2)}\n`)
        const solTransaction = await service.sendSol(
            body.target, body.amount, body.privateKey
        );
        console.log(`Controller: solTransaction ${JSON.stringify(solTransaction)}\n`);
        res.send({ status: "OK", data: solTransaction });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


/// FANTOM ///
const getFtmBalance = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\naddress"
            }
        })
        return;
    };
    try {
        console.log(`Controller: getFtmBalance ${address}\n`)
        const fntBalance = await service.getFtmBalance(address);
        console.log(`Controller: wallet ${address} FTM balance is ${fntBalance}\n`)
        res.send({ status: "OK", data: fntBalance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const sendFtm = async (req, res) => {
    const body = req.query;
    if (
        !body.sender ||
        !body.target ||
        !body.amount ||
        !body.privateKey
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                sender; target; amount; privateKey"
            }
        })
        return;
    }
    try {
        console.log(`Controller: sendFtm ${JSON.stringify(body, null, 2)}\n`)
        const ftmTransaction = await service.sendFtm(
            body.sender, body.target, body.amount, body.privateKey
        );
        console.log(`Controller: ftmTransaction hash ${ftmTransaction.transactionHash}\n`);
        res.send({ status: "OK", data: ftmTransaction.transactionHash });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


// TRONWEB //
const createTrxWallet = async (req, res) => {
    try {
        const newWallet = await service.createTrxWallet();
	    console.log(`Controller: New Wallet ${JSON.stringify(newWallet)}\n`)
	    res.send({ status: "OK", data: newWallet });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const getTrxBalance = async (req, res) => {
    const address = req.query.address;
    if ( !address ) {
		res.status(400).send({
            status: "FAILED",
            data: {
                error: "One of following keys is missing or is empty in request body:\naddress"
            }
        });
        return;
	};
    try {    
        console.log(`Controller: getTrxBalance ${address}\n`)
        const trxBalance = await service.getTrxBalance(address);
        console.log(`Controller: wallet ${address} TRX balance is ${trxBalance}\n`)
        res.send({ status: "OK", data: trxBalance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


const getTokenBalance = async (req, res) => {
    const body = req.query;
    if ( 
        !body.owner ||
        !body.token ||
        !body.address 
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                owner; token; address"
            }
        })
		return;
	};
    try {
        console.log(`Controller: getTokenBalance ${JSON.stringify(body, null, 2)}\n`)
        const tokenBalance = await service.getTokenBalance(
            body.owner, body.token, body.address
        );
	    console.log(`Controller: wallet ${body.address} token balance is ${tokenBalance}\n`);
	    res.send({ status: "OK", data: tokenBalance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
        data: { error: error?.message || error },
        });
    };
};


const sendTrx = async (req, res) => {
    const body = req.query
    if ( 
        !body.target ||
        !body.amount ||
        !body.privateKey 
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                target; amount; privateKey"
            }
        })
		return;
	};
    try {
        console.log(`Controller: sendTrx ${JSON.stringify(body, null, 2)}\n`)
        const trxTransaction = await service.sendTrx(
            body.target, body.amount, body.privateKey
        );
	    console.log(`Controller: trxTransaction id ${trxTransaction.txid}\n`);
	    res.send({ status: "OK", data: trxTransaction.txid });
    } catch (error) {
        res.status(error?.status || 500).send({
        status: 'FAILED',
        data: { error: error?.message || error },
        });
    };
};


const sendToken = async (req, res) => {
    const body = req.query
    if ( 
        !body.owner ||
        !body.token ||
        !body.target ||
        !body.amount ||
        !body.privateKey
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: {
                error: "One of following keys is missing or is empty in request body:\n\
                owner; token; target; amount; privateKey"
            }
        })
		return;
	};
    try {
        console.log(`Controller: send tokens ${JSON.stringify(body, null, 2)}\n`)
        const tokenTransaction = await service.sendToken(
            body.owner, body.token, body.target, body.amount, body.privateKey
        );
	    console.log(`Controller: tokenTransaction ${JSON.stringify(tokenTransaction)}\n`)
	    res.send({ status: "OK", data: tokenTransaction });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    };
};


// TON //
const createTonWallet = async (req, res) => {
    try {
        console.log(`Controller: createWallet`);
        const wallet = await createTonWallet();
        res.send({ status: 'OK', data: wallet });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    }
};
  

const getTonBalance = async (req, res) => { 
    const { walletAddress } = req.query;
    if (!walletAddress) {
        res.status(400).send({
            status: 'FAILED',
            data: { error: 'Missing walletAddress in request query' },
        });
        return;
    }
    try {
        console.log(`Controller: getTonBalance for walletAddress: ${walletAddress}`);
        const balance = await getTonBalance(walletAddress);
        res.send({ status: 'OK', data: balance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    }
};
  

const getJettonBalance = async (req, res) => {
    const body = req.query;
    if (
        !body.walletAddress ||
        !body.jettonAddress
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: { error: 'Missing walletAddress or jettonAddress in request query' },
        });
        return;
    }
    try {
        console.log(`Controller: getJettonBalance for walletAddress: 
            ${walletAddress}, jettonAddress: ${jettonAddress}`);
        const balance = await getJettonBalance(walletAddress, jettonAddress);
        res.send({ status: 'OK', data: balance });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    }
};
  

const sendTonTransaction = async (req, res) => {
    const body = req.query;
    if ( 
        !body.fromWallet ||
        !body.toAddress || 
        !body.amount || 
        !body.privateKey
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: { error: 'Missing one or more of the required fields:\n\
                            fromWallet, toAddress, amount, privateKey' },
        });
        return;
    }
    try {
        console.log(`Controller: sendTonTransaction from ${fromWallet} to ${toAddress} amount ${amount}`);
        const txid = await sendTonTransaction(
            fromWallet, toAddress, amount, privateKey);
        res.send({ status: 'OK', data: txid });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
    }
};


const sendJettonTransaction = async (req, res) => {
    const body = req.query;
    if (
        !body.fromWallet ||
        !body.toAddress || 
        !body.jettonAddress || 
        !body.amount || 
        !body.privateKey
    ) {
        res.status(400).send({
            status: 'FAILED',
            data: { error: 'Missing one or more of the required fields:\n\
                            fromWallet, toAddress, jettonAddress, amount, privateKey' },
        });
        return;
    }
    try {
        console.log(`Controller: sendJettonTransaction 
                     from ${fromWallet} to ${toAddress} amount ${amount}`);
        const txid = await sendJettonTransaction(
            fromWallet, toAddress, jettonAddress, amount, privateKey);
        res.send({ status: 'OK', data: txid });
    } catch (error) {
        res.status(error?.status || 500).send({
            status: 'FAILED',
            data: { error: error?.message || error },
        });
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
    createTrxWallet,   
    getTrxBalance,
    getTokenBalance,
    sendTrx,
    sendToken,
    createTonWallet,
    getTonBalance,
    getJettonBalance,
    sendTonTransaction,
    sendJettonTransaction
};
