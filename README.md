# Shop template in Telegram
Empty template for Market based in Telegram Bot. 
Working example: https://t.me/nitrogen_market_bot
If registration is closed - you can write me in Telegram to get access
or support the project in TRON, to open registration.
<code></code>

## How it works?
Three entities: Shop, Game, Admin panel. 
Market use tokens, based on TRON.

### Costumer
Shop and Game for costumers. In Main Menu costumer can switch between items, see catalog, go to game, see account data.

Costumers place orders, require: count of items; delivery address. Placed order sends to manager. When manager confirm or decline order - costumer receive notification.

In Account Menu costumer see self ID, sum of purchases, count of purchases, count of referrals and referral link, count of tokens on wallet, link for purchase tokens and self TRON address.

In game costumer can win tokens. Game: Rock-Paper-Scissors for two players. Players make bet and play for 2 wins.

### Admin
Admin can change order status: confirm, decline, complete. Add new item, edit and delete items.

### Database
Users, Catalog, Income, Orders, Outcome, Variables, Edited
Redis user for Game cache 

### Requires
Python3 (built on 3.12), <code>aiogram aiogram_dialog sqlalchemy psycorg redis fluentogram PyYAML environs validators</code>

## I18N
Ready for EN and RU

## Feedback
tg: @okolo_boga
