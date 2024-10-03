const express = require('express');
const controller = require('../controllers/controller');

const router = express.Router();
/**
 * @openapi
 * /api/ethbalance:
 *   get:
 *     tags:
 *       - ETH Balance
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
 * /api/ethaddress:
 *   get:
 *     tags:
 *       - ETH Address Validation
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
 * /api/sendeth:
 *   post:
 *     tags:
 *       - Send ETH
 *     parameters:
 *       - name: sender
 *         in: query
 *         type: string
 *         description: Senders address of wallet to send ETH
 *       - name: privateKey
 *         in: query
 *         type: string
 *         description: Wallet's private key for sign transaction
 *       - name: target
 *         in: query
 *         type: string
 *         description: Target address of wallet to send ETH
 *       - name: amount
 *         in: query
 *         type: string
 *         description: Amount of tokens to send
 *     responses:
 *       200:
 *         description: OK
 *       5XX:
 *         description: FAILED
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
router.post('/newwallet', controller.createWallet);
router.get('/trxbalance', controller.getTrxBalance);
router.get('/tokenbalance', controller.getTokenBalance);
router.post('/trxtransaction', controller.sendTrx);
router.post('/tokentransaction', controller.sendToken);


module.exports = router;
