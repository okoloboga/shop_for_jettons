const express = require('express');
const controller = require('../controllers/controller');

const router = express.Router();
/**
 * @openapi

 * /api/solbalance:
 *   get:
 *     tags:
 *       - SOL Balance
 *     parameters:
 *       - in: query
 *         name: address
 *         type: string
 *         description: Get ballance of Wallet by Address
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/soladdress:
 *   get:
 *     tags:
 *       - SOL Address Validation
 *     parameters:
 *       - in: query
 *         name: address
 *         type: string
 *         description: Validate Address of Wallet
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/sendsol:
 *   post:
 *     tags:
 *       - Send SOL
 *     parameters:
 *       - name: sender
 *         in: query
 *         type: string
 *         description: Senders address of wallet to send SOL
 *       - name: privateKey
 *         in: query
 *         type: string
 *         description: Wallet's private key for sign transaction
 *       - name: target
 *         in: query
 *         type: string
 *         description: Target address of wallet to send SOL
 *       - name: amount
 *         in: query
 *         type: string
 *         description: Amount of tokens to send
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/ftmbalance:
 *   get:
 *     tags:
 *       - FTM Balance
 *     parameters:
 *       - in: query
 *         name: address
 *         type: string
 *         description: Get ballance of Wallet by Address
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/sendftm:
 *   post:
 *     tags:
 *       - Send FTM
 *     parameters:
 *       - name: sender
 *         in: query
 *         type: string
 *         description: Senders address of wallet to send FTM
 *       - name: privateKey
 *         in: query
 *         type: string
 *         description: Wallet's private key for sign transaction
 *       - name: target
 *         in: query
 *         type: string
 *         description: Target address of wallet to send FTM
 *       - name: amount
 *         in: query
 *         type: string
 *         description: Amount of tokens to send
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/newwallet:
 *   post:
 *     tags:
 *       - New Wallet
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/trxbalance:
 *   get:
 *     tags:
 *       - TRX Balance
 *     parameters:
 *       - in: query
 *         name: address
 *         type: string
 *         description: Get ballance of Wallet by Address
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/tokenbalance:
 *   get:
 *     tags:
 *       - Get Token Balance
 *     parameters:
 *       - name: owner
 *         in: query
 *         type: string
 *         description: Token owner's address
 *       - name: token
 *         in: query
 *         type: string
 *         description: Token contract address
 *       - name: address
 *         in: query
 *         type: string
 *         description: Address of wallet with token
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/trxtransaction:
 *   post:
 *     tags:
 *       - Send TRX
 *     parameters:
 *       - name: target
 *         in: query
 *         type: string
 *         description: Target address of wallet to send TRX
 *       - name: amount
 *         in: query
 *         type: string
 *         description: Amount of tokens to send
 *       - name: privateKey
 *         in: query
 *         type: string
 *         description: Wallet's private key for sign transaction
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/tokentransaction:
 *   post:
 *     tags:
 *       - Send Token
 *     parameters:
 *       - name: owner
 *         in: query
 *         type: string
 *         description: Token owner's address
 *       - name: token
 *         in: query
 *         type: string
 *         description: Token contract address
 *       - name: target
 *         in: query
 *         type: string
 *         description: Target address of wallet to send Tokens
 *       - name: amount
 *         in: query
 *         type: string
 *         description: Amount of tokens to send
 *       - name: privateKey
 *         in: query
 *         type: string
 *         description: Wallet's private key for sign transaction
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/createTonWallet:
 *   get:
 *     tags:
 *       - Wallet
 *     summary: Create a new TON wallet
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/getTonBalance:
 *   get:
 *     tags:
 *       - Balance
 *     summary: Get TON balance of a wallet
 *     parameters:
 *       - in: query
 *         name: walletAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Wallet address to get the TON balance
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/getJettonBalance:
 *   get:
 *     tags:
 *       - Balance
 *     summary: Get Jetton balance of a wallet
 *     parameters:
 *       - in: query
 *         name: walletAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Wallet address to get the Jetton balance
 *       - in: query
 *         name: jettonAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Jetton contract address
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/sendTonTransaction:
 *   post:
 *     tags:
 *       - Transaction
 *     summary: Send TON to another wallet
 *     parameters:
 *       - in: query
 *         name: fromWallet
 *         required: true
 *         schema:
 *           type: string
 *         description: Sender wallet address
 *       - in: query
 *         name: toAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Receiver wallet address
 *       - in: query
 *         name: amount
 *         required: true
 *         schema:
 *           type: string
 *         description: Amount of TON to send
 *       - in: query
 *         name: privateKey
 *         required: true
 *         schema:
 *           type: string
 *         description: private key for sender wallet
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 * /api/sendJettonTransaction:
 *   post:
 *     tags:
 *       - Transaction
 *     summary: Send Jetton tokens to another wallet
 *     parameters:
 *       - in: query
 *         name: fromWallet
 *         required: true
 *         schema:
 *           type: string
 *         description: Sender wallet address
 *       - in: query
 *         name: toAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Receiver wallet address
 *       - in: query
 *         name: jettonAddress
 *         required: true
 *         schema:
 *           type: string
 *         description: Jetton contract address
 *       - in: query
 *         name: amount
 *         required: true
 *         schema:
 *           type: string
 *         description: Amount of Jetton to send
 *       - in: query
 *         name: privateKey
 *         required: true
 *         schema:
 *           type: string
 *         description: private key for sender wallet
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
 */


// ETHEREUM //
router.get('/ethbalance', controller.getEthBalance);
router.get('/ethaddress', controller.checkEthAddress);
router.post('/ethtransaction', controller.sendEth);


// SOLANA //
router.get('/solbalance', controller.getSolBalance);
router.get('/soladdress', controller.checkSolAddress);
router.post('/soltransaction', controller.sendSol);


// FANTOM //
router.get('/ftmbalance', controller.getFtmBalance);
router.post('/ftmtransaction', controller.sendFtm);


// TRONWEB //
router.post('/newwallet', controller.createTrxWallet);
router.get('/trxbalance', controller.getTrxBalance);
router.get('/tokenbalance', controller.getTokenBalance);
router.post('/trxtransaction', controller.sendTrx);
router.post('/tokentransaction', controller.sendToken);


// TON //
router.get('/newTonWallet', controller.createTonWallet);
router.get('/tonbalance', controller.getTonBalance);
router.get('/jettonbalance', controller.getJettonBalance);
router.post('/tontransaction', controller.sendTonTransaction);
router.post('/jettontransaction', controller.sendJettonTransaction);


module.exports = router;
