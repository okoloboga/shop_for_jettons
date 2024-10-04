# ####### #
# BUTTONS #
# ####### #

button-eth = ETHEREUM

button-sol = SOLANA

button-trx = TRON

button-ftm = FANTOM

button-back = Back

button-account = Account

# ######## #
# MESSAGES #
# ######## #

fill-eth-address = Hello { $name }!

                   In this bot you can get
                   FREE Ethereum, Solana, Tron and Fantom!

                   Аll you have to do is enter your ETH address and send it as a message

fill-trx-address = Good, enter the TRX address

fill-sol-address = Great!

                   Now, enter the SOL address

select-coin = Choose the coin you want to get!
              this may take a few minutes...

              Once a week you can get a choice of:

              { $eth } Ethereum
              { $ftm } Fantom
              { $sol } Solana
              { $trx } Tron

account = Your wallets addresses and last coin claim 

          ETH: <code>{ $eth_address }</code>
          (to get FTM use ETH address)

          SOL: <code{ $sol_address }</code>

          TRX: <code>{ $trx_address }</code>

          The last time you claimed coins:
          { $last_get }

success-eth = Successful withdrawal of ETH!
              Transaction hash:
              { $hash }

success-trx = Successful withdrawal of TRX!
              Transaction ID:
              { $hash }

success-ftm = Successful withdrawal of FTM!
              Transaction hash:
              { $hash }

success-sol = Successful withdrawal of SOL!
              Transaction signature:
              { $hash }

error-central-balance = Central wallet error

error-lastget = Withdrawal can be done once a week!

error-address = Invalid address!

error-ethaddress = Invalid ETH address!

error-soladdress = Invalid SOL address!

error-trxaddress = Invalid TRX address!

error-send = При отправке произошла ошибка...

wrong-input = Invalid input!

unknown-message = Can't understand you...