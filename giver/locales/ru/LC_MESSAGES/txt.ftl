# ####### #
# BUTTONS #
# ####### #

button-eth = ETHEREUM

button-sol = SOLANA

button-trx = TRON

button-ftm = FANTOM

button-back = Назад

button-account = Аккаунт

# ######## #
# MESSAGES #
# ######## #

fill-eth-address = Привет { $name }!
                   
                   В этом боте ты можешь получать
                   БЕСПЛАТНО Ethereum, Solana, Tron и Fantom!
                   
                   Все что нужно сделать - ввести свой адрес
                   ETH и отправить его сообщением  

fill-trx-address = Хорошо, введи адрес TRX

fill-sol-address = Отлично!

                   А теперь, введи адрес SOL

select-coin = Выбери монету, которую хочешь получить!
              Вывод может занять несколько минут...
            
              Один раз в неделю ты можешь получить на выбор:

              { $eth } Ethereum
              { $ftm } Fantom
              { $sol } Solana
              { $trx } Tron

account = Твои адреса кошельков и дата последнего получения монет

          ETH: <code>{ $eth_address }</code>
          (для получение FTM используется адрес ETH)

          SOL: <code>{ $sol_address }</code>

          TRX: <code>{ $trx_address }</code>

          Последний раз ты забирал монеты:
          { $last_get }

success-eth = Успешный вывод ETH!
              Хэш транзакции:
              { $hash }

success-trx = Успешный вывод TRX!
              ID транзакции:
              { $hash }

success-ftm = Успешный вывод FTM!
              Хэш транзакции:
              { $hash }

success-sol = Успешный вывод SOL!
              Signature транзакции:
              { $hash }

error-central-balance = Ошибка центрального кошелька

error-lastget = Вывод можно совершать 1 раз в Неделю!

error-address = Неверный Адрес!

error-ethaddress = Неверный ETH адрес!

error-soladdress = Неверный SOL адрес!

error-trxaddress = Неверный TRX адрес!

wrong-input = Неверный ввод!

unknown-message = Не понял, что ты сказал...